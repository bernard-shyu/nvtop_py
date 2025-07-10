import argparse
import toml

class ConfigManager:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--refresh_interval', type=float, default=1.0, help='Data refresh interval in seconds')
        self.parser.add_argument('--X_data_points', type=int, default=200, help='X-axis data point on the PLOT')
        self.parser.add_argument('--RESOLUTION', type=str, default="1800x800", help='Resolution: 2560x1440, 1920x1080, 1800x800, 1280x720')
        self.args = self.parser.parse_args()
        self.defaults = {}
        for action in self.parser._actions:
            if action.default is not None and action.dest != 'help':
                self.defaults[action.dest] = action.default
        try:
            self.config = toml.load('config/settings.toml')
        except FileNotFoundError:
            self.config = {'app': {}}

    def get(self, key, default=None):
        # Command-line args take precedence over TOML config only when explicitly set
        if hasattr(self.args, key):
            arg_value = getattr(self.args, key)
            # Get the default value from parser
            default_value = self.defaults.get(key, None)
            # Only use command-line value if it's different from default
            if arg_value != default_value:
                return arg_value
        
        # Check TOML config first for top-level section
        if key in self.config:
            return self.config[key]
        
        # Then search for the key in all sections
        for section in self.config.values():
            if isinstance(section, dict) and key in section:
                return section[key]
        
        # If key contains dots, traverse nested structure
        if '.' in key:
            current = self.config
            for part in key.split('.'):
                if isinstance(current, dict):
                    current = current.get(part, {})
                else:
                    return default
            return current if current != {} else default
        
        return default
