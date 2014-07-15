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
#    scheduler.py
#
import time
from xierpa3.toolbox.storage.status.task import Task
from xierpa3.constants.constants import Constants

class Scheduler(object):

    C = Constants
    
    def __init__(self, client):
        self.client = client
        self.status = self.C.SCHEDULER_STATUS_IDLE

    def run(self):
        u"""
        <doc>The <code>run</code> method of the <code>Scheduler</code> class is the main loop that runs infinite, unless
        the <code>self.status</code> is set to a different value than <code>self.C.SCHEDULER_STATUS_RUN</code>. In every
        cycle a new <code>Task</code> is requested from the list of scheduler tasks. If the result is <code>None</code>
        (there are no pending tasks), then the scheduler mode. The method will involuntary sleep for <code>
        self.C.SCHEDULER_SLEEPTIME</code> amount of seconds, before querying the task list again. In the idle state, the
        method calls <code>self.doIdle()</code>, which defaults to do nothing.<br/>
        
        If there is a valid task pending, then <code>self.doTask(task)</code> is called. Note that while there are
        pending tasks, the loop will not sleep.</doc>
        """
        self.status = self.C.SCHEDULER_STATUS_RUN
        while self.status == self.C.SCHEDULER_STATUS_RUN:
            task = Task.next()
            if task is not None:
                self.doTask(task)
            else:
                self.doIdle()
                # Involuntary sleep outside doIdle call, which may be inherited and changed,
                time.sleep(self.C.SCHEDULER_SLEEPTIME)


    def hasTask(self):
        u"""
        <doc>
        The <code>hasTask</code> method answers the boolean flag if there are any pending tasks in the scheduler task
        list. 
        </doc>
        """
        return bool(Task.peek())

    def doTask(self, task):
        if self.C.USE_SCHEDULERVERBOSE:
            print '... [Scheduler task]', (task.description or task.name)
        task.execute(self.C)

    def doIdle(self):
        if self.C.USE_SCHEDULERVERBOSE:
            print '... [Scheduler idle]'
