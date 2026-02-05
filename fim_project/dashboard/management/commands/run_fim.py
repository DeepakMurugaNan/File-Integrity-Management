from django.core.management.base import BaseCommand
from dashboard.models import MonitoredDirectory
from dashboard.utils import scan_directory_and_check
import sys

class Command(BaseCommand):
    help = 'Runs the File Integrity Monitor scan on all active directories.'

    def handle(self, *args, **options):
        directories = MonitoredDirectory.objects.filter(active=True)
        if not directories:
            self.stdout.write(self.style.WARNING("No active directories to monitor. Add one in the Admin or DB."))
            return

        self.stdout.write(f"Starting FIM Scan for {directories.count()} directories...")

        for directory in directories:
            self.stdout.write(f"Scanning: {directory.path}...")
            scan_directory_and_check(directory)
        
        self.stdout.write(self.style.SUCCESS("FIM Scan Completed."))
