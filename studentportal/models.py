from django.db import models
from django.contrib.auth.models import User  # Import User model to link with student

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link student to a user
    department = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    section = models.CharField(max_length=10)
    degree = models.CharField(max_length=100)
    batch = models.CharField(max_length=20)
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
class ToDoTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the student (user)
    task = models.CharField(max_length=255)  # Task description
    created_at = models.DateTimeField(auto_now_add=True)  # When the task was created
    completed = models.BooleanField(default=False)  # Whether the task is completed or not

    def __str__(self):
        return self.task

class Timetable(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timetables')
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

class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Discussion by {self.user.username} on {self.timestamp}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    remarks = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.user.first_name} - {self.date} - {'Present' if self.is_present else 'Absent'}"