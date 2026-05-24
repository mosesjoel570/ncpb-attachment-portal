from django.contrib import admin
from .models import AttachmentApplication

@admin.register(AttachmentApplication)
class AttachmentApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'institution', 'course', 'status', 'applied_on', 'approved_by')
    list_filter = ('status', 'current_year', 'applied_on')
    search_fields = ('first_name', 'last_name', 'email', 'institution', 'course')
    readonly_fields = ('student', 'applied_on', 'decision_date')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Education Details', {
            'fields': ('institution', 'course', 'current_year')
        }),
        ('Application Details', {
            'fields': ('proposed_department', 'attachment_duration_weeks', 'cover_letter', 'cv', 'academic_transcript')
        }),
        ('Approval', {
            'fields': ('status', 'approved_by', 'admin_comments', 'applied_on', 'decision_date')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.status != 'pending' and not obj.approved_by:
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)

