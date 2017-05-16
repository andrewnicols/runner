import sys
import argparse

from .logger import getLogger

class Dependency(object):
    def __init__(self):
        self._containers = []

    def run(self, args):
        raise Exception("Runner not defined")

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

    _containers = None
    @property
    def containers(self):
        if self._containers:
            return self._containers

        return []

    @property
    def firstContainer(self):
        return self._containers[0] or None

    _runner = None
    @property
    def runner(self):
        return self._runner

    def setRunner(self, runner):
        self._runner = runner

    def configureParser(self, parser):
        for argument in self.arguments:
            args = argument[0]
            kwargs = argument[1]
            if kwargs.has_key('silent'):
                del kwargs['silent']
                kwargs['help'] = argparse.SUPPRESS
            parser.add_argument(*args, **kwargs)

    def cleanup(self):
        logger = getLogger()
        logger.debug('Shutting down all containers for %s' % __name__)
        for container in self.containers:
            logger.debug('Shutting down docker Container %s' % container.name)
            container.kill()

    def __del__(self):
        cleanup()
