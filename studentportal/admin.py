from django.contrib import admin
from .models import Student
from .models import Timetable
from .models import Discussion

admin.site.register(Student)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('student', 'day', 'time', 'subject', 'location')
    list_filter = ('day', 'student')
    search_fields = ('student__username', 'subject')
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('student', 'day', 'time', 'subject', 'location')
    list_filter = ('day', 'student')
    search_fields = ('student__username', 'subject')
    def __str__(self):  
        return f"{self.student.username} - {self.day} - {self.subject}"
admin.site.register(Discussion)
