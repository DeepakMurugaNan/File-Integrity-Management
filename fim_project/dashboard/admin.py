from django.contrib import admin
from .models import MonitoredDirectory, FileRecord, AuditLog, MalwareSignature

@admin.register(MonitoredDirectory)
class MonitoredDirectoryAdmin(admin.ModelAdmin):
    list_display = ('path', 'active', 'created_at')
    search_fields = ('path',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('change_type', 'file_path', 'detected_at', 'is_resolved')
    list_filter = ('change_type', 'is_resolved')
    search_fields = ('file_path',)

@admin.register(MalwareSignature)
class MalwareSignatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'signature_hash')
    search_fields = ('name', 'signature_hash')

# FileRecord is internal, but we can enable it for debugging if needed
@admin.register(FileRecord)
class FileRecordAdmin(admin.ModelAdmin):
    list_display = ('path', 'directory', 'last_scanned')
    search_fields = ('path',)
