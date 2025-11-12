from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# -----------------
# 1. Lecturer Model
# -----------------
class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name

# -----------------
# 2. Course Model (Credits සහ Semester සමඟ)
# -----------------
class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True, blank=True)
    credits = models.PositiveIntegerField(default=3) # පාඨමාලා ඒකක (Credits)
    semester = models.PositiveIntegerField(default=1) # කුමන වාරයද (Semester)
    
    def __str__(self):
        return f"{self.code}: {self.name}"

# -----------------
# 3. Student Model (GPA ගණනය කිරීමේ තර්කනය සමඟ)
# -----------------
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.name}"

    def calculate_sgpa(self, semester):
        """ මෙම ශිෂ්‍යයාගේ, ලබා දෙන වාරය (semester) සඳහා SGPA ගණනය කරයි """
        
        # එම වාරයට අදාළව ලියාපදිංචි වූ පාඨමාලා (Enrollments)
        semester_enrollments = self.enrollment_set.filter(course__semester=semester)
        
        total_credit_points = Decimal('0.0')
        total_credits = Decimal('0.0')

        for enrollment in semester_enrollments:
            if enrollment.grade_point is not None:
                course_credits = Decimal(str(enrollment.course.credits))
                total_credit_points += (enrollment.grade_point * course_credits)
                total_credits += course_credits
        
        if total_credits == 0:
            return Decimal('0.00')
        
        sgpa = total_credit_points / total_credits
        return sgpa.quantize(Decimal('0.01')) # දශමස්ථාන 2කට

    def calculate_cgpa(self):
        """ මෙම ශිෂ්‍යයාගේ සමස්ත CGPA ගණනය කරයි """
        all_enrollments = self.enrollment_set.all()
        
        total_credit_points = Decimal('0.0')
        total_credits = Decimal('0.0')

        for enrollment in all_enrollments:
            if enrollment.grade_point is not None:
                course_credits = Decimal(str(enrollment.course.credits))
                total_credit_points += (enrollment.grade_point * course_credits)
                total_credits += course_credits
        
        if total_credits == 0:
            return Decimal('0.00')
            
        cgpa = total_credit_points / total_credits
        return cgpa.quantize(Decimal('0.01')) # දශමස්ථාන 2කට

# -----------------
# 4. Assessment Model (CA කොටස් නිර්වචනය කිරීම)
# -----------------
class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # උදා: "Quizzes", "Midterm", "Final Exam"
    weight = models.PositiveIntegerField() # උදා: 20 (එනම් 20%)

    def __str__(self):
        return f"{self.course.code} - {self.name} ({self.weight}%)"

# -----------------
# 5. StudentMark Model (CA ලකුණු ගබඩා කිරීම)
# -----------------
class StudentMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2) # 100න් ලබා ගත් ලකුණු

    class Meta:
        unique_together = ('student', 'assessment')

    def __str__(self):
        return f"{self.student.student_id} - {self.assessment.name}: {self.marks}"

# -----------------
# 6. Enrollment Model (Final Grade ගණනය කිරීමේ තර්කනය සමඟ)
# -----------------
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    # ස්වයංක්‍රීයව ගණනය වන ක්ෂේත්‍ර
    final_mark = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    final_grade = models.CharField(max_length=2, null=True, blank=True) # A+, B- etc.
    grade_point = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True) # 4.0, 3.7 etc.

    class Meta:
        unique_together = ('student', 'course') 

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.name}"

    def get_grade_from_mark(self, mark):
        """ ලකුණ (Mark) ශ්‍රේණිය (Grade) සහ ශ්‍රේණි ලක්ෂ්‍යය (GP) බවට පරිවර්තනය කරයි """
        if mark >= 85: return ('A+', Decimal('4.00'))
        if mark >= 80: return ('A',  Decimal('4.00'))
        if mark >= 75: return ('A-', Decimal('3.70'))
        if mark >= 70: return ('B+', Decimal('3.30'))
        if mark >= 65: return ('B',  Decimal('3.00'))
        if mark >= 60: return ('B-', Decimal('2.70'))
        if mark >= 55: return ('C+', Decimal('2.30'))
        if mark >= 50: return ('C',  Decimal('2.00'))
        if mark >= 45: return ('C-', Decimal('1.70'))
        if mark >= 40: return ('D+', Decimal('1.30'))
        if mark >= 35: return ('D',  Decimal('1.00'))
        return ('E', Decimal('0.00')) # Fail

    def calculate_final_mark(self):
        """ මෙම පාඨමාලාව සඳහා ශිෂ්‍යයාගේ අවසාන ලකුණ (Final Mark) ගණනය කරයි """
        
        # මෙම පාඨමාලාවට අදාළ සියලුම Assessments (CA කොටස්)
        assessments = self.course.assessment_set.all()
        # මෙම ශිෂ්‍යයාගේ, මෙම පාඨමාලාවේ Assessments සඳහා ලකුණු
        student_marks = self.student.studentmark_set.filter(assessment__in=assessments)

        total_weighted_mark = Decimal('0.0')
        total_weight = Decimal('0.0')

        for mark in student_marks:
            weight = Decimal(str(mark.assessment.weight))
            total_weighted_mark += (mark.marks * (weight / Decimal('100.0')))
            total_weight += weight

        # සියලුම CA කොටස් සඳහා ලකුණු ඇතුළත් කර ඇත්නම් (උදා: 100% ක්ම)
        if total_weight == 100:
            self.final_mark = total_weighted_mark.quantize(Decimal('0.01'))
            grade, gp = self.get_grade_from_mark(self.final_mark)
            self.final_grade = grade
            self.grade_point = gp
        else:
            # තවමත් සියලුම ලකුණු ඇතුළත් කර නැත්නම්
            self.final_mark = None
            self.final_grade = "Pending"
            self.grade_point = None
        
        self.save() # ගණනය කළ අගයන් දත්ත සමුදායේ (DB) සටහන් කිරීම
        return self.final_mark

# -----------------
# 7. Attendance Model (වෙනසක් නැත)
# -----------------
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    STATUS_CHOICES = [('P', 'Present'), ('A', 'Absent')]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student.student_id} - {self.course.code} on {self.date}: {self.get_status_display()}"
        
# --- පහත කේතය core/models.py ගොනුවේ අවසානයටම එකතු කරන්න ---

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.CharField(max_length=200) # උදා: "Library Fine", "Exam Fee - Sem 1"
    amount = models.DecimalField(max_digits=10, decimal_places=2) # මුදල
    due_date = models.DateField(null=True, blank=True) # ගෙවිය යුතු අවසන් දිනය
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'), # ගෙවීමට ඇත
        ('Paid', 'Paid'),     # ගෙවා ඇත
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.student.student_id} - {self.description}: {self.amount} ({self.status})"