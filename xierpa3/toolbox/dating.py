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
#    dating.py
#
import datetime
from time import localtime
from random import randint
import re

def uniqueLong():
    u"""
    
    The <code>uniqueLong</code> method answers a unique number (as string) of 18 digits.
    
    """
    return DateTime.timestamprandomlong()

def timestampLong():
    u"""
    
    The <code>timestampLong</code> method answers the timestamp. This may not be unique.
    
    """
    return DateTime.timestamplong()

def uniqueId(size=0):
    u"""
    
    The <code>uniqueId</code> method answers a unique number (as string) of <attr>size</attr> length concatenated
    timestamps. Minimum length of the number is 18 digits, or else string will not be unique.
    
    """
    n = ''
    size = max(size,18)
    while len(n) < size:
        n += str(uniqueLong())
    return n[:size]

def leapyear(year):
    #most common first
    if year % 4 != 0:
        return False

    if year % 400 == 0:
        return True

    if year % 100 == 0:
        return False

    return True

def monthdays(year, month):
    # Separate method, so it also can be used on initialization
    if month == 2:
        if leapyear(year):
            return 29
        else:
            return 28
    elif month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    else:
        return 30

def checkdatetime(date):
    u"""
    
    The <code>checkdatetime</code> answers the <attr>date</attr> if it is a date. If date is None, then answer None. If
    date is a string, then convert to DateTime. Check on the month and day boundaries. Answer the same type that date
    was. Note that we do not check if date was already a DateTime. This method is especially made to set database fields
    with dates, where that None will result in a NULL value for that field.
    
    """
    if not date: # Check on None or empty string
        return None
    if not isinstance(date, DateTime):
        return DateTime(date=date).date
    return date

def newdatetime(date):
    u"""
    The <code>newdate</code> method answers a new <code>DateTime</code> instance. If the <attr>date</attr> is
    <code>None</code>, then answer <code>None</code>. If <attr>date</attr> is a string, then convert to
    <code>DateTime</code>. Check on the month and day boundaries.<br/>
    
    """
    if date is None:
        return None
    if not isinstance(date, DateTime):
        date = DateTime(date=date)
    return date

