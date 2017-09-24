from enum import Enum
from importlib import import_module
from threading import Thread

from django import db
from django.utils import timezone

from .models import Switch
from .models import SwitchPort
from .models import SwitchPortAction
from .settings import SwitchSettingsManager


class SynchronizationStatus(Enum):
    PENDING = 1
    SYNCHRONIZING = 2
    DONE = 3
    FAILED = 4


class SynchronizationManager:
    '''
    Handle the synchronization operations on the switches configured in the application.

    In order to speed up the process of synchronization, one thread is used per switch.
    '''

    def __init__(self):
        self._switches = None
        self._sync_status = SynchronizationStatus.PENDING
        self._threads = {}

    def start_sync(self, switches=None):
        '''
        Start to synchronize the configuration of the server with the switches.

        If no [model.Switch] are given, synchronize all the configured switches.
        '''
        self._switches = (switches if switches is not None else Switch.objects.all())
        self._sync_status = SynchronizationStatus.SYNCHRONIZING

        # Prepare the threads
        for switch in self._switches:
            settings = SwitchSettingsManager.get(switch)

            if settings is not None:
                self._threads[switch] = SynchronizationThread(switch, settings.adaptater_module,
                                                              settings.adaptater_name)

        for thread in self._threads.values():
            thread.start()

    def update_sync_status(self):
        '''
        Update the status of the synchronization returned by get_sync_status().

        In future versions, we can expect this method to handle thread exceptions or failures
        during the synchronization.
        '''
        if self._get_alive_thread_count() is 0:
            self._sync_status = SynchronizationStatus.DONE

    def get_sync_status(self):
        '''
        Get the status of the current synchronization.

        Return a tuple containing one of SynchronizationStatus as the first value and a message describing
        the current state as the second value.
        '''
        self.update_sync_status()
        return_message = ''

        if self._sync_status is SynchronizationStatus.PENDING:
            return_message = 'The synchronization has not started yet'
        elif self._sync_status is SynchronizationStatus.SYNCHRONIZING:
            thread_count = len(self._threads)
            alive_thread_count = self._get_alive_thread_count()
            return_message = 'Synchronizing switches : {} done out of {} ...'.format(
                    thread_count - alive_thread_count, thread_count)
        elif self._sync_status is SynchronizationStatus.DONE:
            return_message = '{} switche(s) successfully synchronized'.format(len(self._threads))
        elif self._sync_status is SynchronizationStatus.FAILED:
            return_message = 'The synchronization has failed'

        return (self._sync_status, return_message)

    def _get_alive_thread_count(self):
        '''Return the count of alive threads in the current synchronization.'''
        count = 0

        for thread in self._threads.values():
            if thread.is_alive():
                count = count + 1
        return count


class SynchronizationThread(Thread):
    def __init__(self, switch, adaptater_module, adaptater_name):
        '''
        Initialize a new synchronization thread.

        Note that the thread will load the telnet.TelnetAdaptater associated with the switch,
        but will not test the switch configuration yet.
        '''
        super(SynchronizationThread, self).__init__(target=self.perform_sync, name=switch.name)

        # Load the adaptater class
        module = import_module(adaptater_module)
        adaptater_class = getattr(module, adaptater_name)

        self._switch = switch
        self._adaptater = adaptater_class(switch)

    def perform_sync(self):
        '''
        Perform the actual synchronization with the switch.

        For each SwitchPort declared in the Switch, calculate its current status and update the
        switch port status if needed.
        '''
        self._adaptater.connect()

        for port in SwitchPort.objects.filter(switch=self._switch):
            status = self._adaptater.get_port_status(port)
            current_action = SwitchPortAction.objects.filter(
                    switch_port=port, expiration_date__gt=timezone.now()).first()
            current_state = (current_action.new_state if current_action else port.default_state)

            if status[0] is not current_state:
                self._adaptater.set_port_state(port, current_state)
                port.current_state = current_state
                port.save()

        self._adaptater.disconnect()
        db.connection.close()
