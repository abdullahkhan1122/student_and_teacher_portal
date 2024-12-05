# teacherportal/models.py
from django.db import models
from studentportal.models import Student
from django.contrib.auth.models import User  # Import User model to link with student

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', null=True)
    students = models.ManyToManyField('studentportal.Student', related_name='teachers')
    subject = models.CharField(max_length=100)
    hire_date = models.DateField()
    qualification = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.user.get_full_name()

    def get_students(self):
        """Fetch all students assigned to this teacher."""
        return self.students.all()

class Attendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()  # Date of attendance
    is_present = models.BooleanField(default=False)  # Present/Absent status
    remarks = models.CharField(max_length=200, blank=True, null=True)  # Additional remarks

    class Meta:
        unique_together = ('student', 'date')  # Prevent duplicate entries for the same student and date

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.date} - {'Present' if self.is_present else 'Absent'}"



class TeacherTimetable(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_timetables')
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    time = models.TimeField()
    subject = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['day', 'time']

    def __str__(self):
        return f"{self.day} {self.time} - {self.subject}"

    @staticmethod
    def get_day_order(day):
        """Maps days to numerical values."""
        day_order = {
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6,
            'Sunday': 7,
        }
        return day_order.get(day, 8)  # Default to 8 for invalid days



class Resource(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Marks(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)
    date_awarded = models.DateField()

    class Meta:
        unique_together = ('teacher', 'student', 'date_awarded')  # Ensure no duplicate entries
        ordering = ['-date_awarded']  # Sort by the latest date

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.marks} marks on {self.date_awarded}"
