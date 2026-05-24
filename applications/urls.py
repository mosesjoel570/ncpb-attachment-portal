from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('apply/', views.apply_attachment, name='apply_attachment'),
    path('<int:app_id>/', views.view_application, name='view_application'),
    path('<int:app_id>/withdraw/', views.withdraw_application, name='withdraw_application'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('admin/reject/<int:app_id>/', views.reject_application, name='reject_application'),
]

