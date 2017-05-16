from ..dependency import Dependency
from ..logger import getLogger
class LdapDependency(Dependency):
    _description = 'LDAP Server for tests'

    _arguments = [
        (
            ['--no-ldap'],
            {
                'action': 'store_false',
                'dest': 'ldap',
                'help': 'Whether to setup LDAP or not',
            }
        ),

    ]

    def run(self, args):
        logger = getLogger()
        if not args.ldap:
            logger.debug('LDAP server not requested.')
            return

        from ..dockerClient import startClient, getContainerAddress
        container = startClient(__name__, {
            'image': 'osixia/openldap',
            'version': 'latest',
        })
        self._containers.append(container)

        self.runner.setDependencyParam('ldapserver', getContainerAddress(container))
