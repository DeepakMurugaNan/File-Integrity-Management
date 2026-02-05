from django.db import models
from django.utils import timezone

class MonitoredDirectory(models.Model):
    """
    Directories that the FIM system should watch.
    """
    path = models.CharField(max_length=500, unique=True, help_text="Absolute path to the directory")
    active = models.BooleanField(default=True, help_text="Enable or disable monitoring for this path")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.path

class FileRecord(models.Model):
    """
    Represents the baseline state of a file.
    """
    path = models.CharField(max_length=500, unique=True, db_index=True)
    directory = models.ForeignKey(MonitoredDirectory, on_delete=models.CASCADE, related_name='files')
    file_hash = models.CharField(max_length=64, help_text="SHA-256 Hash")
    last_modified = models.FloatField(help_text="Timestamp from os.stat")
    last_scanned = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.path

class MalwareSignature(models.Model):
    """
    Database of known bad hashes (simulated Threat Intelligence).
    """
    name = models.CharField(max_length=100, help_text="Name of the malware (e.g. EICAR Test File)")
    signature_hash = models.CharField(max_length=64, unique=True, help_text="SHA-256 Hash of the malware")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class AuditLog(models.Model):
    """
    Log of detected changes.
    """
    CHANGE_TYPES = [
        ('NEW', 'New File'),
        ('MODIFIED', 'Modified'),
        ('DELETED', 'Deleted'),
        ('PERM', 'Permission Change'),
        ('MALWARE', 'Malware Detected'),
    ]

    file_path = models.CharField(max_length=500)
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPES)
    old_hash = models.CharField(max_length=64, blank=True, null=True)
    new_hash = models.CharField(max_length=64, blank=True, null=True)
    detected_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False, help_text="Mark if alert has been acknowledged")
    details = models.TextField(blank=True, help_text="Extra details (e.g. Malware Name)")

    def __str__(self):
        return f"{self.change_type} - {self.file_path}"
