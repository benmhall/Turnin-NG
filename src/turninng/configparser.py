# Turnin-NG, an assignment submitter and manager. --- config parser
# Copyright (C) 2009  Ryan Kavanagh <ryanakca@kubuntu.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os.path
import uuid

from configobj import ConfigObj

class ProjectGlobal(object):
    """ This class class represents the global configurations for the project
        command.

    """

    def __init__(self, config_file):
        """
        Initialize. We'll create the configuration file if it doesn't
        already exist. We'll also add the [Global] section if it isn't
        already present.

        @type config_file: string
        @param config_file: path to the project configuration file
        @rtype: None

        """
        self.config = ConfigObj()
        self.config.filename = config_file
        self.config.indent_type = '    '
        self.config.unrepr = True
        self.config.reload()
        if not self.config.has_key('Global'):
            self.config['Global'] = {}
            self.config['Global']['default'] = ''
            self.config.write()

    def set_default(self, course):
        """
        Set the course 'course' as the default course for this professor.

        @type course: string
        @param course: Name of the course we want to set as default
        @rtype: None
        @raise ValueError: We try to set a non-existent course as default.

        """
        if self.config.has_key(course):
            self.config['Global']['default'] = course
            self.config.write()
        else:
            raise ValueError("Please add the course %s first." % course)

class ProjectAdminCourse(ProjectGlobal):
    """ This class represents a course object for project. """

    def __init__(self, config_file, course):
        """
        Initialize the course. If it doesn't already exist, we'll create it.
        self.course will be a shortcut to access the course configurations.

        @type config_file: string
        @param config_file: path to the project configuration file
        @type course: string
        @param course: name of the course
        @rtype: None

        """
        super(ProjectAdminCourse, self).__init__(config_file)
        if not self.config.has_key(course):
            self.config[course] = {}
            self.config[course]['projlist'] = ''
            self.config.write()
        self.course = self.config[course]
        """ @ivar: A shortcut to access the course configurations. """

    def write(self, user='', directory='', group=''):
        """ Modifies the config file.

        @type user: string
        @param user: username that owns the course directory.
        @type directory: string
        @param directory: path to the course submission directory.
        @type group: string
        @param group: group that owns the course directory.
        @rtype: None

        """
        if user:
            self.course['user'] = user
        if directory:
            self.course['directory'] = directory
        if group:
            self.course['group'] = group
        self.course['projlist'] = os.path.join(self.course['directory'],
                                  'turnin-ng.cf')
        self.config.write()
        projlist = ProjectCourse(self.course['projlist'], self.course.name)
        projlist.write(user = self.course['user'],
                       directory = self.course['directory'],
                       group = self.course['group'])

class ProjectCourse(ProjectGlobal):
    """ This class represents a course object for project. """

    def __init__(self, config_file, course):
        """
        Initialize the course. If it doesn't already exist, we'll create it.
        self.course will be a shortcut to access the course configurations.

        @type config_file: string
        @param config_file: path to the project configuration file
        @type course: string
        @param course: name of the course
        @rtype: None

        """
        super(ProjectCourse, self).__init__(config_file)
        if not self.config.has_key(course):
            self.config[course] = {}
            self.config[course]['default'] = ''
            self.config.write()
        self.course = self.config[course]
        """ @ivar: A shortcut to access the course configurations. """

    def set_default(self, project):
        """
        Set the project 'project' as the default project for this course.

        @type project: string
        @param project: Name of the project we want to set as default
        @rtype: None
        @raise ValueError: We try to set a non-existent project as default.

        """
        if self.course.has_key(project):
            self.course['default'] = project
            self.config.write()
        else:
            raise ValueError("Please add the project %s first." % project)

    def write(self, user='', directory='', group=''):
        """ Modifies the config file.

        @type user: string
        @param user: username that owns the course directory.
        @type directory: string
        @param directory: path to the course submission directory.
        @type group: string
        @param group: group that owns the course directory.
        @rtype: None

        """
        if user:
            self.course['user'] = user
        if directory:
            self.course['directory'] = directory
        if group:
            self.course['group'] = group
        self.config.write()

