from ..dependency import Dependency
from ..logger import getLogger
import os
class DatabaseDependency(Dependency):
    _description = 'Select a Database to run with'

    _arguments = [
        (
            ['--dbtype'],
            {
                'metavar': 'dbtype',
                'help': 'The database type to be used',
                'default': 'pgsql',
            }
        ),
        (
            ['--dbversion'],
            {
                'metavar': 'dbversion',
                'help': 'The version of the docker image to use',
                'default': 'latest',
            }
        ),
    ]

    _mapping = {
        'mariadb': {
            'image': 'mariadb',
            'config': {
                'dbtype': 'mariadb',
                'dbuser': 'moodle',
                'dbpass': 'moodle',
                'dbname': 'moodle',
                'dbport': '3306',
                'dbprefix': 'm_',
            },
            'environment': {
                'MYSQL_ROOT_PASSWORD': 'moodle',
                'MYSQL_DATABASE': 'moodle',
                'MYSQL_USER': 'moodle',
                'MYSQL_PASSWORD': 'moodle',
            },
            'tmpfs': {
                '/var/lib/mysql': '',
            },
        },
        'pgsql': {
            'image': 'postgres',
            'config': {
                'dbtype': 'pgsql',
                'dbuser': 'moodle',
                'dbpass': 'moodle',
                'dbname': 'moodle',
                'dbport': '5432',
                'dbprefix': 'm_',
            },
            'environment': {
                'POSTGRES_USER': 'moodle',
                'POSTGRES_PASSWORD': 'moodle',
                'POSTGRES_DB': 'moodle',
                #${DB_SCRIPTS}:/docker-entrypoint-initdb.d
            },
            'startupscripts': '/docker-entrypoint-initdb.d',
            'tmpfs': {
                '/var/lib/postgresql/data': '',
            },
        },
    }

    def run(self, args):
        assert args.dbtype in self._mapping, "Unknown database type '%s'" % args.dbtype

        # Start the Database Server.
        from ..dockerClient import startClient, getContainerAddress

        mapping = self._mapping[args.dbtype].copy()
        mapping['version'] = args.dbversion

        if 'volumes' not in mapping:
            mapping['volumes'] = {}

        if 'startupscripts' in mapping:
            mapping['volumes'].update(self.buildCustomisations(args.dbtype, mapping))

        container = startClient(__name__, mapping)
        self._containers.append(container)

        self.runner.setDependencyParam('dbhost', getContainerAddress(container))
        for key, value in mapping['config'].iteritems():
            self.runner.setDependencyParam(key, value)

    def buildCustomisations(self, dbtype, config):
        if 'startupscripts' not in config:
            return {}

        configDir = [
            'dependencies',
            'databases',
            dbtype,
        ]
        localConfigDir = [
            'local',
            'dependencies',
            'databases',
            dbtype
        ]
        volumes = {}
        volumes.update(self.buildCustomisationsFromDir(config['startupscripts'], configDir))
        volumes.update(self.buildCustomisationsFromDir(config['startupscripts'], localConfigDir))

        return volumes

    def buildCustomisationsFromDir(self, scriptdir, sourcedir):
        sourcedir = [
                os.path.dirname(os.path.realpath(__file__)),
                '..',
                '..',
            ] + sourcedir
        dir = os.path.join(*sourcedir)

        volumes = {}
        for root, dirs, files in os.walk(dir):
            for name in files:
                volumes[os.path.join(root, name)] = {
                    'bind': os.path.join(scriptdir, name),
                    'mode': 'ro',
                }

        return volumes
