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
#    validator.py
#
#    isEmail True if this is a valid email address
#    isUrl True if this is a valid url
#    isTelephone # Only 'nl' format of 10 figures
#    isZipcode
#    isDate # Does not check yet on leap years, 'nl' is yyyy/mm/dd, otherwise yyyy/dd/mm
#    istime # Not yet implemented
#    isLength # Parameter: length value of min, max
#    isRange # Parameters: min, mas
#    isin # Parameters: comma separated list of possible values    
#
import re
from time import localtime, strftime
from xierpa3.toolbox.dating import DateTime

class Validator:

    # @@@ To add: validate bank account
    
    # Used for patterns in email and url checking
    
    HTTP = 'http://'
    SPECIALCHARS = """\(\)<>@,;:#\\\"\[\]"""
    KNOWNDOMAINS = 'com|net|org|edu|int|mil|gov|arpa|biz|aero|name|coop|info|pro|museum|cat'
    QUOTEDUSER = """^\"([^\"]*)\"$"""
    EMAILUSER = '^[^' + SPECIALCHARS + ']*$'
    IPADDRESS = u'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    DOMAIN = u'^(?:([^' + SPECIALCHARS + ']*)\.)?' + '(' + KNOWNDOMAINS + '|[a-zA-Z]{2})$'
    IMAGENAME = u'([-0-9a-zA-Z_\.~]*[\.](?:jpg|jpeg|png|tiff|gif|pdf)$)'
    PDFNAME = u'([-0-9a-zA-Z_\.~]*[\.](?:pdf)$)'
    ZIPNAME = u'([-0-9a-zA-Z_\.~]*[\.](?:zip)$)'
    
    EMAILPATTERN = re.compile(u'(.+)@(.+)$')
                            # http://regexlib.com/REDetails.aspx?regexp_id=1605
                            # Don't take "." and "," at the end of the url, since it can be part of the containing plain text.
    URLPATTERN = '(?:http://)([-0-9a-zA-Z_\.~]*\.?[-0-9a-zA-Z_\.~]*\.(?:arpa|arts|biz|com|edu|firm|gov|info|int|mil|nato|net|nom|org|rec|store|web|jp|' +\
                                    'ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|' +\
                                    'cc|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|de|di|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|' +\
                                    'gb|gd|ge|gf|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|in|io|iq|ir|is|it|jo|jm|jp|ke|' +\
                                    'kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|' +\
                                    'mu|mv|mw|mx|my|mz|an|nc|ne|nf|ng|ni|nl|no|np|nr|nt|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|pt|pw|py|qa|re|ro|' +\
                                    'ru|rw|sa|sb|sc|sd|se|sq|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tm|tn|to|tp|tr|tt|tv|' +\
                                    'tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zr|zw)' + \
                                    '[\S]*[^\.\,\s])'
    QUOTEDUSERPATTERN = re.compile(QUOTEDUSER)
    USERPATTERN = re.compile(EMAILUSER)
    IPPATTERN = re.compile(IPADDRESS)
    DOMAINPATTERN = re.compile(DOMAIN)
    IMAGENAMEPATTERN = re.compile(IMAGENAME)
    PDFNAMEPATTERN = re.compile(PDFNAME)
    ZIPNAMEPATTERN = re.compile(ZIPNAME)
    DATEPATTERN = re.compile(u'^[\s]*([\d]+)[-/\.]([\d]+)[-/\.]([\d]+)[\s]*$')
    ALLEMAILSPATTERNS = re.compile(u'[a-z0-9\.-]+@[a-z0-9\.-]+[\.][a-z]+')

    ZIPCODEPATTERNS = {
        'nl':        re.compile(u'^[0-9]{4}\s?[a-zA-Z]{2}$')
    }
    TELEPHONEPATTERNS = {
        'nl':        re.compile(u'^(?:[\s]*(?:\+?|[0]{2})[\s]?(?:[-0-9\/][-\s]*){11}[\s]*|[\s]*(?:[-0-9\/][-\s]*){10}[\s]*)$')
    }
    @classmethod
    def arg2Arg(cls, value):
        """
            Expand the argument if it contains keywords.
            These keywords cannot be tested because the value will change in time:

            v.arg2Arg('today')
            2006/3/4
            v.arg2Arg('thisday')
            11
            v.arg2Arg('thismonth')
            2
            v.arg2Arg('lastyear')
            2004
            v.arg2Arg('thisyear')
            2005
            v.arg2Arg('nextyear')
            2006
            
            >>> v = Validator()
            >>> v.arg2Arg('1234')
            '1234'
            >>> v.arg2Arg('  1234  ')
            '1234'
            >>> v.arg2Arg('infinite')
            '10.0e99'
        """
        if isinstance(value, basestring):
            value = value.strip()    # Remove trailing whitespace
            if value in ('today', 'now'):
                # Answer (year, month, day) tuple
                d = DateTime(date=value)
                return d.date2s(d.getdate(), 'dd/mm/yyyy')
            if value == 'thisday':
                return strftime("%d",localtime())
            if value == 'thismonth':
                return strftime("%m",localtime())
            if value == 'lastyear':
                return repr(int(strftime("%Y",localtime())) - 1)
            if value == 'thisyear':
                return strftime("%Y",localtime())
            if value == 'nextyear':
                return repr(int(strftime("%Y",localtime())) + 1)
            if value == 'infinite':
                return '10.0e99'
        return value
        
    @classmethod
    def validate(cls, value, params):
        """
            Validate a value
            The protocol is in params.
            For protocol that need other values to test against, 
            params can also be a comma separated list
        
            >>> v = Validator()
            >>> v.validate(123, 'isnumber')
            True
            >>> v.validate(123, 'isinteger')
            True
            >>> v.validate(123.44, 'isinteger')
            False
            >>> v.validate('aaaaa', 'isLength, 5')
            True
            >>> v.validate('1/9/2005', 'isDate')
            True
            >>> v.validate('1/13/2005', 'isDate')
            False
            >>> v.validate('30/2/2005', 'isDate')
            False
            >>> v.validate('01/1500/2005', 'isDate')
            False
            >>> v.validate('a', 'isin, a,b,c,d,e,f,g,h')
            True
            >>> v.validate(10, 'isRange, 0, 100')
            True
            >>> v.validate(10, 'isRange, 50, 100')
            False
            >>> v.validate('1/1/1966', 'isRange,1/1/1870,1/1/2008')
            True
            >>> v.validate(None, 'isRange,1/1/1870,1/1/2008')
            False
            >>> v.validate('', 'isempty')
            True

        """
        if value is None:
            return False
        split = params.split(',')
        func = split[0].strip()
        if func == 'isLength':
            if len(split) == 2:
                return cls.isLength(value, split[1])
            else:
                return cls.isLength(value, split[1], split[2])
        if func == 'isempty':
            return value == ''
        if func == 'isRange':
            return cls.isRange(value, split[1], split[2])
        if func == 'isin':
            return cls.isin(value, split[1:])
        if func == 'isPattern':
            return cls.isPattern(value, ','.join(split[1:]))
    
        # Now we know that we look for single value validators
        validators = {
            'isnumber':        cls.isnumber,
            'isinteger':    cls.isinteger,
            'isDate':        cls.isDate,
            'isfuture':        cls.isfuture,
            'ispast':        cls.ispast,
            'isEmail':         cls.isEmail,
            'isTwitter':     cls.isTwitter,
            'isUrl':         cls.isUrl,
            'isImage':        cls.isImage,
            'isBank':         cls.isBank,
            'isgiro':         cls.isgiro,
            'isBankgiro':     cls.isBankgiro,
            'isZipcode':    cls.isZipcode,
            'isTelephone':    cls.isTelephone,
        }
        return validators[func](value)

    @classmethod
    def isPattern(cls, value, pattern):
        """
        Compare to the re pattern. 
        Note that this is kinda expensive, since the pattern is compiled again
        every time that this method is called. So if one of the other other
        check fit the need, then that one is more efficient to use.

            >>> v = Validator()
            >>> v.isPattern('1234', '^[\d]*$')
            True
            >>> v.isPattern('1234xxxx', '^[\d]*$')
            False
            >>> v.isPattern('aaaaaa', '^[a-zA-Z]*$')
            True
            >>> v.isPattern('12345aaaaaa', '^[a-zA-Z]*$')
            False
            >>> v.isPattern('', '^[a-zA-Z]*$')
            False
            >>> v.isPattern(None, '^[a-zA-Z]*$')
            False
        """
        if not value:
            return False
        p = re.compile(pattern)                                        # Compile the pattern
        return re.findall(p, value) != []                            # Test if found something
        
