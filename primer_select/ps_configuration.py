from configuration import *


class PsConfigurationHandler(ConfigurationHandler):

    def write_standard_config(self):  # Write the standard settings file
        """ Write the standard settings file

        """
        config = configparser.RawConfigParser()
        config.add_section('DEFAULT')
        config.set('DEFAULT', 'workingDir', '')
        config.add_section('PRIMER3')
        config.set('Primer3', 'path', '')
        config.set('Primer3', 'configPath', '')
        config.add_section('BLAST')
        config.set('BLAST', 'path', '')
        config.set('BLAST', 'maxHits', 5)
        config.add_section('RNAcofold')
        config.set('RNAcofold', 'path', '')
        config.add_section('Optimization')
        config.set('Optimization', 'steps', 500)
        config.set('Optimization', 'maxTemp', 15)
        with open(self.path, 'w') as configfile:
            config.write(configfile)

    @property
    def read_config(self):  # Read the settings file
        """ Read the settings file

        """

        config = configparser.RawConfigParser()
        config.read(self.path)
        c = Configuration()
        c.wd = config.get('DEFAULT', 'workingDir')
        c.p3_path = config.get('Primer3', 'path')
        c.p3_config_path = config.get('Primer3', 'configPath')

        c.blast_path = config.get('BLAST', 'path')
        c.blast_max_hits = config.getint('BLAST', 'maxHits')

        c.rnacf_path = config.get('RNAcofold', 'path')

        c.opt_steps = config.getint('Optimization', 'steps')
        c.opt_max_temp = config.getint('Optimization', 'maxTemp')

        return c

