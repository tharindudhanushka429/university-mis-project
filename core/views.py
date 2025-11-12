from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import (
    Course, Student, Enrollment, Lecturer, Attendance,
    Assessment, StudentMark, Payment
)

# -----------------
# Public Views
# -----------------
def home_page(request):
    return render(request, 'core/home.html')

def course_list(request):
    courses = Course.objects.all().order_by('code')
    context = { 'course_list': courses }
    return render(request, 'core/course_list.html', context)

def student_report_search(request):
    # (මෙම වාර්තාව තවදුරටත් ක්‍රියා නොකරනු ඇත, 
    # මක්නිසාද 'Enrollment' හි 'grade' ක්ෂේත්‍රය වෙනස් වී ඇත. 
    # නමුත් අපි එය දැනට මෙසේම තබමු.)
    context = {}
    if request.method == 'GET' and 'student_id_query' in request.GET:
        query = request.GET.get('student_id_query')
        try:
            student = Student.objects.get(student_id=query)
            enrollments = Enrollment.objects.filter(student=student)
            context['student_found'] = student
            context['enrollments_list'] = enrollments
        except Student.DoesNotExist:
            context['error_message'] = f"Student ID '{query}' not found."
    return render(request, 'core/student_report.html', context)

def lecturer_report_search(request):
    all_lecturers = Lecturer.objects.all()
    context = { 'all_lecturers_list': all_lecturers }
    if request.method == 'GET' and 'lecturer_query' in request.GET:
        query_id = request.GET.get('lecturer_query')
        if query_id:
            try:
                lecturer = Lecturer.objects.get(id=query_id)
                courses_taught = Course.objects.filter(lecturer=lecturer)
                context['lecturer_found'] = lecturer
                context['courses_taught_list'] = courses_taught
            except Lecturer.DoesNotExist:
                context['error_message'] = f"Lecturer with ID '{query_id}' not found."
    return render(request, 'core/lecturer_report.html', context)


# -----------------
# Student Dashboard & Calculation Views
# -----------------
@login_required
def student_dashboard(request):
    try:
        student = request.user.student
        
        # ශිෂ්‍යයා ලියාපදිංචි වූ පාඨමාලා (Enrollments)
        enrollments = Enrollment.objects.filter(student=student).order_by('course__semester', 'course__code')
        
        # පැමිණීමේ වාර්තා (Attendance)
        attendance_records = Attendance.objects.filter(student=student).order_by('-date')
        
        
        payments = Payment.objects.filter(student=student).order_by('status', '-due_date') # Pending ඒවා මුලින් පෙන්වයි
        
        # SGPA සහ CGPA ගණනය කිරීම
        sgpa_s1 = student.calculate_sgpa(semester=1)
        sgpa_s2 = student.calculate_sgpa(semester=2) # 2nd Semester එකක් ඇතැයි උපකල්පනය කරමු
        cgpa = student.calculate_cgpa()
        
        context = {
            'student': student,
            'enrollments_list': enrollments,
            'attendance_list': attendance_records,
            'sgpa_s1': sgpa_s1,
            'sgpa_s2': sgpa_s2,
            'cgpa': cgpa,
            'payment_list': payments,
        }
        return render(request, 'core/dashboard.html', context)
    
    except Student.DoesNotExist:
        # Admin කෙනෙක් ලොග් වුවහොත්, ඔහුව මුල් පිටුවට යොමු කිරීම
        return redirect('home')
    except AttributeError:
        # User ගිණුමක් නැති Student කෙනෙක් (මෙය සිදු නොවිය යුතුය)
        return redirect('home')

@login_required
def trigger_calculations(request):
    """ 
    ශිෂ්‍යයාගේ සියලුම ලකුණු, ශ්‍රේණි, සහ GP අගයන් 
    ස්වයංක්‍රීයව ගණනය කිරීම ආරම්භ කරයි (trigger)
    """
    try:
        student = request.user.student
        enrollments = student.enrollment_set.all()
        
        # ශිෂ්‍යයා ලියාපදිංචි වී ඇති සෑම පාඨමාලාවක් සඳහාම
        for enrollment in enrollments:
            # calculate_final_mark() function එක ක්‍රියාත්මක කිරීම
            enrollment.calculate_final_mark() 
            
        # ගණනය කිරීම් අවසන් වූ පසු, නැවත Dashboard එකට යොමු කිරීම
        return redirect('student-dashboard')
        
    except Student.DoesNotExist:
        return redirect('home')