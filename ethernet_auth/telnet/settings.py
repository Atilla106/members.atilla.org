from django.config import settings


class SwitchSettingsManager:
    '''
    Define a manager for different SwichSettings.

    This manager is a singleton that loads the switches configurations declared in the server configuration
    at instanciation time.
    '''

    _settings = None

    def get(switch):
        '''
        Get the SwitchSettings associated with the given switch.

        If no configuration is defined, return None.
        '''
        if SwitchSettingsManager._settings is None:
            SwitchSettingsManager._settings = SwitchSettingsManager.get_settings()

        if switch.name not in SwitchSettingsManager._settings:
            return None
        else:
            return SwitchSettings(switch, SwitchSettingsManager._settings[switch.name])

    def get_settings():
        '''
        Load the switches configuration from the server configuration.

        The configuration of the switches should have the following structure:
        >>> SWITCHES = {
        >>>     'switch-name-1': { // Configuration of switch-name-1 },
        >>>     'switch-name-2': { // Configuration of switch-name-2 }
        >>> }
        '''
        if not settings.SWITCHES:
            SwitchSettingsManager._settings = {}
        else:
            SwitchSettingsManager._settings = settings.SWITCHES


class SwitchSettings:
    '''Define an object containing the settings of a switch extracted from the server configuration.'''

    def __init__(self, switch, switch_configuration):
        self._switch = switch
        self._switch_configuration = switch_configuration

        self.name = switch.name
        self.adatpater = self._load_parameter('adaptater')
        self.username = self._load_parameter('username', '')
        self.password = self._load_parameter('password', '')

    def _load_parameter(self, name, default_value=None):
        if name in self._switch_configuration:
            return self._switch_configuration[name]
        else:
            return default_value
