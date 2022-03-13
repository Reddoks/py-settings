# Configuration management module
# Source: https://github.com/Reddoks/py_settings
# Version 0.31
# Imports
import os, json, uuid, copy

# Dict with default settings
defaults = {
    "APP_WORK_DIR": "",
    "APP_SECRET": uuid.uuid4().hex,
    "APP_DB_FILENAME": "db.sqlite",
    "APP_SERVER_PORT": 80,
    "APP_SERVER_ADDRESS": "0.0.0.0"
}
# Dict with settings to drop from config file
drop_list = [
    "APP_WORK_DIR",
    "APP_SECRET"
]


class Settings(object):
    def __init__(self, config_file=None):
        # Set defaults
        self.__dict__ = {**self.__dict__, **defaults}
        # Check work directory settings
        # If work folder defined via environment - update it
        if os.getenv('APP_WORK_DIR'):
            self.__dict__.APP_WORK_DIR = os.getenv('APP_WORK_DIR')
        else:
            # If APP_WORK_DIR not configured by defaults or via environment variable - use current folder
            if 'APP_WORK_DIR' not in self.__dict__:
                self.APP_WORK_DIR = os.getcwd()
        # Load config from file
        if config_file:
            config_settings = self.load_config(config_file)
            # If config data loaded, apply to setting
            if config_settings:
                self.__dict__ = {**self.__dict__, **config_settings}
        # Apply environment variables
        for s_var in self.__dict__:
            if os.getenv(str(s_var)):
                self[s_var] = os.getenv(str(s_var))
        if config_file:
            if not config_settings:
                self.save_config(config_file)
        return

    # Load configuration from file
    def load_config(self, config_file):
        # Check configuration file exist and load configuration
        if os.path.isfile(os.path.join(self.APP_WORK_DIR, config_file)):
            with open(os.path.join(self.APP_WORK_DIR, config_file), 'r') as file:
                settings = json.load(file)
                return settings
        else:
            return None

    # Save configuration to file
    def save_config(self, config_file):
        with open(os.path.join(self.APP_WORK_DIR, config_file), 'w') as file:
            settings_save = copy.deepcopy(self.__dict__)
            for item in drop_list:
                del settings_save[item]
            json.dump(settings_save, file, indent=4)
        return