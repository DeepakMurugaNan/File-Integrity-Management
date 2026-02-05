import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.core.management.base import BaseCommand
from dashboard.models import MonitoredDirectory
from dashboard.utils import process_file_event

class FIMEventHandler(FileSystemEventHandler):
    def __init__(self, directory_obj):
        self.directory_obj = directory_obj

    def on_created(self, event):
        if not event.is_directory:
            self.stdout_write(f"Detected CREATED: {event.src_path}")
            process_file_event(event.src_path, 'created', self.directory_obj)

    def on_modified(self, event):
        if not event.is_directory:
            self.stdout_write(f"Detected MODIFIED: {event.src_path}")
            process_file_event(event.src_path, 'modified', self.directory_obj)

    def on_deleted(self, event):
        if not event.is_directory:
            self.stdout_write(f"Detected DELETED: {event.src_path}")
            process_file_event(event.src_path, 'deleted', self.directory_obj)
            
    def set_stdout(self, stdout):
        self.stdout = stdout
        
    def stdout_write(self, msg):
        if hasattr(self, 'stdout'):
             self.stdout.write(msg)
        else:
             print(msg)


class Command(BaseCommand):
    help = 'Starts the Real-Time File Integrity Monitor.'

    def handle(self, *args, **options):
        directories = MonitoredDirectory.objects.filter(active=True)
        if not directories:
            self.stdout.write(self.style.WARNING("No active directories to monitor."))
            return

        observer = Observer()
        self.stdout.write("Starting Real-Time Watcher...")

        for directory in directories:
            if not os.path.exists(directory.path):
                self.stdout.write(self.style.ERROR(f"Directory not found: {directory.path}"))
                continue
                
            self.stdout.write(f"Watching: {directory.path}")
            event_handler = FIMEventHandler(directory)
            event_handler.set_stdout(self.stdout)
            
            observer.schedule(event_handler, directory.path, recursive=True)

        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        
        observer.join()
