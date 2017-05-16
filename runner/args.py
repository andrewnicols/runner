def parseArgs():
    import argparse
    import sys
    import pprint
    import os

    from .version import __version__
    from .logger import getLogger
    from .tasks import getTaskInstance, getTaskList

    logger = getLogger()

    parser = argparse.ArgumentParser(description="Moodle Task Runner", add_help=False)

    # Add the basic arguments.
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('-v', '--version', action='store_true', help='Display the current version')

    # Add the list of commmands.
    parser.add_argument('task', metavar='task', nargs='?', help='The task to run', choices=getTaskList())
    parser.add_argument('-l', '--list', action='store_true', help='List the available tasks')

    parser.add_argument('args', metavar='arguments', nargs=argparse.REMAINDER, help='arguments of the command')

    parsedArgs = parser.parse_args()
    if not parsedArgs.task:
        if parsedArgs.version:
            print 'Moodle Task Runner version %s' % __version__
        elif parsedArgs.list:
            for task in getTaskList():
                print '{0:<15} {1}'.format(task, getTaskInstance(task)._description)
        else:
            parser.print_help()

        sys.exit(0)

    return parsedArgs
