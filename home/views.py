from django.shortcuts import render,redirect
from django.http import HttpResponse #manually added
from django.contrib.auth import authenticate,login,logout
from home.models import Feedback,User,Task #manually added to import database
from datetime import datetime #manually added

# Create your views here.

def register(request):
    if request.method=="POST":
        firstname = str(request.POST.get('first-name'))
        lastname = str(request.POST.get('last-name'))
        username = request.POST.get('username')
        email = request.POST.get('email')
        occupation = request.POST.get('occupation')
        password = request.POST.get('password')

        user = User.objects.create_user(first_name=firstname , email=email , 
        user_name=username ,password=password)
        user.last_name = lastname
        user.occupation = occupation
        user.save()
        
        return render(request,'login.html')

    return render(request,'register.html')

def login_view(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,user_name=username ,password=password)
        
        if user is not None:  
            login(request,user)
            # Redirect to a success page.
            return redirect("/")
        else:       
            return render(request,"login.html" )

    return render(request,"login.html" ) # Return an 'invalid login' error message.

def logout_view(request):
    logout(request)
    return redirect("/login")

def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).order_by('status','due_date','-priority').values()
        context = {
            'title':'Home Page',
            'tasks' : tasks,
            'name' : str(request.user.first_name).upper()
        }
        return render(request,"index.html",context)

    return redirect("/login")

def add_task(request):
    if request.method=="POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due-date")
        desc = request.POST.get("desc")
        priority = request.POST.get("priority")

        task = Task()
        task.user = request.user
        task.title = title
        task.due_date = due_date
        task.priority = priority
        task.desc = desc

        task.save()
        return redirect("/")

def delete_task(request,id):
    task = Task.objects.get(id=id)
    if(task.user==request.user):
        task.delete()
    
    return redirect("/")

def done_task(request,id):
    task = Task.objects.get(id=id)
    if(task.user==request.user):
        task.status = True
        task.save()
    
    return redirect("/")

def reset_task(request,id):
    task = Task.objects.get(id=id)
    if(task.user==request.user):
        task.status = False
        task.save()

    return redirect("/")

def edit_task(request,id):
    if request.method=="POST":
        task = Task.objects.get(id=id)
        if(task.user==request.user):
            task.due_date = request.POST.get("due-date")
            task.desc = request.POST.get("desc")
            task.title = request.POST.get("title")
            task.priority = request.POST.get("priority")
            task.save()
    return redirect("/")

def profile(request):
    user = request.user
    if user.is_authenticated:
        user_tasks = Task.objects.filter(user=user)
        today = datetime.utcnow()
        total_tasks = user_tasks.count()
        tasks_completed = user_tasks.filter(status=True).count()
        tasks_pending = user_tasks.filter(status=False,due_date__gte=today).count()
        tasks_overdue = user_tasks.filter(status=False,due_date__lt=today).count()
        profile = {
            'name' : str(user.first_name).upper() + " " + str(user.last_name).upper(),
            'total_tasks':total_tasks,
            'tasks_completed':tasks_completed,
            'tasks_pending':tasks_pending,
            'tasks_overdue':tasks_overdue
        }

        context = {
            'title':'Profile Page',
            'profile':profile,
            'user' : user
        }
        return render(request,"profile.html",context)

    return redirect("/login")

def contact(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            firstname = str(request.POST.get('first-name'))
            lastname = str(request.POST.get('last-name'))
            
            name=firstname+" "+lastname
            email = request.POST.get('email')
            text = request.POST.get('feedback-text')
            date = datetime.today()

            feedback = Feedback(name=name , email=email , text=text , date=date)
            feedback.save()

        context={
            'title':'About Page'
        }
        return render(request,"about.html",context)
    
    return redirect("/login")

def about(request):
    if request.user.is_authenticated:
        context = {
            'title':'About Page',
        }
        return render(request,"about.html",context)

    return redirect("/register")