class Duration:
    u"""
    
    The <code>Duration</code> class contains a duration in time. It can e.g. be used to add to a <code>DateTime</code>
    instance with a new date as result.<br/>
    <python>
    Duration(3)<br/>
    Duration(seconds=10)<br/>
    Duration(td=timedelta)<br/>
    </python>
    All common arithmetic applies to a <code>Duration</code> instance. 
    <python>
    d = Duration(3)<br/>
    d * 3 is a duration of 6 days.<br/>
    </python>
    
    """

    #hack months and larger onto datetime.timedleta, which only goes up to weeks
    months = None
    timedelta = None
    
    def __init__(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, months=0, years=0, decades=0, centuries=0, millenia=0, td=None):
        u"""
        
        An extension of the builtin datetime.timedelta class, extending to millenia to match SQL's INTERVAL type
        Note that by itself, a duration of months is meaningless due to diffing month lengths.
        But when doing date arithmetic, we can figure it out.
        
        """
        #convert everything larger than months into months
        self.months = float(months + years*12 + decades*120 + centuries*1200 + millenia*12000)

        if td is not None:
            self.timedelta = td
        else:
            self.timedelta = datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)

    def __getattr__(self, key):
        if key in ('days','seconds','microseconds'):
            return getattr(self.timedelta,key)
        return self.__dict__[key]

    def __len__(self):
        return self.days

    def __str__(self):
        return `self`

    def __repr__(self):
        #repr must return ascii, so no µ for you!
        return u'Duration(%fm,%dd,%ds,%dus)' % (self.months, self.days, self.seconds, self.microseconds)

    # To be added __iter__

    def __coerce__(self, p):
        return None

    def __nonzero__(self):
        return self.months or self.days or self.seconds or self.microseconds 

    def __eq__(self, other):
        if not isinstance(other,Duration):
            return False
        
        return self.months==other.months and self.days==other.days and self.seconds==other.seconds and self.microseconds==other.microseconds

    def __ne__(self,other):
        return not self.__eq__(other)

    def __mul__(self, n):
        return Duration(months=self.months * n, days=self.days * n, seconds=self.seconds * n, microseconds=self.microseconds * n)

    def __div__(self, n):
        return Duration(months=self.months / n, days=self.days / n, seconds=self.seconds / n, microseconds=self.microseconds / n)

    def __neg__(self):
        return self * -1;

    def __add__(self, value):
        # Duration + Date = Date
        # Duration + Duration = Duration
        # Duration + 3 = Duration
        if isinstance(value, (int, long)):
            return self + Duration(days=value)

        if isinstance(value, Duration):
            return Duration(months=self.months + value.months, days=self.days + value.days, seconds=self.seconds + value.seconds, microseconds=self.microseconds + value.microseconds)

        if isinstance(value, DateTime):
            #need to do some magic to take into account leap years etc
            extradays = 0
            import math

            if self.months > 0:
                othermonth = value.month
                otheryear = value.year
                monthselapsed = 0
                
                intmonths = math.floor(self.months)
                decmonths = self.months-intmonths;
                
                while monthselapsed < intmonths:
                    extradays += monthdays(otheryear,othermonth)

                    othermonth += 1
                    if othermonth > 12:
                        othermonth = 1
                        otheryear += 1
                    monthselapsed += 1

                extradays += decmonths * 30 #arbitrarily picking 30 days for fractional months

            elif self.months < 0:
                othermonth = value.month
                otheryear = value.year
                monthselapsed = 0
                
                intmonths = math.floor(abs(self.months))
                decmonths = abs(self.months)-intmonths;
                
                while monthselapsed < intmonths:
                    othermonth -= 1
                    if othermonth < 1:
                        othermonth = 12
                        otheryear -= 1
                    monthselapsed += 1
                     
                    extradays += monthdays(otheryear,othermonth)

                extradays += decmonths * 30 #arbitrarily picking 30 days for fractional months

                extradays = -extradays                

            if extradays:
                return DateTime(dt=value.datetime + datetime.timedelta(days=extradays) + self.timedelta)
            else:                
                return DateTime(dt=value.datetime + self.timedelta)
        raise ValueError('[Duration.__add__] Illegal type to add to a Duration instance "%s"' % value)

    def __sub__(self, dt):
        # Duration - Date = Date
        # Duration - Duration = Duration
        # Duration - 3 = Duration
        if isinstance(dt, (int, long, Duration)):
            return self + -dt

        if isinstance(dt, DateTime):
            return dt + -self

        raise ValueError('[Duration.__add__] Illegal type to subtract from a Duration instance "%s"' % dt)

    def __iadd__(self, item):
        return self + item

    def __isub__(self, item):
        return self - item

    def __imul__(self, item):
        return self * item

    def __idiv__(self, item):
        return self / item

    def min(self):
        u"""
        
        Most negative timedelta object that can be represented.
        
        """
        return datetime.timedelta.min

    def max(self):
        u"""
        
        Most positivie timedelta object that can be represented.
        
        """
        return datetime.timedelta.max

    def resolution(self):
        u"""
        
        Smallest resolvable difference that a timedelta object can represent.
        
        """
        return datetime.timedelta.resolution

Period = Duration    # Make the lib backward compatible. But the use of Period is supported.

