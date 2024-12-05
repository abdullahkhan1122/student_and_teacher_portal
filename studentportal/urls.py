# studentportal/urls.py
from django.urls import path
from studentportal import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('todovault/', views.todo_vault, name='todovault'),
    path('todo/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    # path('discussion/', views.discussion, name='discussion'),
    path('myteacher/', views.myteacher, name='myteacher'),
    path('learningresources/', views.learning_resources, name='learningresources'),
    path('attendance/', views.student_attendance, name='student_attendance'),
    path('timetable/', views.my_timetable, name='my_timetable'),
    path('discussion/', views.discussion_view, name='discussion'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('view_marks/', views.view_marks, name='discussion'),

]
