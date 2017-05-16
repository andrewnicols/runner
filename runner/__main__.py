#!/usr/bin/env python

"""
Moodle Container Runner

Copyright (c) 2017 Andrew Nicols <andrew@nicols.co.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

def main():

    import sys
    import os

    from .version import __version__
    from .logger import setupLogger, getLogger
    from .tasks import getTaskInstance

    setupLogger()
    logger = getLogger()

    from .args import parseArgs
    parsedArgs = parseArgs()

    from .task import TaskRunner
    taskname = parsedArgs.task
    args = parsedArgs.args

    Task = getTaskInstance(taskname)
    Runner = TaskRunner(Task)

    try:
        Runner.run(args, prog='%s %s' % (os.path.basename(sys.argv[0]), taskname))
    except Exception as e:
        import traceback
        info = sys.exc_info()
        logger.error('%s: %s', e.__class__.__name__, e)
        logger.debug(''.join(traceback.format_tb(info[2])))
        sys.exit(1)
    finally:
        logger.error('Cleaning up')
        Runner.cleanup()

if __name__ == "__main__":
    main()
