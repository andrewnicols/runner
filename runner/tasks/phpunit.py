from ..task import Task
from ..logger import getLogger
class PhpunitTask(Task):
    _description = 'Run PHPUnit'

    _arguments = [
        (
            ['--filter'],
            {
                'metavar': 'filter',
                'help': 'Filters the phpunit tests'
            }
        ),
		(
			['--no-long-running'],
			{
				'action': 'store_false',
                'dest': 'longrunning',
				'help': 'Disable long-running tests'
			}
		),
    ]

    """
        TODO:
        Or, make these optional dependencies based upon flags :/
        'solr',
        'redis',
        'memcached',
    """

    _dependencies = [
        'gitcheckout',
        'database',
        'ldap',
        'php',
        'moodleconfig',
    ]

    def run (self, args):
        from pprint import pprint
        import sys
        from ..dockerClient import getClient

        client = getClient()
        logger = getLogger()

        phpContainer = self.runner.getDependency('php').firstContainer

        command = [
            # This will move to environment soon.
            'export COMPOSER_CACHE_DIR=/.composer/cache'
            ';',
            'php',
            '/var/www/html/moodle/admin/tool/phpunit/cli/init.php',
        ]
        logger.info("Initialising phpunit with '%s'" % " ".join(command))

        resp = client.api.exec_create(
            phpContainer.id,
            "bash -c '%s'" % " ".join(command)
        )

        for line in client.api.exec_start(resp['Id'], stream=True):
            sys.stdout.write(line)
        info = client.api.exec_inspect(resp['Id'])

        assert info['ExitCode'] == 0, "PHPUnit Initialisation exited non-zero with %s" % info['ExitCode']
        logger.info("PHPUnit Ready")

        command = [
            'cd /var/www/html/moodle',
            ';',
            'php',
            './vendor/bin/phpunit',
        ]

        if args.filter:
            command.append('--filter', args.filter)

        logger.info("Running phpunit with '%s'" % " ".join(command))

        resp = client.api.exec_create(
            phpContainer.id,
            "bash -c '%s'" % " ".join(command)
        )

        for line in client.api.exec_start(resp['Id'], stream=True):
            sys.stdout.write(line)
        info = client.api.exec_inspect(resp['Id'])

        assert info['ExitCode'] == 0, "PHPUnit exited non-zero with %s" % info['ExitCode']
