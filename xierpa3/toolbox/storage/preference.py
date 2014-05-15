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
#    preference.py
#
class Preference(dict):
    
    def __repr__(self):
        return 'Preference(%s)' % dict.__repr__(self)
    
    def __setitem__(self, keys, value):
        keys = self.getKeyList(keys)
        if not keys:
            pass
        elif len(keys) == 1:
            dict.__setitem__(self, keys[0], value)
        elif isinstance(self.get(keys[0]), Preference):
            self[keys[0]][keys[1:]] = value
        else:            
            p = Preference()
            p[keys[1:]] = value
            dict.__setitem__(self, keys[0], p)

    def __getitem__(self, keys):
        keys = self.getKeyList(keys)
        if not keys:
            return None
        p = dict.__getitem__(self, keys[0])
        if len(keys) > 1 and isinstance(p, (Preference, dict)):
            return p[keys[1:]]
        return p

    def getKeyList(self, keys):
        if isinstance(keys, (list, tuple)):
            return keys
        assert isinstance(keys, basestring)
        keys = keys.split('/')
        return keys
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
        
    @classmethod
    def fromDict(cls, d):
        assert isinstance(d, (Preference, dict))
        p = cls()
        for key, value in d.items():
            if isinstance(value, dict):
                value = cls.fromDict(value)
            p[key] = value
        return p
        
if __name__ == '__main__':        
    from xierpa3.toolbox.parsers.json import cjson
    p = Preference()
    p['aa/bb'] = 1234
    print p
    print p['aa']
    print p['aa/bb']
    p['aa/cc/dd'] = 2345
    print p
    p['aa/cc']['zz'] = 3456
    print p
    p['a/xy'] = (10,30)
    print p
    """
    print '--- Encoded by json'
    json = json.encode(p)
    print json
    print '--- Decoded by json'
    print Preference.fromDict(json.decode(json))
    """