#     def istrue(self, value):
#         """
#             Interpret the value to be not false by testing if in FALSEVALUES
# 
#             >>> v = Validator()
#             >>> v.istrue(True)
#             True            
#             >>> v.istrue(1)
#             True            
#             >>> v.istrue('aaa')
#             True            
#             >>> v.istrue(False)
#             False            
#             >>> v.istrue(0)
#             False            
#             >>> v.istrue('none')
#             False            
#         """
#         return self.value2Bool(value)
#     
#     def isfalse(self, value):
#         """
#             Interpret the value to be false by testing if in FALSEVALUES
# 
#             >>> v = Validator()
#             >>> v.istrue(True)
#             False            
#             >>> v.istrue(1)
#             False            
#             >>> v.istrue('aaa')
#             False            
#             >>> v.istrue(False)
#             True            
#             >>> v.istrue(0)
#             True            
#             >>> v.istrue('none')
#             True            
#         """
#         return not self.value2Bool(value)
#     
    @classmethod
    def isnbsp(cls, s):
        return s in ('<nbsp/>', '&nbsp;')
        
    @classmethod
    def isnumber(cls, value):
        """
        Test if the value is a valid number
        
            >>> v = Validator()
            >>> v.isnumber(1234)
            True
            >>> v.isnumber(12341234123412341234123412341234)
            True
            >>> v.isnumber(11212.323e-20)
            True
            >>> v.isnumber('3333XX')
            False
            >>> v.isnumber('')
            False
            >>> v.isnumber(None)
            False
        """
        if isinstance(value, (int, long, float)):                    # True if value is already a number
            return True
        try:
            float(value)                                            # Test if this can be converted to a number
            return True
        except:
            return False
            
    @classmethod
    def isinteger(cls, value):
        """
        Test if the value is a valid integer
        
            >>> v = Validator()
            >>> v.isinteger(1234)
            True
            >>> v.isinteger(12341234123412341234123412341234)
            True
            >>> v.isinteger(11212.323e-20)
            False
            >>> v.isinteger('3333XX')
            False
            >>> v.isinteger('')
            False
            >>> v.isinteger(None)
            False
        """
        if isinstance(value, (int, long)):                            # True if value is already a number
            return True
        try:
            if int(value) == float(value):                            # Test if this can be converted to a integer
                return True                                            # False if it got a float
            return False
        except:
            return False
            
    @classmethod
    def isLength(cls, value, minrange, maxrange = None):
        """
        If only minrange, them do an exact match on the value
        If maxrange id defined, then match on the range between 
        the values inclusive by calling self.isRange()

            >>> v = Validator()
            >>> v.isLength('', 0)
            True
            >>> v.isLength('1234', 4)
            True
            >>> v.isLength('aaaaa', 5)
            True
            >>> v.isLength('aaaaa', 6)
            False
            >>> v.isLength(None, 6)
            False
        """
        if value is None:                                            # None does not have a length, empty string is allowed.
            return False
        value = cls.arg2Arg(value)
        if isinstance(value, basestring):                            # In case of a string, simply answer the length
            l = len(value)
        elif isinstance(value, (int, long, float)):                    # In case of a number, answer the number of digits
            l = len(`value`)

        minrange = cls.arg2Arg(minrange)
        if maxrange is None:
            if isinstance(minrange, basestring):                    # Make sure length is a number
                minrange = int(minrange)
            return l == minrange                                    # In case it is another object that knows its length
        else:
            maxrange = cls.arg2Arg(maxrange)
            return cls.isRange(l, minrange, maxrange)
        
    @classmethod    
    def isRange(cls, value, minrange, maxrange):
        """
        Range testing is inclusive on the margins
        minrange <= value <= maxrange
        So minrange == 10 and value == 10 is true
        Float values can be defined with comma's or periods.
        
        Minrange and maxrange are dates or numbers.
        Note that minrange is the relative number of days from today, if defined as number
        The maxrange is the relative number of days if defined as number.
        
            >>> v = Validator()
            >>> v.isRange('today', -2, 2)
            True
            >>> v.isRange('today', -100, 200)
            True
            >>> v.isRange('today', 100, 200)
            False
            >>> v.isRange('today', '3/3/2002', '3/12/2030')
            True
            >>> v.isRange('today', 'today', 'today')
            False
            >>> v.isRange('5/11/1988', '4/11/1988', '6/11/1988')
            True
            >>> v.isRange('5/11/1988', '4/11/2004', '6/11/2004')
            False
            >>> v.isRange('10/10/2015', 'today', '7200')
            True
            >>> v.isRange('10/10/2015', 'today', '720')
            False
            >>> v.isRange('50', '0', '100')
            True
            >>> v.isRange(50, 0, 100)
            True
            >>> v.isRange(-100, 50, 100)
            False
            >>> v.isRange(10,30,100)
            False
            >>> v.isRange('0.4',0,1)
            True
            >>> v.isRange('0,4','0,3','0,8')
            True
            >>> v.isRange('','0,3','0,8')
            False
            >>> v.isRange(None, None, None)
            False
        """
        if not value:
            return False
        value = cls.arg2Arg(value)
        minrange = cls.arg2Arg(minrange)                            # Allow conversion of 'today' or 'infinite'
        maxrange = cls.arg2Arg(maxrange)        
        
        if cls.isDate(value):                                        # Format is date string?

            d = DateTime(date=value)
            thisyear, thismonth, thisday = d.s2date(cls.arg2Arg('today'))    # Get totay for relative calculation
            year, month, day = d.s2date(value)
            
            if cls.isDate(minrange):                                # Minrange is defined as date?
                minyear, minmonth, minday = d.s2date(minrange)
            else:                                                    # Else it be relative number of days instead
                minyear, minmonth, minday = d.futureday(thisyear, thismonth, thisday, number=int(minrange))        

            if cls.isDate(maxrange):
                maxyear, maxmonth, maxday = d.s2date(maxrange)
            else:
                maxyear, maxmonth, maxday = d.futureday(thisyear, thismonth, thisday, number=int(maxrange))        

            if minyear < year < maxyear:                            # Precheck, to avoid the limit in 1970 < mktime < 2040
                return True
            if not (1970 < year < 2040):                            # Can't check other than this interval when using mktime in dating
                return False                                        # when on of the limits is same as range years. False to be sure
                
            # Now we have to check the dates, but still one of the ranges can be outside the 1970 < mktime < 2040 range
            # so we'll crop them on both limits, which is safe because we know that thisyear is already within the limits.
            
            return d.dates2difference((min(2040, max(1970, minyear)), minmonth, minday), (year, month, day)) > 0 and\
                   d.dates2difference((min(2040, max(1970, maxyear)), maxmonth, maxday), (year, month, day)) < 0
        else:
            try:
                if isinstance(minrange, basestring):
                    minrange = float(minrange.replace(',','.'))
                if isinstance(maxrange, basestring):
                    maxrange = float(maxrange.replace(',','.'))
                if isinstance(value, basestring):
                    value = float(value.replace(',','.'))
            except:
                return False  # Any error as with None or string, aswer false

        result = minrange <= value <= maxrange
        return result
    
    @classmethod
    def isImage(cls, value):
        """
        Test if the value is the reference to an image."
        """
        return bool(cls.IMAGENAMEPATTERN.findall(value))

    def isPdf(self, value):
        """
        Test if the value is the reference to an image."
        """
        return bool(self.PDFNAMEPATTERN.findall(value))

    def isZip(self, value):
        """
        Test if the value is the reference to an image."
        """
        return bool(self.ZIPNAMEPATTERN.findall(value))

    @classmethod
    def isin(cls, value, options):
        """
        Test if the value is in options.
        If options is not a list, then do a comman split.
        We have to run through them separately, because the
        options come from a comma separated list, so the still
        may contain heading and trailing spaces

        
            >>> v = Validator()
            >>> v.isin('50', ['0', '50', '100'])
            True
            >>> v.isin(50, [0, 50, 100])
            True
            >>> v.isin(51, [0, 50, 100])
            False
            >>> v.isin('ccc', 'aaa, bbb, ccc')
            True
            >>> v.isin('cccc', 'aaa, bbb, ccc')
            False
            >>> v.isin('', '')
            False
            >>> v.isin(None, None)
            False
        """
        if not value or not options:
            return False
        if not isinstance(options, (list, tuple)):
            options = options.split(',')
        if isinstance(value, basestring):
            value = value.strip()
        for option in options:
            if isinstance(option, basestring):
                option = option.strip()
            if value == option:
                return True
        return False
    
    @classmethod    
    def isDate(cls, value, country='nl'):
        """
        Check if value is a valid date. @@@ Still add checking on leap year
        
            >>> v = Validator()
            >>> v.isDate('2003/04/04')
            True
            >>> v.isDate('04/04/2004')
            True
            >>> v.isDate('14/04/2004')
            True
            >>> v.isDate('32-04-2004')
            False
            >>> v.isDate('14-04-2004')
            True
            >>> v.isDate('    14.04.2004')
            True
            >>> v.isDate('4-14-2004', 'usa')
            True
            >>> v.isDate('14-04-2004', 'usa')
            False
            >>> v.isDate('2000-33-44')
            False
            >>> v.isDate('2000-0202')
            False
            >>> v.isDate('2000-02-==02')
            False
            >>> v.isDate('aaa')
            False
            >>> v.isDate('2003/3')
            False
            >>> v.isDate('200-233-444')
            False
            >>> v.isDate('10-2000-12')
            False
            >>> v.isDate('10')
            False
            >>> v.isDate(10)
            False
            >>> v.isDate('')
            False
            >>> v.isDate(None)
            False
        """
        monthdays = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        try:
            split = re.findall(cls.DATEPATTERN, value)    
        except TypeError:
            return False
            
        if not split:
            #print '[%s] Date has wrong format' % value
            return False

        d1 = int(split[0][0])
        d2 = int(split[0][1])
        d3 = int(split[0][2])
        if d1 >= 1000:
            # d1 is year
            if country == 'nl':        # d2 is month
                m = d2
                d = d3
            else:
                m = d3
                d = d2
        elif d3 >= 1000:
            # d3 is year
            if country == 'nl':        # d2 is month
                m = d2
                d = d1
            else:
                m = d1
                d = d2
        else:    # We don't support years < 1000
            #print '[%s] Year is out of range' % value
            return False
            
        if not (1 <= m <= 12):
            #print '[%s] Month is out of range' % value
            return False
            
        if not (1 <= d <= monthdays[m]):
            #print '[%s] Day is out of range for this month' % value
            return False

        return True
    
    @classmethod
    def isfuture(cls, value):
        """
            Answer true if value represents a date in the future
        
            >>> v = Validator()
            >>> v.isfuture('12/9/2013')
            True
            >>> v.isfuture('2013/10/21')
            True
            >>> v.isfuture('12/12/2513')
            True
            >>> v.isfuture('12/12/2001')
            False
            >>> v.isfuture('12/12/1399')
            False
            >>> v.isfuture('today')
            False
            >>> v.isfuture('')
            False
            >>> v.isfuture(None)
            False
        """
        if not value:
            return False
        return cls.isRange('today', -1, value)
        
    @classmethod
    def ispast(cls, value):
        """
            Answer true if value represents a date in the past
        
            >>> v = Validator()
            >>> v.ispast('12/9/1313')
            True
            >>> v.ispast('1313/10/21')
            True
            >>> v.ispast('12.1.1921')
            True
            >>> v.ispast('12/1/2040')
            False
            >>> v.ispast('12-01-2540')
            False
            >>> v.ispast('today')
            False
            >>> v.ispast('')
            False
            >>> v.ispast(None)
            False
        """
        if not value:
            return False
        return cls.isRange('today', value, 1)
        
    @classmethod
    def isBank(cls, s):
        """
        Testing if s is a valid bank number:
        - replace all "."
        - result should only by figures
        - total number of figures == 9
        
            >>> v = Validator()
            >>> v.isBank('66.76.65.195')
            True
            >>> v.isBank('667665195')
            True
            >>> v.isBank('6.6.7.6.6.5.1.9.5')
            True
            >>> v.isBank('66 76 65 195')
            False
            >>> v.isBank('66.76.65.1950')
            False
            >>> v.isBank('555')
            False
            >>> v.isBank('aaaaa')
            False
            >>> v.isBank('')
            False
            >>> v.isBank(None)
            False
        """
        if not s:
            return False
        si = s.replace('.', '')
        if not cls.isinteger(si):
            return False
        return len(si) == 9
    
    @classmethod    
    def isgiro(cls, s):
        """
        Testing if s is a valid giro number:
        - should only by figures
        - total number of figures < 9
        
            >>> v = Validator()
            >>> v.isgiro('66766519')
            True
            >>> v.isgiro('555')
            True
            >>> v.isgiro('66.76.65.195')
            False
            >>> v.isgiro('667665195')
            False
            >>> v.isgiro('66 76')
            False
            >>> v.isgiro('66.76.65.1950')
            False
            >>> v.isgiro('aaaaa')
            False
            >>> v.isgiro('')
            False
            >>> v.isgiro(None)
            False
        """
        if not cls.isinteger(s):
            return False
        return len(s) < 9
        
    @classmethod
    def isBankgiro(cls, s):
        """
        Testing if s is a valid giro number:
        - should only by figures
        - total number of figures < 10
        
            >>> v = Validator()
            >>> v.isBankgiro('667665195')
            True
            >>> v.isBankgiro('555')
            True
            >>> v.isBankgiro('66.76.65.195')
            True
            >>> v.isBankgiro('667665195')
            True
            >>> v.isBankgiro('66 76')
            False
            >>> v.isBankgiro('66.76.65.1950')
            False
            >>> v.isBankgiro('aaaaa')
            False
        """
        return cls.isBank(s) or cls.isgiro(s)
    
    @classmethod
    def findUrls(cls, s):
        """
            # Answer a list of all available urls in the s.
            
            >>> v = Validator()
            >>> v.findUrls('This is a text from http://www.apple.com containing valid urls http://www.petr.com, http://xyz.www.petr.com, and some more text and invalid url http://www.petr.c.')
            ['www.apple.com', 'www.petr.com', 'xyz.www.petr.com']
        """
        return re.findall(cls.URLPATTERN, s)
    
    @classmethod
    def isUrl(cls, s):
        """
            # Answer the boolean if this string is a valid url, with out without 'http://'
            
            >>> v = Validator()
            >>> v.isUrl('http://www.petr.com')
            True
            >>> v.isUrl('http://a.b.v.c.x.www.petr.com')
            True
            >>> v.isUrl('ttp://www.petr.com')
            False
            >>> v.isUrl('//www.petr.com')
            True
            >>> v.isUrl('www.petr.com')
            True
        """
        url = re.findall(cls.URLPATTERN, s)
        if bool(url and (cls.HTTP + url[0] == s)):    # Only true if exactly the same.
            return True
        # Try again, adding http:// to see if generates a valid url.
        s = cls.HTTP + s
        url = re.findall(cls.URLPATTERN, s)
        if bool(url and (cls.HTTP + url[0] == s)):    # Only true if exactly the same.
            return True
        return False
    
    @classmethod    
    def findEmails(cls, s):
        """
            # Answer a (validated) list of all available email addresses in the s.
            
            >>> v = Validator()
            >>> v.findEmails('This is a text from buro@petr123.com containing 3 valid (info@apple.com, p.vanblokland@petr.com) email addresses (and wrong xxx@petr.xyz not found)')
            ['buro@petr123.com', 'info@apple.com', 'p.vanblokland@petr.com']
        """
        validated = []
        for email in cls.ALLEMAILSPATTERNS.findall(s):
            if cls.isEmail(email):                                        # Do testing if this is a valid e
                validated.append(email)
        return validated

    @classmethod
    def isTwitter(cls, s):
        u"""
        Answer if s is a twitter address (starting with @)
        """
        return s and s.startswith('@')

    @classmethod
    def isEmail(cls, s):
        """
        Test if s is a valid email adres.
        Testing is done on:
        - pattern
        - Only one @
        - No characters > 127 in user
        - No characters > 127 in domain
        - Valid user name pattern
        - Valid ip number pattern
        - Valid domain name pattern
        
            >>> v = Validator()
            >>> v.isEmail('"aaa"@bbb123.com')
            True
            >>> v.isEmail('aaa@bbb.com')
            True
            >>> v.isEmail('aaa@www.bbb.com')
            True
            >>> v.isEmail('aaa@www.bbb.nl')
            True
            >>> v.isEmail('aaa.xxx@bbb.com')
            True
            >>> v.isEmail('buro@petr.com')
            True
            >>> v.isEmail('xxx-sss@abc.nl')
            True
            >>> v.isEmail('xxx-sss@100.100.100.100')
            True
            >>> v.isEmail('xxx-sss@abc.co')
            True
            >>> v.isEmail('xxx-sss@a.a.a.a.a.a.a.a.a.a.a.a.co')
            True
            >>> v.isEmail('~xxx._._._sss@a.a.a.a.a.a.a.a.a.a.a.a.co')
            True
            >>> v.isEmail('<xxx-sss@abc.nl>')
            False
            >>> v.isEmail('x###xx-sss@abc.nl')
            False
            >>> v.isEmail('xxx-sss@abc.nlxxxx')
            False
            >>> v.isEmail('xxx-sss@abc.55')
            False
            >>> v.isEmail('xxx-sss@abc.55')
            False
            >>> v.isEmail('xxx-sss@222.444.555.666')
            False
            >>> v.isEmail('xxx-sss@100,aaa,100,100')
            False
            >>> v.isEmail('')
            False
            >>> v.isEmail(None)
            False
        """
        if not s:                                                    # Some extra safety
            return False
        try:
            split = re.findall(cls.EMAILPATTERN, s)[0]
        except IndexError:
            #print '[%s] Wrong email pattern' % s                    # Totally wrong pattern
            return False
            
        if len(split) != 2:
            #print '[%s] Wrong @ pattern' % s
            return False
        user, domain = split

        for c in user:                                                # Test user name characters on > 127
            if ord(c) > 127:
                #print '[%s] User character > 127' % user
                return False
        for c in domain:
            if ord(c) > 127:                                        # Test domain name characters on > 127
                #print '[%s] Domain character > 127' % user
                return False

        u1 = re.findall(cls.QUOTEDUSERPATTERN, user)
        u2 = re.findall(cls.USERPATTERN, user)
        if not (u1 or u2):
            #print '[%s] Wrong user pattern' % user
            return False
            
        
        ip = re.findall(cls.IPPATTERN, domain)                        # Test on ip number and domain name
        if ip:                                                        # Test if values in ip address are valid
            for t in ip[0]:
                v = int(t)
                if not (0 <= v <= 255):
                    #print '[%s] Not within 0-255 range' % domain    # Values not within 0-255 range
                    return False
                    
        d = re.findall(cls.DOMAINPATTERN, domain)        
        if not (ip or d):
            #print '[%s] Wrong domain pattern' % user
            return False
                
        return True
    
    @classmethod            
    def isZipcode(cls, value, country = 'nl'):
        """
        Test if the value is a valid zipcode
        
            >>> v = Validator()
            >>> v.isZipcode('1234 AB')
            True
            >>> v.isZipcode('3333XX')
            True
            >>> v.isZipcode('123XX')
            False
            >>> v.isZipcode('1234 XXX')
            False
            >>> v.isZipcode('sdsdsd')
            False
            >>> v.isZipcode('123 4')
            False
            >>> v.isZipcode('3232##')
            False
            >>> v.isZipcode('')
            False
            >>> v.isZipcode(None)
            False
        """
        if not value:
            return False
        return re.findall(cls.ZIPCODEPATTERNS[country], value) != []
        
    @classmethod
    def isTelephone(cls, value, country = 'nl'):
        """
        Test if the value is a valid telephone number
        
            >>> v = Validator()
            >>> v.isTelephone('1234567898')
            True
            >>> v.isTelephone('1 23 23 23 444')
            True
            >>> v.isTelephone('       1 23 23 23 444')
            True
            >>> v.isTelephone('+31 15 219 10 40')
            True
            >>> v.isTelephone('   +31 15 219 10 40   ')
            True
            >>> v.isTelephone('1 23----------- 23 23 444')
            True
            >>> v.isTelephone('sdsdsd')
            False
            >>> v.isTelephone('123 4')
            False
            >>> v.isTelephone('3232##')
            False
            >>> v.isTelephone('')
            False
            >>> v.isTelephone(None)
            False
        """
        if not value:
            return False
        return re.findall(cls.TELEPHONEPATTERNS[country], value) != []


if __name__ == "__main__":
    import doctest
    doctest.testmod()
