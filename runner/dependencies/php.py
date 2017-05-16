from ..dependency import Dependency
class PhpDependency(Dependency):
    _description = 'Select a version of PHP'

    _arguments = [
        (
            ['--phpversion'],
            {
                'metavar': 'phpversion',
                'help': 'The version of the docker image to use',
                'default': '70',
            }
        ),

    ]

    _mapping = {
        '70': {
            'image': 'andrewnicols/moodle-php',
            'version': '7.0',
            'entrypoint': '/bin/bash',
            'environment': {
            },
        },
    }

    def run(self, args):
        from ..dockerClient import startClient, getContainerAddress
        import os
        from tempfile import mkdtemp
        from ..logger import getLogger

        if args.phpversion not in self._mapping:
            raise Exception("Unknown PHP Version '%s'" % args.phpversion)

        logger = getLogger()

        # Configure the container.
        containerargs = self._mapping[args.phpversion].copy()

        # Setup the volume configuration.
        scriptdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
        if 'volumes' not in containerargs:
            containerargs['volumes'] = {}

        containerargs['volumes'][self.runner.workingDirectory] = {
            'bind': '/var/www/html/moodle',
            'mode': 'rw',
        }

        shareddir = mkdtemp(dir=os.path.join(scriptdir, 'shared'), prefix='run_')
        containerargs['volumes'][shareddir] = {
            'bind': '/var/www/shared',
            'mode': 'rw',
        }

        containerargs['volumes'][os.path.join(scriptdir, 'cache', 'composer')] = {
            'bind': '/.composer/cache',
            'mode': 'rw',
        }

        container = startClient(__name__, containerargs)
        logger.debug("Started PHP Client")
        self._containers.append(container)

        container.exec_run('mkdir -p /var/www/data/moodle')
        container.exec_run('mkdir -p /var/www/data/phpunit')
        container.exec_run('mkdir -p /var/www/data/behat')

        self.runner.setDependencyParam('datadir', '/var/www/data')
        self.runner.setDependencyParam('phphost', getContainerAddress(container))
        self.runner.setDependencyParam('shareddir', shareddir)
