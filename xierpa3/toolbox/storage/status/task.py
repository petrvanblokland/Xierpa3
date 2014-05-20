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
#    task.py
#
import os
import inspect
from random import randint
from xierpa3.toolbox.parsers.c_json import cjson
from xierpa3.toolbox.storage.status.status import Status
from xierpa3.toolbox.dating import timestampLong
from xierpa3.constants.constants import C

Super = Status

class Task(Super):
    u"""
    The <code>Task</code> class implements a set of paramters (inherited from <code>Status</code>) that
    can be saved and derived from json files. These files are read by class method <code>Task.next()</code> 
    (or <code>Task.peek()</code>) and executed by the running <code>Scheduler</code> instance. 
    A posted task can be positioned in the scheduler list by altering the <attr>priority</attr> and 
    <attr>order</attr> attributes of the post.
    """
    PATH_SCHEDULERTASKS = C.FSPATH_DATAROOT + '/_scheduler/tasks'
    PATH_SCHEDULERLOG = C.FSPATH_DATAROOT + '/_scheduler/log'

    # Make sure that these directories exist
    for dir in (PATH_SCHEDULERTASKS, PATH_SCHEDULERLOG):
        try:
            os.makedirs(dir)
        except OSError:
            pass

    @classmethod
    def getTaskNames(cls):
        u"""
        The <code>getTaskNames</code> method answers the list of file names in the
        pending task directory.
        """
        return os.listdir(cls.PATH_SCHEDULERTASKS)

    @classmethod
    def next(cls, remove=True):
        u"""
        The <code>next</code> method answers the next task instance that needs
        to be executed. The method takes the top of the sorted list of task files
        from the <code>cls.PATH_SCHEDULERTASKS</code> and creates the <code>Task</code>
        instance and then deletes the task file (if the optional attribute 
        <attr>remove</attr> has default value <code>True</code>. This method is also 
        called by <code>self.peek()</code>, but then the file is not removed.
        """
        tasknames = cls.getTaskNames()
        if not tasknames:
            return None
        task = None
        try:
            for taskname in tasknames:
                if taskname.startswith('.'):
                    continue
                path = cls.PATH_SCHEDULERTASKS + '/' + taskname
                f = open(path, 'rb')
                code = f.read()
                f.close()
                d = cjson.decode(code)
                task = cls(**d)
                if remove:
                    os.remove(path)
                break # Just get the top of the task file list
        except TypeError:
            print '### Error in json code:', code
        except Exception as e:
            print '### unknown error in task:', e
        return task

    @classmethod
    def peek(cls):
        u"""
        The <code>peek</code> method answers the next task that must be executed 
        by the running <code>Scheduler</code>. The method is equivalent to 
        <code>self.next(False)</code>.
        """
        return cls.next(remove=False)

    def post(self, builder, priority=999999, order=0, args=None):
        u"""
        The <code>post</code> method adds <code>self</code> task to the scheduled tasks,
        if the <code>builder.USE_MULTIPROCESSING</code> is <code>True</code>. Other wise the
        task is immediately executed. This direct execution is required for servers running
        Python2.5 or older (that don‚Äôs support multiprocessing) of for debugging in Eclipse.
        Due to a deep bug, the Python application of the split process crashes when in debug mode.
        """
        print '... Post task', self.name
        if builder.USE_MULTIPROCESSING:
            self.name = self.getTaskName(priority, order)
            self.arguments = args if isinstance(args, dict) else {}
            f = open(self.PATH_SCHEDULERTASKS + '/' + self.name, 'wb')
            f.write(cjson.encode(self.getValues()))
            f.close()
        else:
            # In case multiprocessing is off, execute the task immediately
            self.execute(builder)

    def execute(self, builderorcls):
        u"""
        The <code>execute</code> method is called by the running <code>Scheduler</code> instance
        (or directly by the <code>self.post</code> method, if <code>builder.USE_MULTIPROCESSING</code>
        is turned off. The attribute <attr>builderorcls</attr> can either be a <code>Builder</code>
        instance (as it is called directly from from the <code>self.post</code>) or a <code>Builder</code>
        class when called from the running <code>Scheduler</code> (since the <code>Scheduler</code>
        cannot know any instantiated builder, it just knows the class of the site.
        It is assumed that <code>self.method</code> exists as method name or list of method names.
        """
        if inspect.isclass(builderorcls):
            builderorcls = builderorcls()
            builderorcls.setup()
        if self.method:
            if not isinstance(self.method, (list, tuple)):
                self.method = [self.method]
            for method in self.method:
                # try:
                if hasattr(builderorcls, method):
                    getattr(builderorcls, method)(self, **(self.arguments or {}))
                    self.log()
                else:
                    print u'### Task builder does not have method ‚Äú%s‚Äù defined' % method
                # except AttributeError:
                #    print '### Task builder does not implement method ‚Äú%s‚Äù'
        else:
            print u'### Task does not have ‚Äúmethod‚Äù attribute defined'

    def getTaskName(self, priority, order):
        u"""
        The <code>getTaskName</code> method constructs a unique task name that depends on the order
        of <attr>priority</attr>, <code>timestamplong()</code>, <attr>order</attr> and an 6-digit random integer.
        """
        return '%06d-%s-%06d-%06d.json' % (priority, timestampLong(), order, randint(0, 999999))

    def log(self):
        f = open(self.PATH_SCHEDULERLOG + '/log.txt', 'ab')
        print '...', (self.description or `self`)
        f.write((self.description or `self`) + '\n')
        f.close()

