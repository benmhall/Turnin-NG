from configobj import ConfigObj

class ProjectGlobal(object):
    """ This class is in case we ever decide we want global configurations. """
    
    def __init__(self, config_file):
        self.config = ConfigObj()
        self.config.filename = config_file
        self.config.indent_type = '    '
        self.config.unrepr = True
        if not self.config.has_key('Global'):
            self.config.reload()
            self.config['Global'] = {}
            self.config.default = ''
            self.config.write()

    def set_default(self, course):
        if self.config.has_key(course):
            self.config.reload()
            self.config.default = course
            self.config.write()
        else:
            raise ValueError("Please add the course %s first." % course)

class ProjectCourse(ProjectGlobal):
    """ This class represents a turnin course object. """

    def __init__(self, config_file, course):
        super(ProjectCourse, self).__init__(config_file)
        if not self.config.has_key(course):
            self.config.reload() # We don't want to clobber something
            self.config[course] = {}
            self.config.write()
        self.course = self.config[course]

    def read(self):
        """ Reads the self.course section in the config file. """
        self.config.reload()
        self.user = self.course['user']
        self.directory = self.course['directory']
        self.group = self.course['group']
        self.sections = self.course['sections']

    def write(self, user='', directory='', group='', sections='', default=''):
        """ Modifies the config file. """
        #self.config.reload() # We don't want to clobber something
        if user:
            self.course['user'] = user
        if directory:
            self.course['directory'] = directory
        if group:
            self.course['group'] = group
        if sections:
            self.course['sections'] = sections
        if type(default) == bool:
            self.course['default'] = default
        self.config.write()

class ProjectProject(ProjectCourse):
    """ This class represents a turnin course's project object. """

    def __init__(self, config_file, course, project):
        super(ProjectProject, self).__init__(config_file, course)
        if not self.course.has_key(project):
            self.config[course][project] = {}
            self.config[course][project]['enabled'] = False
            self.config.write()
        self.project = self.course[project]

    def read(self):
        """ Reads the project from the config file. """
        self.config.reload()
        self.description = self.project['description']
        self.enabled = self.project['enabled']

    def write(self, enabled, description=''):
        """ Modifies the config file. """
        #self.config.reload() # We don't want to clobber something
        self.project['enabled'] = enabled
        if description:
            self.project['description'] = description
        self.config.write()
