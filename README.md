# NCPB Online Attachment Portal

A professional Django web application for managing attachment applications for the National Cereals and Produce Board (NCPB).

## 🎯 Project Overview

The NCPB Online Attachment Portal is a complete Django application that provides:
- User registration with validation
- Secure user authentication
- Professional user dashboard
- Responsive design
- Modern UI/UX

## ✨ Features

### Authentication System
- **User Registration**: Create new accounts with email validation and password confirmation
- **User Login**: Secure login with error handling
- **User Logout**: Safe logout functionality with success messages
- **Protected Routes**: Dashboard requires authentication
- **Welcome Messages**: Personalized greeting with user's name

### Form Validation
- Username must be 4+ characters and unique
- Email must be valid and unique
- Password must be 8+ characters
- Password confirmation must match
- Real-time error messaging

### User Interface
- **Professional Header**: Company logo and branding
- **Navigation Bar**: Responsive navigation with user-aware links
- **Dashboard**: Welcome screen with quick stats and guides
- **Alert System**: Success and error messages with close buttons
- **Responsive Design**: Mobile-friendly layout for all devices
- **Footer**: Company contact information

### Security Features
- CSRF protection on all forms
- Password hashing with Django's built-in system
- Authentication decorators on protected views
- Session management

## 🛠️ Technology Stack

- **Framework**: Django 6.0.5
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3
- **Python Version**: 3.x

## 📁 Project Structure

```
NCPB_Attachment_Portal/
├── ncpb_portal/           # Project settings and configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL router
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── accounts/              # User authentication app
│   ├── views.py           # Auth views (register, login, logout, dashboard)
│   ├── urls.py            # Auth routes
│   ├── models.py          # User models (uses Django auth)
│   └── admin.py           # Django admin configuration
├── applications/          # Application management app
│   ├── views.py           # Application views
│   ├── models.py          # Application models
│   └── urls.py            # Application routes
├── core/                  # Core app
│   ├── views.py           # Home view
│   └── urls.py            # Core routes
├── templates/             # HTML templates
│   ├── base.html          # Base template with header/footer
│   ├── home.html          # Home page
│   ├── register.html      # Registration page
│   ├── login.html         # Login page
│   └── dashboard.html     # User dashboard
├── static/                # Static files
│   └── css/
│       └── style.css      # Main stylesheet
├── db.sqlite3             # Database file
├── manage.py              # Django management script
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Virtual environment (venv)

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd NCPB_Attachment_Portal
   ```

2. **Activate the virtual environment**:
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies** (if not already installed):
   ```bash
   pip install django==6.0.5
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

## 📝 Usage

### Registration
1. Click "Register" on the home page or navigation
2. Fill in username (4+ characters), email, and password (8+ characters)
3. Confirm password
4. Click "Register Account"
5. You'll be redirected to the login page with a success message

### Login
1. Click "Login" in the navigation
2. Enter your username and password
3. Click "Login"
4. You'll be taken to your dashboard

### Dashboard
- View your profile information
- See application statistics
- Access quick guides
- Use navigation links to manage applications

### Logout
- Click "Logout" in the top navigation
- You'll be redirected to the home page

## 🔒 Security Features

- **Password Hashing**: Passwords are hashed using Django's built-in algorithm
- **CSRF Protection**: All forms are protected against CSRF attacks
- **Session Management**: Secure session handling
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping prevents XSS attacks
- **Authentication Required**: Dashboard requires login via @login_required decorator

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🎨 Color Scheme

- **Primary**: #1e5a8e (Professional Blue)
- **Secondary**: #d4a574 (Gold/Accent)
- **Success**: #27ae60 (Green)
- **Danger**: #e74c3c (Red)
- **Warning**: #f39c12 (Orange)

## 📧 Contact & Support

For support or inquiries:
- **Email**: info@ncpb.co.ke
- **Phone**: +254 (0) 20 2720000

## 🔄 Testing Checklist

✅ User Registration - Form validation working
✅ User Login - Authentication working
✅ Dashboard Access - Protected route working
✅ Logout - Session management working
✅ Navigation - Links rendering correctly
✅ Responsive Design - Mobile friendly
✅ Error Messages - Displaying correctly
✅ Success Messages - Displaying correctly
✅ Form Validation - All validations working

## 📝 Notes

- Development mode is enabled (DEBUG=True) for development purposes
- For production, update settings:
  - Set DEBUG=False
  - Update ALLOWED_HOSTS with your domain
  - Use a production WSGI server
  - Update SECRET_KEY to a secure random value
  - Use a production database (PostgreSQL recommended)

## 🆘 Troubleshooting

### Django not found error
- Ensure virtual environment is activated
- Reinstall Django: `pip install django==6.0.5`

### Database issues
- Run migrations: `python manage.py migrate`
- Reset database: `rm db.sqlite3` then `python manage.py migrate`

### Template not found errors
- Ensure templates are in the `templates/` directory
- Check TEMPLATES setting in settings.py

### Static files not loading
- Run: `python manage.py collectstatic`
- Check STATIC_URL and STATICFILES_DIRS in settings.py

## 📄 License

© 2024 National Cereals and Produce Board. All rights reserved.

## 🤝 Contributing

For contributions or improvements, please contact the development team.

---

**Last Updated**: May 2024
**Version**: 1.0
**Status**: Production Ready ✅
