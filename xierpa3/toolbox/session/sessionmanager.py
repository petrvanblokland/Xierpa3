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
#     sessionmanager.py
#
#     SessionManager works similar to Cache (which is size limited), but it is
#     time limited instead.
#     If size of the cache runs over MAXCACHE then check on all existing
#     cache entries if their date is expired. If it is, then delete the entry.
#     This way we only will only do garbage collection once in a while and
#     not on every approach.
#
#     The SessionManager handles the virtual storage place for information
#     during a client session to keep information available between a sequence
#     of page queries.
#     All sessions are kept for as long as the expire times indicates (in seconds)
#     The default expiration time is 4 hours.
#     In principle sessions are publicly stored. But since the key is a number
#     with a significant large key size it is very unlikely that another client
#     is able to find the right key with its lifespan.
#
#     session.new()                                                Create a new session and answers a unique identifier and expire of 4 hours
#     session.new(3600, 'name of the session', 'guest')        Create a new session with name/user and a life span of one hour
#     session.delete(id)                                            Delete session with id
#
from time import time
from xierpa3.toolbox.dating import uniqueId, uniqueLong
from xierpa3.constants.constants import Constants
from session import Session

class SessionManager(dict):

    C = Constants 
    
    @classmethod
    def getNewSessionId(cls, size=None):
        u"""
        
        The <code>getNewSessionId</code> method answers a new generated session id of length <attr>size</attr>
        of <code>self.SESSION_SIDDIGITS</code> if omitted.
        
        """
        return str(uniqueId(size or cls.C.SESSION_SIDDIGITS))

    @classmethod
    def newTimeStamp(cls):
        u"""
        
        The <code>newTimeStamp</code> method answers a uniquelong, so there the total number is always unique.
        The result is a 18-digit long that will fit inside a Postgres bigint, instead of a relational id.
        
        """
        return uniqueLong()

    def getTimeStamps(self):
        u"""
        
        The <code>getTimeStamps</code> method answers a list with the timestamps of all existing session.
        The <code>self.garbageCollect</code> method is called to cleanup expired sessions once in a while.
        This is done before the collection of current time stamps is performed.
        
        """
        self.garbageCollect()
        timestamps = []
        for session in self.values():
            timestamps.append(session.timestamp)
        return timestamps

    def getSession(self, sid, limit=None, name=None, user=None, keep=False, protected=False):
        u"""
        
        The <code>getSession</code> method answers the <code>Session</code> instance with <attr>sid</attr>.
        Answer a new instance if the <attr>sid</attr> cannot be found. Store that session in the dict of <code>self</code>.
        
        """
        session = self.get(sid)
        if session is None:
            sid = self.getNewSessionId()
            timestamp = self.newTimeStamp()
            session = self[sid] = Session(sid, timestamp, limit=limit, name=name, user=user, keep=keep, protected=protected)
        return session

    def newSession(self):
        u"""
        
        The <code>getNewSession</code> method answers a new session.
        
        """
        return self.getSession(0) # Non-existing session id forces the creation of a new one

    def refresh(self, sid):
        u"""
        
        The <code>refresh</code> method refreshes the timestamp of session <attr>sid</attr>.
        Ignore the call if the session cannot be found.
        
        """
        if self.has_key(sid):
            self[sid].refresh()

    def getExpire(self, sid):
        u"""
        
        The <code>getExpire</code> method answers amount of seconds before the session <attr>sid</attr> will expire.
        Answer <code>0</code> is the session cannot be found.
        
        """
        if self.has_key(sid):
            return self[sid].expire - time()
        return 0

    def garbageCollect(self, force=False):
        #
        #     If the total size of the session cache exceeds the max number
        #     then make space by removing the expired ones.
        #     If none of them was expired, then keep them (we can allow to
        #     run over limit for a while because we don't want to loose information
        #     of running sessions.
        #
        if force or (len(self) % 100) == 0:                    # every now and then, clean the cache
            for keyv, session in self.items():                # Get key, expiration time an item
                if session.expired():                        # Expired?
                    self.delete(keyv)                        # Delete expired session.

    def getLoggedUserIds(self, applicationname):
        u"""
        
        The <code>getLoggedUserIds</code> method answers the list of ids for all users that are logged in with 
        non-expired sessions that have <attr>applicationname</attr>. 
        
        """
        ids = []
        for session in self.values():
            if not session.expired() and session['AppName'] == applicationname:
                ids.append(session['UserId'])
        return ids

    def getSessionById(self, applicationname, sid):
        u"""
        
        The <code>getSessionById</code> method answers the session the is defined by <attr>applicationname</attr>
        and <attr>sid</attr>. Answer <code>None</code> if the session cannot be found.
        
        """
        session = self.get(sid)
        if session['AppName'] == applicationname:
            return session
        return None

sessionmanager = SessionManager()

