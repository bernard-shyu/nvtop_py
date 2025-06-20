import argparse
import toml

class ConfigManager:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--refresh_interval', type=float, default=1.0, help='Data refresh interval in seconds')
        self.parser.add_argument('--X_data_points', type=int, default=1000, help='X-axis data point on the PLOT')
        self.parser.add_argument('--RESOLUTION', type=str, default="1800x800", help='Resolution: 2560x1440, 1920x1080, 1800x800, 1280x720')
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
