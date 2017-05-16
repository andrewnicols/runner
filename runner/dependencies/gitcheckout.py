from ..dependency import Dependency
from ..logger import getLogger
class GitcheckoutDependency(Dependency):
    _description = 'Checkout the relevant git repository'

    _arguments = [
        (
            ['--repository'],
            {
                'metavar': 'repository',
                'help': 'The remote repository to be cloned',
                'default': 'git://git.moodle.org/integration.git',
            }
        ),
        (
            ['--branch'],
            {
                'metavar': 'branch',
                'help': 'The branch on the remote repository to clone',
                'default': 'master',
            }
        ),
    ]

    def run(self, args):
        from git import Repo

        logger = getLogger()
        logger.debug('Cloning into %s repo %s' % (self.runner.workingDirectory, args.repository))
        repo = Repo.clone_from(args.repository, self.runner.workingDirectory, progress=MyProgressPrinter(), branch = args.branch)
        import pprint

from git import RemoteProgress
class MyProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        logger = getLogger()
        #logger.debug('Cloning repository ({0:.0f}%)'.format((cur_count / max_count or 100.0) * 100))
