import sys
import argparse
import pprint

from .logger import getLogger
logger = getLogger()

class Task(object):

    _arguments = None
    @property
    def arguments(self):
        if self._arguments is None:
            pprint.pprint(self._arguments)
            raise Exception("Arguments list not defined")
        return self._arguments

    _description = None
    @property
    def description(self):
        if self._description is None:
            raise Exception("Description not defined")
        return self._description

    _dependencies = None
    @property
    def dependencies(self):
        if self._dependencies is None:
            raise Exception("Dependencies not defined")
        return self._dependencies

    _runner = None
    @property
    def runner(self):
        return self._runner

    def setRunner(self, runner):
        self._runner = runner

    def configure(self, args):
        pass

    def run(self, args, dependencyParams):
        raise Exception("Runner not defined for")

class TaskRunner(object):
    def __init__(self, task):
        task.setRunner(self)
        self._task = task

    @property
    def task(self):
        return self._task

    _workingDirectory = None
    @property
    def workingDirectory(self):
        return self._workingDirectory

    _dependencies = None
    @property
    def dependencies(self):
        return self._dependencies

    def getDependency(self, name):
        return self._dependencies[name]

    def setDependency(self, name, dependency):
        assert name not in self._dependencies
        self._dependencies[name] = dependency

    _dependencyParams = None
    @property
    def dependencyParams(self):
        return self._dependencyParams or {}

    def setDependencyParam(self, name, value):
        if not self._dependencyParams:
            self._dependencyParams = {}

        self._dependencyParams[name] = value

    def run(self, sysargs=sys.argv, prog=None):
        from .dependencies import getDependencyInstance
        logger = getLogger()

        task = self.task;

        self.setupWorkspaceDirectory()

        parser = TaskArgumentParser(description=task.description, prog=prog,
            formatter_class=TaskArgumentFormatter)

        for argument in task.arguments:
            args = argument[0]
            kwargs = argument[1]
            if kwargs.has_key('silent'):
                del kwargs['silent']
                kwargs['help'] = argparse.SUPPRESS
            parser.add_argument(*args, **kwargs)

        # Fetch, and configure the dependencies.
        from collections import OrderedDict
        self._dependencies = OrderedDict()
        for dependencyName in task.dependencies:
            dependency  = getDependencyInstance(dependencyName)
            dependency.setRunner(self)
            dependency.configureParser(parser)
            self.setDependency(dependencyName, dependency)

        # Parse the arguments now we've configured the parser.
        args = parser.parse_args(sysargs)

        # Configure the task.
        task.configure(args)

        # Start the dependencies.
        dependencyResults = {}
        for dependencyName, dependency in self.dependencies.iteritems():
            dependency.run(args)

        # Run the task.
        try:
            task.run(args)
        except:
            parser.error(sys.exc_info())

    def setupWorkspaceDirectory(self):
        from tempfile import mkdtemp
        self._workingDirectory = mkdtemp()
        logger.debug('Creating new workspace directory for task at %s' % self._workingDirectory)

    def cleanup(self):
        from os import path
        workingDirectory = self.workingDirectory
        if workingDirectory and path.isdir(workingDirectory):
            from shutil import rmtree
            logger.debug('Deleting directory %s' % workingDirectory)
            rmtree(workingDirectory)

        for dependencyName, dependency in self.dependencies.iteritems():
            dependency.cleanup()

class TaskArgumentError(Exception):
    """Exception when a task sends an argument error"""
    pass


class TaskArgumentFormatter(argparse.HelpFormatter):
    """Custom argument formatter"""

    def _get_help_string(self, action):
        help = action.help
        if '%(default)' not in action.help:
            forbiddentypes = ['_StoreTrueAction', '_StoreFalseAction']
            if action.__class__.__name__ not in forbiddentypes and action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help += ' (default: %(default)s)'
        return help


class TaskArgumentParser(argparse.ArgumentParser):
    """Custom argument parser"""

    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '\n%s: error: %s\n' % (self.prog, message))
