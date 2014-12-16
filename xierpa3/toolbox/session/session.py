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
#       session.py
#
#    SessionManager works similar to Cache (which is size limited), but it is
#    time limited instead.
#    If size of the cache runs over MAXCACHE then check on all existing
#    cache entries if their date is expired. If it is, then delete the entry.
#    This way we only will only do garbage collection once in a while and
#    not on every approach.
#
#    The SessionManager handles the virtual storage place for information 
#    during a client session to keep information available between a sequence
#    of page queries.
#    All sessions are kept for as long as the expire times indicates (in seconds)
#    The default expiration time is 4 hours.
#    In principle sessions are publicly stored. But since the key is a number
#    with a significant large key size it is very unlikely that another client
#    is able to find the right key with its lifespan.
#    
#    session.new()                                                Create a new session and answers a unique identifier and expire of 4 hours
#    session.new(3600, 'name of the session', 'guest')            Create a new session with name/user and a life span of one hour
#    session.delete(id)                                            Delete session with id    
#
from time import time
import pickle
from xierpa3.constants.constants import Constants

class Session:
    
    C = Constants
    
    def __init__(self, key, timestamp, limit=None, name=None, user=None, keep=False, protected=False):
        #
        #    Defaults:
        #    limit        SESSION_EXPIRETIME (1 hour)
        #    name        'Session'
        #    user        'guest'
        #
        #    Xierpa applications will add a xierpa instance to session to make it invisible
        #    from the parameter side. Thus is cannot accidentically be overwritten by a parameter
        #    with the name xierpa.
        #
        #    Add a timestamp part to the session at the time it is created. This way we have a safe
        #    value to set to the “inuseby” field of records, which does both better sorting and protecting records
        #    from being open by multiple editors at the same time.
        #
        self.protected = protected # If True, then the content of e.form it not copied to self
        self.key = key # Store original key
        self.timestamp = timestamp # Time based + random unique id for each session, different per session version.
        self.data = {self.C.PARAM_SID: key,     # Always store session key and timestamp in data set, so it will show
            'timestamp': self.timestamp, # and be saved in a server halt-start
        }
        self.limit = limit or self.C.SESSION_SESSIONEXPIRATIONTIME    # Remember the original limit, so we can extend with the same amount. Default is 1 hour.
        self.name = name or 'Session' # Store an optional name for this session (e.g. storage for a connected url)
        self.user = user or 'guest' # Store user name in the session
        self.refresh() # Set expire time for this session

    def __repr__(self):
        return self.show()

    def show(self):
        t = ['''<table>
            <tr><td align="left" valign="top"><span class="em">Session:</span></td><td>%s</td></tr>
            <tr><td align="left" valign="top"><span class="em">Name:</span></td><td>%s</td></tr>
            <tr><td align="left" valign="top"><span class="em">Expire:</span></td><td>%s</td></tr>''' % \
                (repr(self.key), repr(self.name), repr(self.expireTime()))]
        fields = self.data.keys()
        fields.sort()
        for field in fields:
            t.append('<tr><td align="left" valign="top"><span class="em">%s:</span></td><td>%s</tr>' % (field, repr(self.data.get(field))))
        t.append('</table>')
        return ' '.join(t)

    def __setitem__(self, field, item):
        # TODO: flag as dirty
        self.refresh()
        self.data[field] = item

    def __getitem__(self, field):
        try:
            self.refresh()
            return self.data.get(field)
        except KeyError:
            return None

    def __delitem__(self, key):
        if self.data.has_key(key):
            del self.data[key]

    def get(self, field):
        # Make session compatible with dicts
        return self[field]
    
    def clear(self):
        u"""
        
        The <code>clear</code> method clears all session data, while keeping the instance working.
        This e.g. can be used when the user is logging out, and all previous data should be cleared.
        
        """
        self.key = 0
        self.data = {}
        
    def asString(self):
        t = ['[Session(%s) Name: %s, Expire: %s, Backtrack: %s, Keep: %s]' % \
            (repr(self.key), repr(self.name), repr(self.expireTime()), repr(self._backtrack), repr(self._keep))]
        for dataset in [self.data[-1]]:
            fields = dataset.keys()
            fields.sort()
            for field in fields:
                t.append('%s: %s\n' % (field, repr(dataset[field]).encode('UTF-8')))
        return ', '.join(t)

    def initialize(self, form=None):
        #
        #    Re-initialize the session as it was when it was created.
        #
        self.__init__(self.key, self.limit, self.name, self.user, self._backtrack, self._keep)
        if form is not None:
            self.append(form)

    def getSid(self):
        return self.key

    def getExpirationTime(self):
        return self.limit

    def setData(self, d):
        self.data = [d]
        self.refresh()

    def set(self, field, value):
        #
        #    Equivalent of "session[key] = value" but "session.set(key, value)" is more clear
        #    to be used as side-effect scripts in attributes. The value is answered.
        #
        self[field] = value
        return value

    def default(self, field, value):
        u"""
        
        The <code>default</code> method sets the value of <attr>field</attr> to <attr>value</attr>
        only if the current value is <code>None</code>. This way the method can be used to compact
        initialize the value of a session field.
        
        """
        if self[field] is None:
            self[field] = value

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()

    def keys(self):
        return self.data.keys()

    def has_key(self, field):
        return self.data.has_key(field)

    __contains__ = has_key

    def cleanUp(self):
        """ 
        Clean up the session for objects that can't be cpickled: 
        1. parsed node trees with weakrefs cannot be cpickled;
        
        python v 2.4 raises a TypeError instead of pickle.UnpickleableError, so catch this exception
        
        >>> from xpyth.xmlparser import XMLParser
        >>> parsed_xml = XMLParser().parse('<a><b>c</b></a>')
        >>> parsed_xml
        <a No parent >
        >>> s = Session('1234')
        >>> s.set('nodewithweakparent', parsed_xml)
        <a No parent >
        """

        for d in self.data:
            for key, value in d.items():
                try:
                    pickle.dumps(value, 1)
                except (pickle.UnpickleableError, pickle.PicklingError, TypeError, KeyError): #@UndefinedVariable
                    del d[key]

    def append(self, form):
        #
        #    Append a form to the this session
        #    Skip writing of SESSION_ID as field, since this is not allowed
        #
        #    Check on fields that have a single "__checkbox__" value. These
        #    are flags for missing (unchecked) checkboxes. If we find such a 
        #    value, then reset the value of the same name in this session
        #    If the value if a list/tuple and it contains "__checkbox__" then
        #    the checkbox was set. Remove the marker and update the session
        #    with the remaining list.
        #    Example from xierpa/ultralite.xsl:
        #     
        #     <xhtml:input type="hidden" name="xpyth:'xierpa_field_' + e.attr('xmlnode', 'name')" value="__checkbox__"/>
        #     <xhtml:input type="checkbox"
        #         checked="xpyth:e.attr('eachnode', e.attr('xmlnode', 'name')) == e.attr('xmlnode', 'truevalue')"
        #         name="xpyth:'xierpa_field_' + e.attr('xmlnode', 'name')"
        #         value="xpyth:e.attr('xmlnode', 'truevalue')"/>
        #     
        #
        #    Otherwise just replace the content of the session[field] by the form value
        #
        if form:
            self.refresh()
            for field in form.keys():
                if field == self.C.PARAM_SID:        # Never overwrite local sessions id
                    continue
                self[field] = form[field]

    def anyExists(self, fields, matchvalues=[None]):
        #
        #    If one or more of the fields exist in the session, then answer true
        #    Else answer false. Remove any spaces between the fieldnames and comma's
        #    Matchvalues is a list of values that behave as non-existing
        #
        #    Example: rq.session.anyexists('aa, bb, cc')
        #
        self.refresh()
        for field in fields.split(','):            # Split "aa, bb, cc, dd" into a list of field names
            if self[field.strip()] not in matchvalues:
                return True                        # This fields exists. We are satisfied
        return False                            # Did not find any existing field

    def allExist(self, fields, matchvalues=[None]):
        #
        #    If all of the fields exist in the session, then answer true
        #    Else answer false. Remove any spaces between the fieldnames and comma's
        #    Matchvalues is a list of values that behave as non-existing
        #
        #    Example: rq.session.allexist('aa, bb, cc', ['0', 0, '', None])
        #
        self.refresh()
        for field in fields.split(','):            # Split "aa, bb, cc, dd" into a list of field names            
            if self[field.strip()] in matchvalues:
                return False                    # This fields exists. We are satisfied
        return True                                # Did not find any existing field

    def refresh(self):
        #
        #    Update refresh time.
        #
        self.expire = int(time() + self.limit)

    def expireTime(self):
        #
        #    !!! Don't update refresh time there, or else it won't work !!!
        #
        return int(self.expire - time())

    def expired(self):
        #
        #    Answer true if this session already expired
        #    !!! Don't update refresh time there, or else it won't work !!!
        #
        return self.expire < time()        # Compare self.expire with current time in seconds