class DateTime:
    u"""
    
    The <code>newdate</code> method answers a new <code>DateTime</code> instance. If the <attr>date</attr> is
    <code>None</code>, then answer <code>None</code>. If <attr>date</attr> is a string, then convert to
    <code>DateTime</code>. Check on the month and day boundaries.<br/>
    <list>
        <li>Initialize the current date if the <attr>date</attr> is equal to <code>now</code></li>
        <li>Initialize on first day of the week if year and week are defined</li>
        <li>Initialize from existing datetime if "dt" is defined</li>
        <li>Initialize from <attr>date_time</attr> string, date and time separated by white space.</li>
        <li>Initialize from <attr>date</attr> string (identical to the result of self.date) if defined</li>
        <li>Initialize from <attr>time</attr> string (identical to the result of self.time) if defined</li>
        <li>Initialize from (year, month, day) if all of them are defined.</li>
        <li>Otherwise raise an error</li>
    </list>
    If the <attr>trimvalues</attr> attribute is set to <code>False</code> (default is <code>True</code>) then the
    input values of the date are <em>not</em> trimmed to their minimum and maximum values. This checking is done in
    context for days in months and years.<br/>
    <python>
    DateTime(date='now')
    DateTime(date='2008-11-23')
    DateTime(date='2008-11-23', time='23:11')
    DateTime(date='2008-11-23', time='23:11:22')
    DateTime(2008, 11, 23)
    DateTime(2008, 11, 23, 23, 11, 22, 0)
    DateTime(2008, week=23)
    </python>
    
    """
    keys = {'year': 0, 'month': 1, 'day': 2, 'hour': 3, 'minute': 4, 'second': 5, 'weekday': 6, 'yearday': 7, 'tz': 8}
    daynames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fulldaynames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    monthnames = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fullmonthnames = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    def __init__(self, year=None, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tz=None,
        dt=None, date_time=None, date=None, time=None, week=None, trimvalues=True, mtime=None):

        if dt is not None:
            # Assume that dt is of type date string. Direct init from existing datetime
            self.datetime = dt
        else:
            if date == 'now' or date_time == 'now':
                self.datetime = datetime.datetime.now()
                return

            if date_time is not None:
                date_time = str(date_time) # In case of a datetime instance from Django
                datetimeparts = date_time.split(' ')
                date = datetimeparts[0].strip()
                time = datetimeparts[1].strip()

            if date is not None:
                if isinstance(date, (basestring, unicode)):
                    # Could one of the follovwing formats
                    # YYYY-MM-DD HH:MM:SS                    
                    stamp = re.compile("(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)([\-\+]\d+)?")
                    m = stamp.match(date)
                    if m:
                        year = int(m.group(1))
                        month = int(m.group(2))
                        day = int(m.group(3))
                        hour = int(m.group(4))
                        minute = int(m.group(5))
                        second = int(m.group(6))
                        #@# tz must be a tzinfo object, not an integer, leave it as None for now.
                        #tz = int(m.group(7) or tz)
                    else:
                        try:
                            if '.' in date or '/' in date:
                                date = date.replace('.', '-').replace('/', '-')
                            date = date.split(' ')[0]    # Skip possible time part of date input
                            year, month, day = date.split('-')
                            if int(day) > int(year):    # If notation 25-03-2007, then swap day and year
                                year, day = day, year
                        except:
                            raise ValueError('[DateTime] Wrong date format "%s"' % date)
                else:
                    # If date is an integer .... format: YYYYMMDD
                    d = str(date)
                    year, month, day = d[:4], d[4:6], d[6:]

            if mtime is not None:
                # Evaluate the number of seconds since the beginning of time
                tt = localtime(mtime)
                year = tt.tm_year
                month = tt.tm_mon
                day = tt.tm_mday
                hour = tt.tm_hour
                minute = tt.tm_min
                second = tt.tm_sec
                
            if time is not None:
                time = time.split(' ')[-1]    # Skip possible date part of the time input
                timeparts = time.split(':')
                if len(timeparts) == 2:
                    hour, minute = timeparts
                    second = 0
                elif len(timeparts) == 3:
                    hour, minute, second = timeparts
                    if '.' in second:
                        second, microsecond = second.split('.',1)
                        if len(microsecond) < 6:
                            microsecond += '0' * (6-len(microsecond))

            if year is not None and week is not None:
                week = int(week)
                # Set date of first day in the requested week
                dt = datetime(int(year), 1, 1) + datetime.timedelta(weeks=week)
                self.datetime = dt - datetime.timedelta(days=dt.timetuple()[self.keys['weekday']])
                # This algorithm may be one week off, so test and adjust if it does not match.
                if self.week > week:
                    self.datetime -= datetime.timedelta(days=7)

            elif year is None or month is None or day is None:
                if time is not None:
                    # Just a time was specified, 
                    year = month = day = 0
                else:
                    raise ValueError('[DateTime] Did not supply all values of y,m,d (%s,%s,%s)' % (year, month, day))

            elif trimvalues:
                year          = int(year)
                month          = min(12, max(1, int(month)))
                day          = min(monthdays(year, month), max(1, int(day)))
                hour          = min(23, max(0, int(hour)))
                minute          = min(60, max(0, int(minute)))
                second         = min(60, max(0, int(second)))
                microsecond     = min(99, max(0, int(microsecond)))
                self.datetime = datetime.datetime(year, month, day, hour, minute, second, microsecond, tz)
            else:
                self.datetime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second),
                                                int(microsecond), tz)

    def __getattr__(self, key):
        if key in self.keys:
            # year, month, day, hour, minute, second, weekday, yearday
            return self.datetime.timetuple()[self.keys[key]]

        method = '_' + key
        if hasattr(self, method):
            return getattr(self, method)()

        return self.__dict__[key]

    def __str__(self):
        u"""
        
        The function <code>str(dt)</code> answers the string representation of the date. Typically the identical to
        <code>dt.date + ' ' + dt.time</code>.
        
        """
        return `self`

    def __repr__(self):
        u"""
        
        The function <code>repr(dt)</code> (or <code>`dt`</code>) answers the string representation of the date,
        typically identical to <code>dt.date + ' ' + dt.time</code>.
        
        """
        return self.date + ' ' + self.time

    def __nonzero__(self):
        u"""
        
        Always answer <code>True</code> indicating that a <code>DateTime</code> instance can never be zero.
        
        """
        return True

    def __lt__(self, dt):
        u"""
        
        Answers <code>True</code> if <code>self</code> is in the past of date <code>dt</code> as in <code>self &lt; dt</code>.<br/>
        Note that in evaluating the condition the difference in time is taken into account as well.<br/>
        Use <code>self.datenumber &amp;lt; dt.datenumber</code> to test on date comparison only instead of <code>dy &amp;lt; self</code>.</br>
        
        """
        return self.datetime < dt.datetime

    def __le__(self, dt):
        u"""
        
        Answers <code>True</code> if <code>self</code> is in the past of or equal to date <code>dt</code> as in <code>self &lt;=< dt/code>.<br/>
        Note that in evaluating the condition the difference in time is taken into account as well.<br/>
        Use <code>self.datenumber &amp;lt; dt.datenumber</code> to test on date comparison only instead of <code>dy &amp;lt;= self</code>.</br>
        
        """
        return self.datetime <= dt.datetime

    def __gt__(self, dt):
        return self.datetime > dt.datetime

    def __ge__(self, dt):
        return self.datetime >= dt.datetime

    def __ne__(self, dt):
        return not self == dt

    def __eq__(self, dt):
        if isinstance(dt, DateTime):
            return self.datetime == dt.datetime
        return False

    def __coerce__(self, duration):
        return None

    def __iadd__(self, item):
        return self + item

    def __isub__(self, item):
        return self - item

    def __add__(self, duration):
        u"""
        
        Add the <attr>duration</attr> to <code>self</code>.
        <python>
        Date + Duration = Date
        Date + 3 = Date
        </python>
        
        """
        if isinstance(duration, (int, long, float)):
            duration = Duration(days=duration)
        assert isinstance(duration, Duration)
        return Duration.__add__(duration,self)

    def __sub__(self, durationordate):
        u"""
        
        <python>
        Date - Duration = Date<br/>
        Date - Date = Duration<br/>
        Date - 3 = Date<br/>
        
        """
        if isinstance(durationordate, (int, long, float)):
            durationordate = Duration(days=durationordate)
        if isinstance(durationordate, Duration):
            # Date - Duration = Date
            return Duration.__sub__(durationordate,self)
        if isinstance(durationordate, DateTime):
            # Date - Date = Duration
            return Duration(td=self.datetime - durationordate.datetime)

    @classmethod
    def timestamprandomlong(cls):
        u"""
        
        The <code>_uniquenumber</code> method/attributes answers a unique number of format <code>'20090621200511993066'</code>, 
        derived from date, time and a six digit random number. This can be used e.g. in a URL as parameters to make sure that browser 
        will not cache the content of the page. The number is also used to create a unique file name for background shell scripts.
        
        """
        return cls.timestamplong() + ('%06d' % randint(0, 999999))
    
    @classmethod    
    def timestamplong(cls):
        import time
        return '%012d' % int(time.time()*100)

    def _timestamp(self, usetz=False):
        u"""
        
        The <code>dt.timestamp</code> answers a formatted string <code>2010-10-05 16:47:29+o4</code> of the date. This
        is exactly what SQL needs as timestamp with time zone definition.<br/>
        <note>use of tz does not yet work, and is ignored</note>
        
        """
        if self.tz is None or not usetz:
            tz = ""
        elif self.tz < 0:
            tz = "-%02d" % -self.tz
        else:
            tz = "+%02d" % self.tz
        return  "%s %s%s" % (self.date, self.time, tz)

    def _date(self):
        u"""
        
        The <code>dt.date</code> answers a formatted string <code>2008-10-23</code> of the date.
        This is exactly what SQL needs as date-string definition.
        
        """
        return '%04d-%02d-%02d' % (self.year, self.month, self.day)

    def _eurodate(self):
        u"""
        
        The <code>dt.eurodate</code> answers a formatted string <code>23-10-2008</code> of the date.
        
        """
        return '%02d-%02d-%02d' % (self.day, self.month, self.year)

    def _studyyear(self):
        u"""
        
        The <code>dt.studyyear</code> method/attribute answers a string <code>0708 with leading zero for the study year
        from <code>2007-08-01</code> until <code>2008-07-31</code>
        
        """
        studyyear = (self.year - 2000) * 100 + self.year - 2000 + 1
        if self.month <= 8: # Switch study year on end of summer break
            studyyear -= 101
        return '%04d' % studyyear

    def _datenumber(self):
        u"""
        
        The <code>dt.datenumber</code> method/attribute answers a long integer number 20080502 of the date. This can by
        used to compare dates on day only and not on time. Or it can be used as ordering key.
        
        """
        return self.year * 10000 + self.month * 100 + self.day

    def _datetuple(self):
        u"""
        
        The <code>dt.datetuple</code> method/attribute answers a tuple <code>(y,m,d)</code> of the date.
        
        """
        return self.year, self.month, self.day

    def _time(self):
        u"""
        
        The <code>dt.datenumber</code> method/attribute answers a formatted <code>'12:23:45'</code> time string.
        
        """
        return '%02d:%02d:%02d' % (self.hour, self.minute, self.second)

    def _date_time(self):
        u"""
        
        The <code>dt.date_time</code> method/attribute answers a formatted <code>'2010-12-06 12:23:34'</code> date/time
        string.
        
        """
        return '%s %s' % (self.date, self.time)

    def _timetuple(self):
        u"""
        
        The <code>dt.timetuple</code> method/attribute answers a tuple <code>(h, m, s)</code> of the time.
        
        """
        return self.hour, self.minute, self.second

    def _timezone(self):
        u"""
        
        The <code>dt.timezone</code> method/attribute answers the timezone <code>dt.tz</code>.
        
        """
        return self.tz

    def _week(self):
        u"""
        
        The <code>dt.week</code> method/attribute answers the weeknummer according to ISO 8601 where the first week of
        the year that contains a thursday.
        
        """
        return self.datetime.isocalendar()[1]

    def _dayname(self):
        u"""
        
        The <code>dt.dayname</code> method/attribute answers a 3 letter abbreviation of current day name. 
        
        """
        return self.daynames[self.weekday]

    def _fulldayname(self):
        u"""
        
        The <code>dt.fulldayname</code> method/attribute answers the full name of the current day. 
        
        """
        return self.fulldaynames[self.weekday]

    def _monthname(self):
        u"""
        
        The <code>dt.monthname</code> method/attribute answers a 3 letter abbreviation of current month name. 
        
        """
        return self.monthnames[self.month]

    def _fullmonthname(self):
        u"""
        
        The <code>dt.fullmonthname</code> method/attribute answers the full name of the current month. 
        
        """
        return self.fullmonthnames[self.month]

    def _monthstart(self):
        u"""
        
        The <code>dt.monthstart</code> method/attribute answers the first day of the current month.    
        
        """
        return self + (1 - self.day) # Keep integer calculation combined by brackets

    def _monthend(self):
        u"""
        
        The <code>dt.monthend</code> method/attribute answers the last day of the current month.    
        
        """
        return self - self.day + self.monthdays

    def _weekstart(self):
        u"""
        
        The <code>dt.weekstart</code> method/attribute answers the “Monday” date of the current week.
        
        """
        return self - self.weekday

    def _weekend(self):
        u"""
        
        Keep integer calculation combined by brackets
        
        """
        return self + (7 - self.weekday)

    def _yearstart(self):
        u"""
        
        The <code>dt.yearstart</code> method/attribute answers the first day of the current year.    
        
        """
        return DateTime(self.year, 1, 1)

    def _yearend(self):
        u"""
        
        The <code>dt.yearend</code> method/attribute answers the last day of the current year.    
        
        """
        return DateTime(self.year, 12, 31)

    def _workday(self):
        u"""
        
        The <code>dt.workday</code> method/attribute answers <code>True</code> if this day is one of Monday till Friday.
        
        """
        return 0 <= self.weekday <= 4

    def _nextworkday(self):
        u"""
        
        The <code>dt.nextworkday</code> method/attribute answers the first next date (including itself) that is a
        workday
        
        """
        if self.workday:
            return self
        return self + (7 - self.weekday) # Keep integer calculation combined by brackets

    def _leapyear(self):
        u"""
        
        The <code>dt.leapyear</code> method/attribute answers a boolean if the <code>dt</code> is a leap year.
        
        """
        return leapyear(self.year)

    def _yeardays(self):
        u"""
        
        The <code>dt.yeardays</code> method/attribute answers the number of days in the current year.
        
        """
        if leapyear(self.year):
            return 366
        return 365

    def _monthdays(self):
        u"""
        
        The <code>dt.monthdays</code> method/attribute answers the number of days in the current month.
        
        """
        return monthdays(self.year, self.month)

    def _nextmonth(self):
        u"""
        
        The <code>nextmonth</code> method/attribute answers the first day of the month after the current month. Due to
        length differences between the months, it is not consistent to answer the current day number in the next month,
        so it is set to 1.
        
        """
        return self + (self.monthdays - self.day + 1)

    def _prevmonth(self):
        u"""
        
        The <code>prevmonth</code> method/attribute answers the first day of the month previous to the current month.
        Due to length differences between the months, it is not consistent to  answer the current day number in the
        previous month
        
        """
        return (self.monthstart - 1).monthstart

    def _calendarmonth(self):
        u"""
        
        The <code>calendarmonth</code> method/attribute answers a list of lists containing the weeks with dates of the
        current month. Note that the first and lost week are filled with the days of end of the previous month and the
        start of the next month.<br/>
        <python>
            [<br/>
                [p01, p02, p03, d01, d02, d03, d04],<br/>
                [d05, d06, d07, d08, d09, d10, d11],<br/>
                [d12, d13, d14, d15, d16, d17, d18],<br/>
                [d19, d20, d21, d22, d23, d24, d25],<br/>
                [d26, d27, d28, d29, d30, n01, n02]<br/>
            ]<br/>
        </python>
        
        """
        monthweekdates = []
        weekstart = self.monthstart.weekstart
        running = False
        while not running or weekstart.month == self.month:
            weekdates = []
            monthweekdates.append(weekdates)
            for day in range(7):
                weekdates.append(weekstart + day)
            weekstart += 7
            running = True
        return monthweekdates

    def _calendaryear(self):
        u"""
        
        The <code>calendaryear</code> method/attribute answers a list of lists of lists containing all
        <code>calendarmonths</code> of the year.<br/>
        <python>
            [<br/>
            [<br/>
                [p01, p02, p03, d01, d02, d03, d04],<br/>
                [d05, d06, d07, d08, d09, d10, d11],<br/>
                [d12, d13, d14, d15, d16, d17, d18],<br/>
                [d19, d20, d21, d22, d23, d24, d25],<br/>
                [d26, d27, d28, d29, d30, n01, n02]<br/>
            ]<br/>
            [<br/>
            ...<br/>
            ]<br/>
            ...<br/>
            ]<br/>
        </python>
        
        """
        yearweekdates = []
        for month in range(1, 13):
            yearweekdates.append(DateTime(year=self.year, month=month, day=1).calendarmonth)
        return yearweekdates

    def nextdaynamed(self, weekday):
        if not (0 <= weekday <= 7):
            raise ValueError('[DateTime.nextdaynamed] Weekday "%s" must be in range (0, 8)' % weekday)
        nextday = self + Duration(days=1)
        while 1:
            if nextday.weekday == weekday:
                return nextday
            nextday = nextday + Duration(days=1)
        return None

