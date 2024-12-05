from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from datetime import datetime
from .models import Student
from .models import ToDoTask
from .models import Timetable
from .models import Discussion
from teacherportal.models import Attendance,Resource,Marks

from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json
import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor


# Student Portal HomePage
def dashboard(request):
    # Get the current date
    current_date = datetime.now().strftime("%B %d, %Y")

    # Assuming you have a model called Student and the user is a student
    student = Student.objects.get(user=request.user)  # Assuming Student model has a One-to-One relation with User
    
    context = {
        'current_date': current_date,
        'student': student,
    }
    
    return render(request, 'dashboard.html', context)


# student_attendance
def student_attendance(request):
    # Get the logged-in student's record
    student = Student.objects.get(user=request.user)
    
    # Fetch attendance records for the logged-in student
    attendance_records = Attendance.objects.filter(student=student).select_related('student', 'student__user')
    
    # Pass student's name and roll number to the template
    context = {
        'attendance_records': attendance_records,
        'student_name': student.user.first_name + " " + student.user.last_name,
        'roll_no': student.roll_no
    }

    return render(request, 'studentattendance.html', context)
def myteacher(request):
    # URL to scrape
    url = "http://pwr.nu.edu.pk/cs-faculty/"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Initialize an empty list to store faculty data
    faculty_data = []
    
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = bs(response.content, 'html.parser')
        
        # Find all faculty members
        faculty_members = soup.find_all('div', class_='faculty-member')

        # Define a function to extract individual faculty member data
        def scrape_faculty_member(faculty):
            try:
                name = faculty.find('h2').text.strip()
                position = faculty.find_all('p')[0].text.strip()
                email = faculty.find_all('p')[1].text.strip()
                phone = faculty.find_all('p')[2].text.strip() if len(faculty.find_all('p')) > 2 else "Not available"
                
                return {
                    'name': name,
                    'position': position,
                    'email': email,
                    'phone': phone
                }
            except Exception as e:
                # In case of an error, return None
                return None
        
        # Use ThreadPoolExecutor to process faculty members concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Map the scraping function over the list of faculty members
            faculty_data = list(executor.map(scrape_faculty_member, faculty_members))
    
    # Filter out any None values (in case of any errors)
    faculty_data = [faculty for faculty in faculty_data if faculty]

    # Group the faculty data by position
    grouped_faculty = {}
    for faculty in faculty_data:
        position = faculty['position']
        if position not in grouped_faculty:
            grouped_faculty[position] = []
        grouped_faculty[position].append(faculty)

    # Pass the grouped data to the template
    return render(request, "myteacher.html", {'grouped_faculty': grouped_faculty})


# learning Resources

# todoVault
def todo_vault(request):
    tasks = ToDoTask.objects.filter(user=request.user)  # Get tasks for the logged-in user

    if request.method == 'POST':
        task = request.POST.get('task')
        if task:
            ToDoTask.objects.create(user=request.user, task=task)  # Create new task
            return redirect('todovault')  # Redirect to the same page after adding task

    return render(request, 'todovault.html', {
        'tasks': tasks,  # Pass tasks to the template
    })

def delete_task(request, task_id):
    task = ToDoTask.objects.get(id=task_id, user=request.user)  # Get task to delete
    if task:
        task.delete()  # Delete the task
    return redirect('todovault')

# Mytimetable Student
def my_timetable(request):
    timetable = Timetable.objects.all()
    # Sort the timetable manually by the day order and then by time
    sorted_timetable = sorted(
        timetable,
        key=lambda entry: (Timetable.get_day_order(entry.day), entry.time)
    )
    return render(request, 'mytimetable.html', {'timetable': sorted_timetable})


def discussion_view(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        parent_id = request.POST.get('parent_id')

        # If parent_id is provided, create a reply
        if parent_id:
            parent_message = Discussion.objects.get(id=parent_id)
            Discussion.objects.create(user=request.user, content=message_content, parent=parent_message)
        else:
            # Otherwise, create a new discussion
            Discussion.objects.create(user=request.user, content=message_content)

    # Fetch all discussions and their replies
    discussions = Discussion.objects.filter(parent__isnull=True)  # Fetch only parent discussions
    return render(request, 'discussion.html', {'messages': discussions})

def delete_message(request, message_id):
    # Get the message object, or return a 404 error if not found
    message = get_object_or_404(Discussion, id=message_id)

    # Check if the logged-in user is the owner of the message
    if message.user == request.user:
        message.delete()  # Delete the message
        return redirect('discussion')  # Redirect to the discussion page

    # If the user is not the owner, you can handle the error or just redirect
    return redirect('discussion')  # You can replace this with error handling logic


def learning_resources(request):
    resources = Resource.objects.all()  # Fetch all resources
    return render(request, 'learningResources.html', {'resources': resources})


def view_marks(request):
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        # Get the logged-in student's marks
        student = request.user.student
        marks = Marks.objects.filter(student=student).order_by('-date_awarded')  # Order by most recent
        return render(request, 'view_marks.html', {'marks': marks})
    else:
        return redirect('login')  # Redirect to login if not a student