import ConfigParser
import os.path


class Configuration:
    pass


class ConfigurationHandler:
    """Interface for a configuration handler"""

    def __init__(self, path):
        """

        :param path:
        """
        self.path = path
        if not os.path.isfile(self.path):
            self.write_standard_config()


    def write_standard_config(self):  # Write the standard settings file
        """ Write the standard settings file

        """
        pass

    def read_config(self):
        """ Read the settings file and return all settings


        """
        pass
