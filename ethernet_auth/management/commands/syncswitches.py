from time import sleep

from django.core.management.base import BaseCommand

from ...sync import SynchronizationManager
from ...sync import SynchronizationStatus


class Command(BaseCommand):
    help = 'Perform a synchronization operation on the switches declared in the application'

    def handle(self, *args, **options):
        self.stdout.write('Initializing synchronization manager ...')
        manager = SynchronizationManager()

        manager.start_sync()
        self.stdout.write('Synchronization started ...')
        status = SynchronizationStatus.SYNCHRONIZING

        while status is SynchronizationStatus.SYNCHRONIZING:
            new_sync_status = manager.get_sync_status()
            status = new_sync_status[0]

            if status is SynchronizationStatus.FAILED:
                self.stderr.write(self.style.ERROR(new_sync_status[1]))
            elif status is SynchronizationStatus.DONE:
                self.stdout.write(self.style.SUCCESS(new_sync_status[1]))
            else:
                self.stdout.write(new_sync_status[1])

            sleep(1)
