# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#     dynamodb.py
#
import cjson, httplib, datetime, time, hashlib, hmac, re
from xierpa3.constants.constants import C # Using the config for db access keys

class DynamoDB:

    NOW = None # Time stamp
    CONNECTION = None # Keep connection open in class.
    # Get keys from config, but also allow redefine by inheritance.
    AMAZON_REGION = C.AMAZON_REGION
    AMAZON_HOST = C.AMAZON_HOST
    CONTENT_TYPE = C.CONTENT_TYPE
    DYNAMODB_URI = C.DYNAMODB_URI
    DYNAMODB_TARGET = C.DYNAMODB_TARGET
    DYNAMODB_SIGNING_ALGORITHM = C.DYNAMODB_SIGNING_ALGORITHM

    PROVISIONED_THROUGHPUT = {} # for avoiding maxing out write requests
    ITEMS_PER_SECOND = {}

    def __init__(self):
        pass

    def _now(self):
        return datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")

    def _createSignature(self, headers, payload):
        # see: http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html

        canonicalheaders = {}
        for k, v in headers.items():
            canonicalheaders[k.lower()] = re.sub(r'\s\s+', ' ', v.strip())

        signedheaders = ";".join(sorted(canonicalheaders.keys()))

        # \n separated: method, uri, query string, canonical headers, signed headers, hex hashed payload
        canonicalrequest = "\n".join((
            'POST',
            self.DYNAMODB_URI,
            '',
            "".join([k + ':' + canonicalheaders[k] + "\n" for k in sorted(canonicalheaders.keys())]),
            signedheaders,
            hashlib.sha256(payload).hexdigest(),
        ))

        canonicalrequest = hashlib.sha256(canonicalrequest).hexdigest()

        credentialscope = "{0}/{1}/dynamodb/aws4_request".format(self.NOW[:8], self.AMAZON_REGION)

        # \n separated: algorithm, requestdate, credential scope, canonical request
        stringtosign = "\n".join((
            self.DYNAMODB_SIGNING_ALGORITHM,
            self.NOW,
            credentialscope,
            canonicalrequest
        ))

        def HMAC(key, msg, hex=False):
            temp = hmac.new(key, msg, hashlib.sha256)
            if hex:
                return temp.hexdigest()
            else:
                return temp.digest()

        kSecret = Config.SECRETACCESSKEY # this is defined by the application
        kDate = HMAC("AWS4" + kSecret, self.NOW[:8])
        kRegion = HMAC(kDate, self.AMAZON_REGION)
        kService = HMAC(kRegion, "dynamodb")
        kSigning = HMAC(kService, "aws4_request")

        signature = HMAC(kSigning, stringtosign, hex=True)

        return self.DYNAMODB_SIGNING_ALGORITHM + " " + ", ".join((
            "Credential={0}/{1}".format(Config.ACCESSKEYID, credentialscope),
            "SignedHeaders={0}".format(signedheaders),
            "Signature={0}".format(signature),
        ))

    def openConnection(self, reset=True):
        if reset:
            try:
                self.CONNECTION.close()
            except:
                pass

        self.CONNECTION = httplib.HTTPSConnection(self.AMAZON_HOST, timeout=1.0)


    def request(self, operation, req={}, persistent=False):
        '''
        <doc>Takes object or JSON <attr>req</attr> and dispatches the actual HTTP request to AWS. Returns raw response object.
        </doc>
        '''
        # save this so it's always the same for this request
        self.NOW = self._now()

        if not isinstance(req, basestring):
            req = cjson.encode(req)

        headers = {
            'host': self.AMAZON_HOST,
            'x-amz-date': self.NOW,
            'x-amz-target': "{0}.{1}".format(self.DYNAMODB_TARGET, operation),
            'content-type': self.CONTENT_TYPE,
        }

        headers['Authorization'] = self._createSignature(headers, req)

        if not persistent or not self.CONNECTION:
            self.openConnection()

        # TODO: handle timeout or failure

        try:
            self.CONNECTION.request('POST', self.DYNAMODB_URI, headers=headers, body=req)
        except:
            self.openConnection()
            self.CONNECTION.request('POST', self.DYNAMODB_URI, headers=headers, body=req)

        result = self.CONNECTION.getresponse()
        json = result.read()

        # print json

        if not persistent:
            self.CONNECTION.close()
            self.CONNECTION = None

        return cjson.decode(json)

    def _formatValue(self, val):
        if isinstance(val, dict):
            raise ValueError("Dicts not allowed in DynamoDB")

        type = None
        if isinstance(val, (list, tuple, set)):
            for v in val:
                if isinstance(v, (int, float, long)):
                    type = "NS"
                    val = [str(v) for v in val]
                else:
                    type = "SS"
                break
        elif isinstance(val, (int, float, long)):
            type = "N"
            val = str(val)
        else:
            type = "S"

        return {type:val}

    def _unformatValue(self, val, depth=0):
        if depth == 0:
            return dict([(k, self._unformatValue(val[k], depth + 1)) for k in val.keys()])

        # val should be a dict with the type specifier and the actual value
        assert isinstance(val, dict)
        assert len(val) == 1

        type = val.keys()[0]
        value = val.values()[0]

        def str2num(s):
            if '.' in s:
                return float(s)
            else:
                return int(s)

        if type == "N":
            return str2num(value)
        elif type == "NS":
            return [str2num(v) for v in value]
        else:
            return value


    def add(self, table, items):
        if not isinstance(items, (list, tuple, set)):
            # single put
            for item in items:
                req = {
                    "TableName": table,
                    "Item": dict([(k, self._formatValue(item[k])) for k in item.keys()]),
                }

                result = self.request('PutItem', req)

                return result

        # batch put

        # don't exceed provisioned throughput
        if table in self.ITEMS_PER_SECOND:
            persecond = self.ITEMS_PER_SECOND[table]
        else:
            tableinfo = self.request("DescribeTable", {"TableName":table})
            writeunits = int(tableinfo["Table"]["ProvisionedThroughput"]["WriteCapacityUnits"])
            indexes = len(tableinfo["Table"].get("LocalSecondaryIndexes") or [])
            persecond = self.ITEMS_PER_SECOND[table] = self.PROVISIONED_THROUGHPUT[table] = int(writeunits) / (indexes + 1)

        if isinstance(items, set):
            items = list(items)

        perreq = 25 # set limit

        starttime = datetime.datetime.now()

        # each run through this loop takes a minimum of 1 second, to not go over our per-second writes
        retry = []
        itemcount = len(items)
        for idx in range(0, itemcount, persecond):
            # do all the work before checking time time, since it will take a fraction of a second
            reqs = []

            # but there's more! Limit of 25 items per request.
            for subidx in range(0, persecond, perreq):
                if idx + subidx >= itemcount:
                    break
                reqs.append({"ReturnConsumedCapacity":"TOTAL", "RequestItems":{table:[
                    {"PutRequest":{"Item":dict([(k, self._formatValue(item[k])) for k in item.keys()])}}
                    for item in items[idx + subidx:idx + subidx + perreq]
                ]}});


            # now see if more than a second has passed since the last round
            diff = datetime.datetime.now() - starttime
            print idx,
            if diff.seconds < idx / persecond:
                tosleep = 1 - diff.microseconds / 1000000.0
                print "Waiting {0}".format(tosleep),
                time.sleep(tosleep)

            # go!
            consumed = 0
            for req in reqs:
                result = self.request('BatchWriteItem', req, persistent=True)
                if 'message' in result:
                    print result.get('__type'), result['message']
                    print req
                if 'ConsumedCapacity' in result:
                    consumed += result["ConsumedCapacity"][0]["CapacityUnits"]
                unprocessed = result.get("UnprocessedItems")
                if unprocessed:
                    # be less agressive next time, to a point
                    # if persecond > self.PROVISIONED_THROUGHPUT[table] * 0.7:
                    #     self.ITEMS_PER_SECOND[table] = int(persecond * 0.95)
                    retry.append(unprocessed)

            print "Wrote {0} requests, consumed {1} units".format(len(reqs), consumed)

        # resend the stragglers, recursively
        while retry:
            num = len(retry)
            print "Retrying {0} requests".format(num),
            consumed = 0
            time.sleep(1)
            for i in range(num):
                req = {"ReturnConsumedCapacity":"TOTAL", "RequestItems" : retry.pop(0)}
                result = self.request('BatchWriteItem', req, persistent=True)
                if 'message' in result:
                    print result.get('__type'), result['message']
                    print req
                if 'ConsumedCapacity' in result:
                    consumed += result["ConsumedCapacity"][0]["CapacityUnits"]
                unprocessed = result.get("UnprocessedItems")
                if unprocessed:
                    retry.append(unprocessed)
            print "Consumed {0} units".format(consumed)

    def get(self, table, key, fields=None):
        req = {
            "TableName": table,
            "Key": dict([(k, self._formatValue(key[k])) for k in key.keys()]),
        }

        if fields:
            req["AttributesToGet"] = fields

        result = self.request("GetItem", req)

        if result and "Item" in result:
            return self._unformatValue(result["Item"])
        else:
            return None

    def query(self, table, primaryfield, primaryvalue, secondaryfield, secondaryvalue, op="=", limit=None, reverse=False, fields=None, index=None):
        operators = {
            "=": "EQ",
            "<": "LT",
            "<=": "LE",
            ">": "GT",
            ">=": "GE",
        }

        req = {
            "TableName": table,
            "IndexName": index or "{0}-index".format(secondaryfield),
            "KeyConditions": {
                primaryfield: { "AttributeValueList": [ self._formatValue(primaryvalue) ], "ComparisonOperator": "EQ" },
                secondaryfield: { "AttributeValueList": [ self._formatValue(secondaryvalue) ], "ComparisonOperator": operators.get(op) or op },
            },
        }

        if fields:
            req["AttributesToGet"] = fields

        if limit:
            req["Limit"] = limit

        if reverse:
            req["ScanIndexForward"] = False

        result = self.request("Query", req)

        if result and "Items" in result:
            return [self._unformatValue(item) for item in result['Items']]
        else:
            return []

    def delete(self, table, key):
        req = {
            "TableName": table,
            "Key": dict([(k, self._formatValue(key[k])) for k in key.keys()]),
        }

        result = self.request("DeleteItem", req)
