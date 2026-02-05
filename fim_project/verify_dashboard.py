import os
import sys
import django
from django.test import RequestFactory
from django.urls import reverse

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fim_project.settings')
django.setup()

from dashboard.views import dashboard_home
from dashboard.models import MonitoredDirectory, AuditLog

def test_dashboard_view():
    # Setup Data
    MonitoredDirectory.objects.create(path="/test/path/dashboard", active=True)
    AuditLog.objects.create(file_path="/test/path/file.txt", change_type='NEW', is_resolved=False)

    # Create Request
    factory = RequestFactory()
    request = factory.get('/')
    
    # Get Response
    response = dashboard_home(request)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        if "FIM Dashboard" in content:
            print("SUCCESS: Dashboard title found.")
        else:
            print("FAILURE: Dashboard title not found.")
            
        if "Recent Activity" in content:
            print("SUCCESS: Recent Activity section found.")
            
        if "NEW" in content:
            print("SUCCESS: Log entry found.")
    else:
        print("FAILURE: Status code is not 200")

    # Clean up (Optional, since these are DB calls that persist)
    # Ideally should use TestCase, but this is a quick script
    MonitoredDirectory.objects.filter(path="/test/path/dashboard").delete()
    AuditLog.objects.filter(file_path="/test/path/file.txt").delete()

if __name__ == "__main__":
    test_dashboard_view()
