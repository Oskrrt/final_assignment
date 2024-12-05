import os
import tomllib

class ConfigManager:
    CONFIG_FILE_PATH = os.path.join('src', 'tarjan_planner', 'route_planner_config.toml')

    @classmethod
    def load_config(cls, config_header):
        try:
            with open(cls.CONFIG_FILE_PATH, "rb") as f:
                return tomllib.load(f)[config_header]
        except Exception as e:
            print("error occured " + repr(e))
            raise e