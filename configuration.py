import configparser


class Configuration:
    pass


class ConfigurationHandler:
    """Interface for a configuration handler"""

    def __init__(self, path):
        """

        :param path:
        """
        self.path = path

    def write_standard_config(self):  # Write the standard settings file
        """ Write the standard settings file

        """
        pass

    def read_config(self):
        """ Read the settings file and return all settings


        """
        pass
