from django.contrib import admin
from .models import (
    Student, Course, Lecturer, Enrollment, Attendance,
    Assessment, StudentMark, Payment
)

# --- Admin Panel එක පහසු කිරීමට Inlines ---

class AssessmentInline(admin.TabularInline):
    """ Course Admin පිටුවේම CA කොටස් (Assessments) ඇතුළත් කිරීමට """
    model = Assessment
    extra = 1 # අලුතින් එකතු කිරීමට පෙන්වන හිස් තැන් ගණන

class StudentMarkInline(admin.TabularInline):
    """ Student Admin පිටුවේම ලකුණු (Marks) ඇතුළත් කිරීමට """
    model = StudentMark
    extra = 0

# --- Model Admin සැකසුම් ---

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'lecturer', 'credits', 'semester')
    search_fields = ('code', 'name')
    list_filter = ('semester', 'credits')
    inlines = [AssessmentInline] # Course එක සාදන විටම CA කොටස් ද සෑදීමට

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email', 'user')
    search_fields = ('student_id', 'name')
    inlines = [StudentMarkInline] # Student පිටුවේම ලකුණු බැලීමට/ඇතුළත් කිරීමට

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'final_mark', 'final_grade', 'grade_point')
    # ගණනය කළ ක්ෂේත්‍ර Admin Panel එකේ වෙනස් කළ නොහැකි ලෙස පෙන්වීම
    readonly_fields = ('final_mark', 'final_grade', 'grade_point') 
    list_filter = ('course', 'final_grade')
    search_fields = ('student__student_id', 'student__name')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'weight')
    list_filter = ('course',)

@admin.register(StudentMark)
class StudentMarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'assessment_name', 'marks')
    search_fields = ('student__student_id', 'student__name')
    list_filter = ('assessment__course',)

    @admin.display(description='Assessment')
    def assessment_name(self, obj):
        return obj.assessment

# --- අනෙක් Models ලියාපදිංචි කිරීම ---
admin.site.register(Lecturer)
admin.site.register(Attendance)

# --- පහත කේතය core/admin.py ගොනුවේ අවසානයටම එකතු කරන්න ---

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'description', 'amount', 'status', 'due_date')
    list_filter = ('status', 'due_date')
    search_fields = ('student__student_id', 'student__name', 'description')