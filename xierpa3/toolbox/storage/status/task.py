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

class Task(Status):
    u"""
    The ``Task`` class implements a set of paramters (inherited from ``Status``) that
    can be saved and derived from json files. These files are read by class method ``Task.next()`` 
    (or ``Task.peek()``) and executed by the running ``Scheduler`` instance. 
    A posted task can be positioned in the scheduler list by altering the <attr>priority</attr> and 
    <attr>order</attr> attributes of the post.
    """
    C = Status.C
    
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
        The ``getTaskNames`` method answers the list of file names in the
        pending task directory.
        """
        return os.listdir(cls.PATH_SCHEDULERTASKS)

    @classmethod
    def next(cls, remove=True):
        u"""
        The ``next`` method answers the next task instance that needs
        to be executed. The method takes the top of the sorted list of task files
        from the ``cls.PATH_SCHEDULERTASKS`` and creates the ``Task``
        instance and then deletes the task file (if the optional attribute 
        <attr>remove</attr> has default value ``True``. This method is also 
        called by ``self.peek()``, but then the file is not removed.
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
        The ``peek`` method answers the next task that must be executed 
        by the running ``Scheduler``. The method is equivalent to 
        ``self.next(False)``.
        """
        return cls.next(remove=False)

    def post(self, builder, priority=999999, order=0, args=None):
        u"""
        The ``post`` method adds ``self`` task to the scheduled tasks,
        if the ``builder.USE_MULTIPROCESSING`` is ``True``. Other wise the
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
        The ``execute`` method is called by the running ``Scheduler`` instance
        (or directly by the ``self.post`` method, if ``builder.USE_MULTIPROCESSING``
        is turned off. The attribute <attr>builderorcls</attr> can either be a ``Builder``
        instance (as it is called directly from from the ``self.post``) or a ``Builder``
        class when called from the running ``Scheduler`` (since the ``Scheduler``
        cannot know any instantiated builder, it just knows the class of the site.
        It is assumed that ``self.method`` exists as method name or list of method names.
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
        The ``getTaskName`` method constructs a unique task name that depends on the order
        of <attr>priority</attr>, ``timestamplong()``, <attr>order</attr> and an 6-digit random integer.
        """
        return '%06d-%s-%06d-%06d.json' % (priority, timestampLong(), order, randint(0, 999999))

    def log(self):
        f = open(self.PATH_SCHEDULERLOG + '/log.txt', 'ab')
        print '...', (self.description or `self`)
        f.write((self.description or `self`) + '\n')
        f.close()

