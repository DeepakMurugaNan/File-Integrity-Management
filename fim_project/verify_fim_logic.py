import os
import sys
import django
import time

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fim_project.settings')
django.setup()

from dashboard.models import MonitoredDirectory, FileRecord, AuditLog
from dashboard.utils import scan_directory_and_check

# 1. Setup Test Directory
TEST_DIR = os.path.join(os.getcwd(), 'fim_test_zone')
if not os.path.exists(TEST_DIR):
    os.makedirs(TEST_DIR)

# Clean DB for this test path
MonitoredDirectory.objects.filter(path=TEST_DIR).delete()

# Create MonitoredDirectory
mon_dir = MonitoredDirectory.objects.create(path=TEST_DIR, active=True)
print(f"Monitored Directory Created: {TEST_DIR}")

# 2. Add a file (Initial State)
file_a = os.path.join(TEST_DIR, 'file_a.txt')
with open(file_a, 'w') as f:
    f.write("Version 1")

print("Created file_a.txt")

# 3. First Scan (Should detect NEW)
scan_directory_and_check(mon_dir)
print("Scan 1 Complete.")

# Verify AuditLog
logs = AuditLog.objects.filter(file_path=file_a).order_by('-detected_at')
if logs.exists() and logs.first().change_type == 'NEW':
    print("SUCCESS: Detected NEW file.")
else:
    print("FAILURE: Did not detect NEW file.")

# 4. Modify file
time.sleep(1.1) # Ensure timestamp differs significantly for FS granularity
with open(file_a, 'w') as f:
    f.write("Version 2 (Modified)")
print("Modified file_a.txt")

# 5. Second Scan (Should detect MODIFIED)
scan_directory_and_check(mon_dir)
print("Scan 2 Complete.")

# Verify AuditLog
logs = AuditLog.objects.filter(file_path=file_a).order_by('-detected_at')
latest_log = logs.first()
if latest_log.change_type == 'MODIFIED':
    print("SUCCESS: Detected MODIFIED file.")
else:
    print(f"FAILURE: Expected MODIFIED, got {latest_log.change_type}")

# 6. Delete file
os.remove(file_a)
print("Deleted file_a.txt")

# 7. Third Scan (Should detect DELETED)
scan_directory_and_check(mon_dir)
print("Scan 3 Complete.")

# Verify AuditLog
logs = AuditLog.objects.filter(file_path=file_a).order_by('-detected_at')
latest_log = logs.first()
if latest_log.change_type == 'DELETED':
    print("SUCCESS: Detected DELETED file.")
else:
    print(f"FAILURE: Expected DELETED, got {latest_log.change_type}")

# Cleanup
MonitoredDirectory.objects.filter(path=TEST_DIR).delete()
if os.path.exists(TEST_DIR):
    try:
        os.rmdir(TEST_DIR)
    except:
        pass
print("Test Complete.")
