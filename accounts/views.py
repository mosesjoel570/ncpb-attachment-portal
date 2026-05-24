from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


def register(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required.')
        elif len(username) < 4:
            errors.append('Username must be at least 4 characters.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
            
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already exists.')
            
        if not password:
            errors.append('Password is required.')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters.')
            
        if password != password_confirm:
            errors.append('Passwords do not match.')
        
        if errors:
            return render(request, 'register.html', {'errors': errors})
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        except IntegrityError:
            errors.append('An error occurred during registration.')
            return render(request, 'register.html', {'errors': errors})

    return render(request, 'register.html')


def user_login(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            return render(request, 'login.html', {'error': 'Username and password are required.'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard(request):
    """User dashboard - redirect to appropriate panel"""
    if request.user.is_staff and request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('student_dashboard')


def user_logout(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')