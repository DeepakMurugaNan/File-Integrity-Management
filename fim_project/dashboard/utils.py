import hashlib
import os

def calculate_file_hash(filepath, block_size=65536):
    """
    Calculates the SHA-256 hash of a file.
    Returns the hex digest string.
    """
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None
    except PermissionError:
        return "PERMISSION_DENIED"
    except Exception as e:
        return f"ERROR: {e}"

from .models import FileRecord, AuditLog, MonitoredDirectory, MalwareSignature
from django.utils import timezone

SUSPICIOUS_EXTENSIONS = {'.exe', '.bat', '.cmd', '.ps1', '.vbs', '.scr'}

def check_for_malware(filepath, file_hash):
    """
    Checks file against malware indicators.
    Returns (is_malware, reason).
    """
    # 1. Check Hash Signature
    try:
        sig = MalwareSignature.objects.get(signature_hash=file_hash)
        return True, f"Known Malware: {sig.name}"
    except MalwareSignature.DoesNotExist:
        pass

    # 2. Check Extension (Simple heuristic)
    _, ext = os.path.splitext(filepath)
    if ext.lower() in SUSPICIOUS_EXTENSIONS:
        return True, f"Suspicious Extension: {ext}"

    return False, None

def scan_directory_and_check(monitored_dir_obj):
    """
    Scans the given MonitoredDirectory.
    1. Detects NEW files.
    2. Detects MODIFIED files (hash change).
    3. Detects DELETED files.
    4. Cjecks for MALWARE.
    Updates the DB and creates AuditLogs.
    """
    root_path = monitored_dir_obj.path
    if not os.path.exists(root_path):
        print(f"Warning: Directory {root_path} does not exist.")
        return

    current_files = set()

    # 1. Walk the directory
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            
            # Skip if file is transient/temp? (Optional enhancement)
            
            current_hash = calculate_file_hash(full_path)
            stat = os.stat(full_path)
            last_mod = stat.st_mtime
            
            current_files.add(full_path)

            # Check for Malware (Always check current state)
            is_malware, reason = check_for_malware(full_path, current_hash)
            if is_malware:
                # Log Malware Alert (De-duplicate if already active?)
                # For now, we log it if it's a new occurrence or simple log
                # To avoid spam, we might check if the last log for this file was MALWARE and unresolved.
                last_log = AuditLog.objects.filter(file_path=full_path).last()
                if not (last_log and last_log.change_type == 'MALWARE' and not last_log.is_resolved):
                    AuditLog.objects.create(
                        file_path=full_path,
                        change_type='MALWARE',
                        new_hash=current_hash,
                        details=reason,
                        is_resolved=False
                    )

            # Get or Create
            record, created = FileRecord.objects.get_or_create(
                path=full_path,
                defaults={
                    'directory': monitored_dir_obj,
                    'file_hash': current_hash,
                    'last_modified': last_mod,
                    'last_scanned': timezone.now()
                }
            )

            if created:
                # NEW FILE DETECTED
                AuditLog.objects.create(
                    file_path=full_path,
                    change_type='NEW',
                    new_hash=current_hash,
                    is_resolved=False
                )
            else:
                # CHECK FOR MODIFICATIONS
                if record.file_hash != current_hash:
                    AuditLog.objects.create(
                        file_path=full_path,
                        change_type='MODIFIED',
                        old_hash=record.file_hash,
                        new_hash=current_hash,
                        is_resolved=False
                    )
                    # Update Record
                    record.file_hash = current_hash
                    record.last_modified = last_mod
                    record.last_scanned = timezone.now()
                    record.save()
                else:
                    # Update scan time
                    record.last_scanned = timezone.now()
                    record.save()

    # 2. Check for DELETED files
    deleted_records = FileRecord.objects.filter(directory=monitored_dir_obj).exclude(path__in=current_files)
    
    for rec in deleted_records:
        AuditLog.objects.create(
            file_path=rec.path,
            change_type='DELETED',
            old_hash=rec.file_hash,
            is_resolved=False
        )
        rec.delete()

def process_file_event(file_path, event_type, directory_obj):
    """
    Handles a single file event from the Real-Time Watcher.
    event_type: 'created', 'modified', 'deleted', 'moved'
    """
    # 1. Handle DELETION
    if event_type == 'deleted':
        try:
            rec = FileRecord.objects.get(path=file_path)
            AuditLog.objects.create(
                file_path=file_path,
                change_type='DELETED',
                old_hash=rec.file_hash,
                is_resolved=False
            )
            rec.delete()
        except FileRecord.DoesNotExist:
            pass
        return

    # 2. Handle CREATED / MODIFIED
    if not os.path.exists(file_path):
        return # Might have been deleted immediately after

    try:
        current_hash = calculate_file_hash(file_path)
        # Check Malware
        is_malware, reason = check_for_malware(file_path, current_hash)
        if is_malware:
             # De-duplicate alert logic if needed
             last_log = AuditLog.objects.filter(file_path=file_path).last()
             if not (last_log and last_log.change_type == 'MALWARE' and not last_log.is_resolved):
                AuditLog.objects.create(
                    file_path=file_path,
                    change_type='MALWARE',
                    new_hash=current_hash,
                    details=reason,
                    is_resolved=False
                )

        stat = os.stat(file_path)
        last_mod = stat.st_mtime

        record, created = FileRecord.objects.get_or_create(
            path=file_path,
            defaults={
                'directory': directory_obj,
                'file_hash': current_hash,
                'last_modified': last_mod,
                'last_scanned': timezone.now()
            }
        )

        if created:
             AuditLog.objects.create(
                file_path=file_path,
                change_type='NEW',
                new_hash=current_hash,
                is_resolved=False
            )
        else:
            if record.file_hash != current_hash:
                AuditLog.objects.create(
                    file_path=file_path,
                    change_type='MODIFIED',
                    old_hash=record.file_hash,
                    new_hash=current_hash,
                    is_resolved=False
                )
                record.file_hash = current_hash
                record.last_modified = last_mod
                record.last_scanned = timezone.now()
                record.save()
            else:
                record.last_scanned = timezone.now()
                record.save()

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


