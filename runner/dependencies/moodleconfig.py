from ..dependency import Dependency
import os
class MoodleconfigDependency(Dependency):
    _description = 'Setup the Moodle Configuration file'

    _arguments = []

    def run(self, args):
        # TODO Find a better way to do this.

        source = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'templates', 'config.php')
        target = os.path.join(self.runner.workingDirectory, 'config.php')

        sourceFile = open(source, 'r')
        content = sourceFile.read()
        sourceFile.close()

        # Setting default params
        configParams = {
            # Default behat configuration.
            'fromrun': 0,
            'totalrun': 0,
            'shareddir': '',

            # Default Solr server.
            'solrhost': '',

            # Default LDAP server.
            'ldaphost': '',
        }

        configParams.update(self.runner.dependencyParams)

        from ..logger import getLogger
        logger = getLogger()
        for key, value in configParams.iteritems():
            logger.debug('Replacing %%%%%s%%%% with %s' % (key, str(value)))
            content = content.replace('%%%%%s%%%%' % key, str(value))

        targetFile = open(target, 'w')
        targetFile.write(content)
        targetFile.close()
