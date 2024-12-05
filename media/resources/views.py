from django.shortcuts import render, redirect , get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt

def dashboard(request):
    
    current_date = datetime.now().strftime("%B %d, %Y")

    student = Student.objects.get(user=request.user)  
    
    context = {
        'current_date': current_date,
        'student': student,
    }
    
    return render(request, 'dashboard.html', context)



def student_attendance(request):
  
    student = Student.objects.get(user=request.user)
    

    attendance_records = Attendance.objects.filter(student=student).select_related('student', 'student__user')
    
   
    context = {
        'attendance_records': attendance_records,
        'student_name': student.user.first_name + " " + student.user.last_name,
        'roll_no': student.roll_no
    }

    return render(request, 'studentattendance.html', context)
def myteacher(request):
    
    url = "http://pwr.nu.edu.pk/cs-faculty/"
    
   
    response = requests.get(url)
    
  
    faculty_data = []
    
    if response.status_code == 200:
     
        soup = bs(response.content, 'html.parser')
        
      
        faculty_members = soup.find_all('div', class_='faculty-member')

       
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
              
                return None
        
     
        with ThreadPoolExecutor(max_workers=5) as executor:
   
            faculty_data = list(executor.map(scrape_faculty_member, faculty_members))
    
    
    faculty_data = [faculty for faculty in faculty_data if faculty]

   
    grouped_faculty = {}
    for faculty in faculty_data:
        position = faculty['position']
        if position not in grouped_faculty:
            grouped_faculty[position] = []
        grouped_faculty[position].append(faculty)

   
    return render(request, "myteacher.html", {'grouped_faculty': grouped_faculty})





def todo_vault(request):
    tasks = ToDoTask.objects.filter(user=request.user) 

    if request.method == 'POST':
        task = request.POST.get('task')
        if task:
            ToDoTask.objects.create(user=request.user, task=task) 
            return redirect('todovault') 

    return render(request, 'todovault.html', {
        'tasks': tasks, 
    })

def delete_task(request, task_id):
    task = ToDoTask.objects.get(id=task_id, user=request.user)  
    if task:
        task.delete() 
    return redirect('todovault')


def my_timetable(request):
    timetable = Timetable.objects.all()

    sorted_timetable = sorted(
        timetable,
        key=lambda entry: (Timetable.get_day_order(entry.day), entry.time)
    )
    return render(request, 'mytimetable.html', {'timetable': sorted_timetable})


def discussion_view(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        parent_id = request.POST.get('parent_id')

       
        if parent_id:
            parent_message = Discussion.objects.get(id=parent_id)
            Discussion.objects.create(user=request.user, content=message_content, parent=parent_message)
        else:
          
            Discussion.objects.create(user=request.user, content=message_content)

   
    discussions = Discussion.objects.filter(parent__isnull=True)
    return render(request, 'discussion.html', {'messages': discussions})

def delete_message(request, message_id):
   
    message = get_object_or_404(Discussion, id=message_id)

  
    if message.user == request.user:
        message.delete()  
        return redirect('discussion')  

   
    return redirect('discussion')  


def learning_resources(request):
    resources = Resource.objects.all()  
    return render(request, 'learningResources.html', {'resources': resources})


def view_marks(request):
    if request.user.is_authenticated and hasattr(request.user, 'student'):

        student = request.user.student
        marks = Marks.objects.filter(student=student).order_by('-date_awarded')  
        return render(request, 'view_marks.html', {'marks': marks})
    else:
        return redirect('login')  