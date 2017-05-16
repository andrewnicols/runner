from ..task import Task
from ..dockerClient import getClient
import sys
class InfoTask(Task):
    _description = 'List Info'

    _arguments = [
    ]

    _dependencies = [
    ]

    def run(self, args):
        import docker
        from pprint import pprint
        client = docker.from_env()

        containers = client.containers.list()
        command = ['echo "Hello!"']
        environment = {}
        for container in containers:
            pprint(container.name)
            resp = client.api.exec_create(
                container.id,
                "bash -c '%s'" % " ".join(command),
            )

            for line in client.api.exec_start(resp['Id'], stream=True):
                sys.stdout.write(line)

            pprint(resp)
            info = client.api.exec_inspect(resp['Id'])
            pprint(info)
