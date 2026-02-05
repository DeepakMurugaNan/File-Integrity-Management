from django.shortcuts import render
from .models import MonitoredDirectory, FileRecord, AuditLog

def dashboard_home(request):
    """
    Main dashboard view.
    """
    directories = MonitoredDirectory.objects.all()
    # Stats
    total_files = FileRecord.objects.count()
    recent_logs = AuditLog.objects.order_by('-detected_at')[:50]
    
    # Simple alert counts
    alerts_count = AuditLog.objects.filter(is_resolved=False).count()

    context = {
        'directories': directories,
        'total_files': total_files,
        'recent_logs': recent_logs,
        'alerts_count': alerts_count,
    }
    return render(request, 'dashboard/home.html', context)
