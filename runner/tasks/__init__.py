def getTask(task):
    cls = task.capitalize() + 'Task'
    return getattr(getattr(getattr(__import__('runner.%s.%s' % ('tasks', task)), 'tasks'), task), cls)

def getTaskInstance(taskname):
    taskClass = getTask(taskname)

    return taskClass()

def getTaskList():
    # Todo - automate this.
    taskList = [
        'info',
        'phpunit',
    ]

    return sorted(taskList)
