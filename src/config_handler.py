import argparse
import toml

class ConfigManager:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--refresh-interval', type=float, default=2.0,
                                help='Data refresh interval in seconds')
        self.args = self.parser.parse_args()
        try:
            self.config = toml.load('config/settings.toml')
        except FileNotFoundError:
            self.config = {'app': {}}

    def get(self, key, default=None):
        # Command-line args take precedence over TOML config
        if hasattr(self.args, key):
            return getattr(self.args, key)
        try:
            return self.config.get('app', {}).get(key)
        except:
            return default
