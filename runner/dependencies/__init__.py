def getDependency(dependency):
    cls = dependency.capitalize() + 'Dependency'
    return getattr(getattr(getattr(__import__('runner.%s.%s' % ('dependencies', dependency)), 'dependencies'), dependency), cls)

def getDependencyInstance(dependencyname):
    dependencyClass = getDependency(dependencyname)

    return dependencyClass()
