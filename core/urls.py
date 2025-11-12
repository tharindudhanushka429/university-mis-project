from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public & Home
    path('', views.home_page, name='home'), 
    
    # Auth (Login / Logout)
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Student Dashboard
    path('dashboard/', views.student_dashboard, name='student-dashboard'),
    
    # --- අලුත් ---
    # Dashboard එකේ "Calculate My Marks" බොත්තම (button) සඳහා
    path('dashboard/calculate/', views.trigger_calculations, name='trigger-calculations'),

    # Public Reports
    path('courses/', views.course_list, name='course-list'),
    path('student_report/', views.student_report_search, name='student-report-search'),
    path('lecturer_report/', views.lecturer_report_search, name='lecturer-report-search'),
]