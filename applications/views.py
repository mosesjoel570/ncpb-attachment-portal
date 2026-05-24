from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.http import Http404
from .models import AttachmentApplication
from django.core.paginator import Paginator

def is_admin_user(user):
    """Check if user is admin staff"""
    return user.is_staff and user.is_superuser

# =============================================
# STUDENT VIEWS
# =============================================

@login_required(login_url='login')
def student_dashboard(request):
    """Student dashboard to manage their applications"""
    applications = AttachmentApplication.objects.filter(student=request.user).order_by('-applied_on')
    
    # Statistics
    total_apps = applications.count()
    pending = applications.filter(status='pending').count()
    approved = applications.filter(status='approved').count()
    rejected = applications.filter(status='rejected').count()
    
    context = {
        'applications': applications,
        'total_apps': total_apps,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'user_type': 'student'
    }
    
    return render(request, 'applications/student_dashboard.html', context)

@login_required(login_url='login')
def apply_attachment(request):
    """Form for students to apply for attachment"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        institution = request.POST.get('institution', '').strip()
        course = request.POST.get('course', '').strip()
        current_year = request.POST.get('current_year', '')
        proposed_department = request.POST.get('proposed_department', '').strip()
        attachment_duration_weeks = request.POST.get('attachment_duration_weeks', '8')
        cover_letter = request.POST.get('cover_letter', '').strip()
        
        # File uploads
        cv = request.FILES.get('cv')
        academic_transcript = request.FILES.get('academic_transcript')
        
        # Validation
        errors = []
        if not all([first_name, last_name, phone, institution, course, current_year, 
                    proposed_department, cover_letter, cv]):
            errors.append('All fields except academic transcript are required.')
        
        if cv and cv.size > 5242880:  # 5MB limit
            errors.append('CV file size must not exceed 5MB.')
        
        if academic_transcript and academic_transcript.size > 5242880:
            errors.append('Academic transcript file size must not exceed 5MB.')
        
        if errors:
            return render(request, 'applications/apply_attachment.html', {
                'errors': errors,
                'user_type': 'student'
            })
        
        # Create application
        application = AttachmentApplication(
            student=request.user,
            first_name=first_name,
            last_name=last_name,
            email=request.user.email,
            phone=phone,
            institution=institution,
            course=course,
            current_year=int(current_year),
            proposed_department=proposed_department,
            attachment_duration_weeks=int(attachment_duration_weeks),
            cover_letter=cover_letter,
            cv=cv,
            academic_transcript=academic_transcript
        )
        application.save()
        
        messages.success(request, 'Application submitted successfully! Admin will review it shortly.')
        return redirect('student_dashboard')
    
    return render(request, 'applications/apply_attachment.html', {'user_type': 'student'})

@login_required(login_url='login')
def view_application(request, app_id):
    """View a specific application"""
    application = get_object_or_404(AttachmentApplication, id=app_id)
    
    # Check if user owns this application or is admin
    if application.student != request.user and not (request.user.is_staff and request.user.is_superuser):
        raise Http404("Application not found")
    
    context = {
        'application': application,
        'is_admin': request.user.is_staff and request.user.is_superuser,
        'user_type': 'admin' if request.user.is_staff else 'student'
    }
    
    return render(request, 'applications/view_application.html', context)

@login_required(login_url='login')
def withdraw_application(request, app_id):
    """Student withdraws their application"""
    application = get_object_or_404(AttachmentApplication, id=app_id, student=request.user)
    
    if application.status == 'pending':
        application.status = 'withdrawn'
        application.save()
        messages.success(request, 'Application withdrawn successfully.')
    else:
        messages.error(request, 'You can only withdraw pending applications.')
    
    return redirect('student_dashboard')

# =============================================
# ADMIN VIEWS
# =============================================

@login_required(login_url='login')
@user_passes_test(is_admin_user)
def admin_dashboard(request):
    """Admin dashboard to manage all applications"""
    applications = AttachmentApplication.objects.all().order_by('-applied_on')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    applications = paginator.get_page(page_number)
    
    # Statistics
    total_apps = AttachmentApplication.objects.count()
    pending = AttachmentApplication.objects.filter(status='pending').count()
    approved = AttachmentApplication.objects.filter(status='approved').count()
    rejected = AttachmentApplication.objects.filter(status='rejected').count()
    
    context = {
        'applications': applications,
        'total_apps': total_apps,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'status_filter': status_filter,
        'user_type': 'admin'
    }
    
    return render(request, 'applications/admin_dashboard.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin_user)
def approve_application(request, app_id):
    """Approve an application"""
    application = get_object_or_404(AttachmentApplication, id=app_id)
    
    if request.method == 'POST':
        admin_comments = request.POST.get('admin_comments', '').strip()
        
        application.status = 'approved'
        application.approved_by = request.user
        application.decision_date = timezone.now()
        application.admin_comments = admin_comments
        application.save()
        
        messages.success(request, f'Application from {application.full_name} has been approved!')
        return redirect('admin_dashboard')
    
    context = {
        'application': application,
        'action': 'approve',
        'user_type': 'admin'
    }
    
    return render(request, 'applications/review_application.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin_user)
def reject_application(request, app_id):
    """Reject an application"""
    application = get_object_or_404(AttachmentApplication, id=app_id)
    
    if request.method == 'POST':
        admin_comments = request.POST.get('admin_comments', '').strip()
        
        if not admin_comments:
            messages.error(request, 'Please provide rejection comments.')
            return redirect('reject_application', app_id=app_id)
        
        application.status = 'rejected'
        application.approved_by = request.user
        application.decision_date = timezone.now()
        application.admin_comments = admin_comments
        application.save()
        
        messages.success(request, f'Application from {application.full_name} has been rejected.')
        return redirect('admin_dashboard')
    
    context = {
        'application': application,
        'action': 'reject',
        'user_type': 'admin'
    }
    
    return render(request, 'applications/review_application.html', context)