class ProjectProject(ProjectCourse):
    """ This class represents a project object for project. """

    def __init__(self, config_file, course, project):
        """
        Initialize the project. If it doesn't already exist, we'll create it.
        self.project will be a shortcut to access the project configurations.

        @type config_file: string
        @param config_file: path to the project configuration file
        @type course: string
        @param course: name of the course
        @type project: string
        @param project: name of the project.
        @rtype: None

        """
        super(ProjectProject, self).__init__(config_file, course)
        if not self.course.has_key(project):
            self.config[course][project] = {}
            self.config[course][project]['enabled'] = False
            self.config[course][project]['description'] = ''
            self.config[course][project]['uuid'] = str(uuid.uuid4())
            self.config.write()
        self.project = self.course[project]
        """ @ivar: shortcut to the project configurations """
        self.project['directory'] = os.path.join(self.course['directory'],
                                project)
        self.name = project

    def write(self, enabled, description='', directory='', tarball='', 
            default=False):
        """
        Modifies the config file.

        @type enabled: Bool
        @param enabled: Is this course enabled? True/False
        @type description: string
        @param description: Optional description for this project.
        @type directory: string
        @param directory: project directory
        @type tarball: string
        @param tarball: Path to the compressed project's tarball.
        @rtype: None

        """
        self.project['enabled'] = enabled
        if description:
            self.project['description'] = description
        if default:
            super(ProjectProject, self).set_default(self.name)
        if directory:
            self.project['directory'] = directory
        if tarball:
            self.project['tarball'] = tarball
        if not enabled:
            if self.course['default'] == self.name:
                self.course['default'] = ''
        self.config.write()

class TurninGlobal(object):
    """
    This class class represents the global configurations for the turnin
    command.

    """

    def __init__(self, config_file):
        """
        Initialize the global configurations.

        @type config_file: string
        @param config_file: path to the project configuration file
        @rtype: None
        @raise ValueError: The user is trying to use a poorly formatted
        configuration file.

        """

        self.config = ConfigObj()
        self.config.filename = config_file
        self.config.indent_type = '    '
        self.config.unrepr = True
        self.config.reload()
        if not self.config.has_key('Global'):
            raise ValueError("Invalid config file")

class TurninCourse(TurninGlobal):
    """ This class represents a course object for turnin. """

    def __init__(self, config_file, course):
        """
        Initialize the turnin course object. self.course is an alias to access
        the course configurations.

        @type config_file: string
        @param config_file: path to the project configuration file
        @type course: string
        @param course: name of the course
        @rtype: None
        @raise ValueError: The course isn't defined in the config file.

        """
        super(TurninCourse, self).__init__(config_file)
        if not self.config.has_key(course):
            raise ValueError("Course %s does not exists!" % course)
        self.course = self.config[course]
        """ @ivar: shortcut to the course configurations. """


class TurninProject(TurninCourse):
    """ This class represents a turnin course's project object. """

    def __init__(self, config_file, course, project):
        """
        Initialize the project's configurations for turnin.
        self.project will be a shortcut to access the project configurations.

        @type config_file: string
        @param config_file: path to the project configuration file
        @type course: string
        @param course: name of the course
        @type project: string
        @param project: name of the project.
        @rtype: None
        @raise ValueError: The project isn't defined in the config file.

        """
        super(TurninProject, self).__init__(config_file, course)
        if not self.course.has_key(project):
            raise ValueError("Project %s does not exist in course %s!" %
                    (project, course))
        self.project = self.course[project]
        """ @ivar: shortcut to the project configurations. """
        self.project['directory'] = os.path.join(self.course['directory'],
                project)
        self.name = project

class TurninList:
    """ This class represents a list of suffixes for submitted assignments. """

    def __init__(self, config_file):
        self.config = ConfigObj()
        self.config.filename = config_file
        self.config.indent_type = '    '
        self.config.unrepr = True
        self.config.reload()

    def write(self, project, suffix):
        """
        Write the project submission's suffix to the list file.

        @type project: TurninProject
        @param project: Project to which we submitted
        @type suffix: string
        @param suffix: submitted archive's unique suffix
        @rtype: None

        """
        course = project.course.name
        uuid = project.project['uuid']
        if not self.config.has_key(course):
            self.config[course] = {}
        self.config[course][uuid] = suffix
        self.config.write()
