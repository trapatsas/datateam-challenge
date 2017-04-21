"""

Configuration
=============
"""

import configparser
import os


class Settings:
    """
    Application settings and configurations. 
    
    Settings object loads the settings from the respective .ini file.
    
    Parameters:
        :environment: String. The environment name. A configuration file with the name settings-<ENVIRONMENT NAME>.ini should exists.
    """
    active_sections = [
        'redis',
        'geo',
        'input',
        'output',
        'logging',
        'info'
    ]

    def __init__(self, environment):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'configuration/settings-{0}.ini'.format(environment)
        ))

    def __getattr__(self, name):
        """
        Convention based attributes.
        Creates a dynamic attribute named <SECTION>_<PROPERTY> for each property of the configuration file.
        
        :name: The property name
        
        :return: The property value
        """
        for section in self.active_sections:
            if name.startswith(section + '_'):
                key = name[len(section) + 1:]
                return self.config_parser.get(section, key)
        raise Exception('Unknown setting {}'.format(name))
