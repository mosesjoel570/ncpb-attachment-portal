from django.db import models
from django.contrib.auth.models import User

# Application Status Choices
STATUS_CHOICES = [
    ('pending', 'Pending Review'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('withdrawn', 'Withdrawn'),
]

class AttachmentApplication(models.Model):
    """Model for student attachment applications"""
    
    # Student information
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Education details
    institution = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    current_year = models.IntegerField(choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3'), (4, 'Year 4')])
    
    # Application details
    proposed_department = models.CharField(max_length=255)
    attachment_duration_weeks = models.IntegerField(default=8)
    cover_letter = models.TextField()
    
    # File uploads
    cv = models.FileField(upload_to='applications/cv/%Y/%m/%d/')
    academic_transcript = models.FileField(upload_to='applications/transcripts/%Y/%m/%d/', null=True, blank=True)
    
    # Status and approval
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    decision_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_applications')
    admin_comments = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-applied_on']
        verbose_name = 'Attachment Application'
        verbose_name_plural = 'Attachment Applications'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_status_display()}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

