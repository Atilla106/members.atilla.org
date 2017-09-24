'''Adaptaters for telnet connection with switches.'''
import re

from telnetlib import Telnet

from ..models import AUTO
from ..models import AUTHORIZED
from ..models import UNAUTHORIZED
from ..settings import SwitchSettingsManager

from .exceptions import TelnetError


class SwitchTelnetAdaptater:
    '''
    Define a switch telnet adaptater.

    Adaptaters shoud be used to access switches using a telnet connection.
    This class can be inherited to implement telnet connections to different switch models, that do not use
    the same telnet interface.
    '''

    def __init__(self, switch):
        '''Initialize a new telnet adaptater using the given models.Switch.'''
        self._switch = switch

    def connect(self):
        '''
        Establish a telnet connection to the switch.

        This telnet connection should be then closed using disconnect(). A telnet adaptater can also implement
        __del__() to automatically close the connection to the switch.
        '''
        raise NotImplementedError('Method not implemeted')

    def get_port_status(self, switch_port):
        '''
        Get the current status of the given model.SwitchPort.

        Return a tuple containing the state of the switch (models.SWITCH_PORT_STATE) and the username of
        the user connected to the port.
        If no user is connected, returns None as the username.
        '''
        raise NotImplementedError('Method not implemeted')

    def set_port_state(self, switch_port, switch_port_state):
        '''Set the port state of the given model.SwitchPort to the given state.'''
        raise NotImplementedError('Method not implemeted')

    def disconnect(self):
        '''Disconnect from the switch.'''
        raise NotImplementedError('Method not implemeted')


class DellPowerConnect3424Adaptater(SwitchTelnetAdaptater):
    '''
    Implementation of SwitchTelnetAdaptater for Dell PowerConnect switches.

    Note that, as we are communicating with the switch over a telnet session that only supports ASCII,
    we won't be able to use the str().format() method as we are dealing with byte strings.
    '''

    def __init__(self, switch):
        # Define wether the adaptater is currently connected to the switch or not.
        self._is_connected = False

        # Store the connection to the switch.
        self._connection = None

        # Store the configuration of the switch provided by the server configuration.
        self._switch_settings = SwitchSettingsManager.get(switch)

        super(DellPowerConnect3424Adaptater, self).__init__(switch)

    def connect(self):
        self._connection = Telnet(host=self._switch.ip_address, port=23, timeout=3)

        for i in range(3):
            if self._try_connect(False if i == 0 else True):
                self._is_connected = True
                return

        raise TelnetError('Unable to connect to [{}]'.format(self._switch.ip_address))

    def _try_connect(self, skip_user_read=False):
        '''Try to connect to the switch. Return True if the connection is successful.'''

        if not skip_user_read:
            self._connection.read_until(b'User Name:', 5)
        self._connection.write(self._switch_settings.username.encode('ascii') + b'\n')

        self._connection.read_until(b'Password:')
        self._connection.write(self._switch_settings.password.encode('ascii') + b'\n')

        result = self._connection.expect([b'# ', b'User Name:'], 3)
        if result[0] == 0:
            return True
        else:
            return False

    def get_port_status(self, switch_port):
        if not self._is_connected:
            raise TelnetError('The adaptater is not connected to the switch')

        # Here are some examples of lines where this regex should be applied:
        # e1       Auto               Authorized*   Disabled 3600       n/a
        # e2       Auto               Authorized*   Disabled 3600       myusername
        # e12      Force Authorized   Authorized    Disabled 3600       myotherusername
        # e12      Force Unauthorized Authorized*   Disabled 3600       n/a
        regex = switch_port.name.encode('ascii') + b'\s+(?P<state>\w+(\s\w+)?)(\s+\S+){3}\s+(?P<user>\S+)'
        status_regex = re.compile(regex, re.I)

        self._connection.write(b'show dot1x ethernet ' + switch_port.name.encode('ascii') + b'\n')
        self._connection.write(b'q\n')
        result = self._connection.expect([status_regex], 3)

        if result[1].group('state') == b'Auto':
            state = AUTO
        elif result[1].group('state') == b'Force Authorized':
            state = AUTHORIZED
        elif result[1].group('state') == b'Force Unauthorized':
            state = UNAUTHORIZED
        else:
            state = None

        user = (None if result[1].group('user') == 'n/a' else result[1].group('user'))

        return (state, user)

    def set_port_state(self, switch_port, switch_port_state):
        if not self._is_connected:
            raise TelnetError('The adaptater is not connected to the switch')

        if switch_port_state not in [AUTO, AUTHORIZED, UNAUTHORIZED]:
            raise TelnetError('Invalid port state')

        self._connection.write(b'configure\n')
        self._connection.read_until(b'(config)# ')
        self._connection.write(b'interface ethernet ' + switch_port.name.encode('ascii') + b'\n')
        self._connection.read_until(b'(config-if)# ')

        if switch_port_state == AUTO:
            new_state = b'auto'
        elif switch_port_state == AUTHORIZED:
            new_state = b'force-authorized'
        elif switch_port_state == UNAUTHORIZED:
            new_state = b'force-unauthorized'

        self._connection.write(b'dot1x port-control ' + new_state + b'\n')
        self._connection.read_until(b'(config-if)# ')
        self._connection.write(b'exit\n')
        self._connection.read_until(b'(config)# ')
        self._connection.write(b'exit\n')

    def disconnect(self):
        self._connection.close()

    def __del__(self):
        if self._is_connected is False and self._connection is not None:
            self.disconnect()
