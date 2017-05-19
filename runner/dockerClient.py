from .logger import getLogger
from types import *
def getClient():
    import docker
    client = docker.from_env()

    return client

def getContainerAddress(container):
    container.reload()
    return container.attrs['NetworkSettings']['IPAddress']

def startClient(name, args):
    from time import sleep
    logger = getLogger()

    assert type(args['image']) is StringType, "Image name '%s' is poorly defined" % args['image']
    assert type(args['version']) is StringType, "Image Version is poorly defined"

    containerargs = {
        'detach': True,
        'tty': True,
    }

    if 'tmpfs' in args:
        containerargs['tmpfs'] = args['tmpfs']

    if 'environment' in args:
        containerargs['environment'] = args['environment']

    if 'entrypoint' in args:
        containerargs['entrypoint'] = args['entrypoint']

    if 'volumes' in args:
        containerargs['volumes'] = args['volumes']


    # Fetch the UID of the current user.
    uid = os.getuid()
    if uid:
        containerargs['user'] = os.getuid()

    # Start the container.
    image = "%s:%s" % (args['image'], args['version'])
    client = getClient()
    container = client.containers.run(image, **containerargs)

    # Check it is up.
    container.reload()
    assert container.status == 'running', \
        "Container did not start correctly from image %s (%s)" \
        % (image, container.status)
    logger.debug('Started container for %s with image %s (%s) - %s' % (name, image, container.name, container.status))

    return container