if __name__ == "__main__":
    #d1 = DateTime(date='now')
    #d2 = DateTime(year=2008, month=2, day=10)
    #print d1 + Duration(123)
    #print d1.assecond()
    #print d1 - Duration(days=2)
    p = Duration(seconds=10) * 6 / 2
    print 'Duration', p,
    print 'Negated duration', -p
    print 'Duration 1 day longer', p + 1
    print 'Duration 2 minutes longer', p + Duration(minutes=2)
    d1 = DateTime(date='now')
    d2 = d1 + Duration(seconds=10)

    print d1.weekday, d1.dayname
    print d1.month, d1.monthname
    print d1.week, d2.week
    print 'Next working day', d1.nextworkday
    print d1
    print d1 + p
    print '6 days later', d1 + 6
    print '60 days later', d1 + 60
    print 'First work day after 60 days', (d1 + 60).nextworkday
    print '20 days earlier', d1 - 20
    print d1 - p
    print d1 - d2 + d2
    print d1.date
    print d1.datenumber
    print d1.datetuple
    print d1.time
    print d1.timetuple
    print d1.nextdaynamed(5).dayname
    print d1.nextdaynamed(5).nextworkday.dayname
    print d1.nextdaynamed(6).nextworkday.dayname
    print d1.leapyear
    d3 = DateTime(2007, 12, 20)
    print d3.nextmonth
    d3 = DateTime(2008, 1, 15)
    print d3.prevmonth
    print d3 - d1
    d3 = DateTime(d1.year, d1.month, 1)
    print d3 + Duration(days=d3.monthdays - 1)
    print d1.monthstart, d1.monthend
    print d1 - Duration(days=1)
    print 'First week of this month', DateTime(date='2007-12-10').monthstart.week
    print 'Date of start of first week of this month', DateTime(date='2007-12-10').monthstart.weekstart
    print 'Previous month of 2007-12-10 is', DateTime(date='2007-12-10').prevmonth.date
    print 'Previous month of 2008-1-10 is', DateTime(date='2008-1-10').prevmonth.date
    print 'Next month of 2007-12-10 is', DateTime(date='2007-12-10').nextmonth.date
    print 'Next month of 2008-1-10 is', DateTime(date='2008-1-10').nextmonth.date
    print 'First day of third week', DateTime(year=2008, week=2).date
    print 'Trim day value', DateTime(year=2008, month=2, day=35).date
    print 'Trim month and day value', DateTime(year=2008, month=22, day=35).date
    print 'Year start and end', d1.yearstart.date, d1.yearend.date
    print 'Month start and end', d1.monthstart.date, d1.monthend.date
    print d1.calendarmonth
    print DateTime(date='2008-2-29').calendarmonth
    print DateTime(date='2007-12-31').calendaryear
