
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Job
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # commit=False gives us a chance to update the user object before it goes to the database.
            # Pro: useful when you want to add extra fields, set flags, or inspect the user before saving.
            user = form.save(commit=False)
            user.save()

            # Pro: redirecting to login keeps registration and login as two clear separate steps.
            # If you want instant login after registration later, add login(request, user) here.
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout_user(request):
    # Redirect home after logout so users land back on the public job list.
    # This also handles direct visits to /logout/ by sending them back to /.
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('/')


def home(request):
    query = request.GET.get('query', '')  # Get the search query from the GET parameters
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(companyName__icontains=query) |
            Q(location__icontains=query) 
        )
    return render(request, 'index.html', {'jobs': jobs, 'query': query})


@login_required
def createjob(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        companyName = request.POST.get('companyName')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        logo = request.FILES.get('logo')  # Get the uploaded logo file

        job = Job(
            title=title, 
            companyName=companyName, 
            location=location, 
            salary=salary,
            logo=logo
            )
        job.save()

        messages.success(request, 'Job created successfully!')
        return redirect('home')

    else:
        return render(request, 'addform.html')
    
@login_required
def deleteJob(request, id):
    job = Job.objects.get(id=id)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('home')
    else:
        return redirect('home')

@login_required
def updateJob(request, id):
    job = Job.objects.get(id=id)
    
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.companyName = request.POST.get('companyName')
        job.location = request.POST.get('location')
        job.salary = request.POST.get('salary')
        logo = request.FILES.get('logo')  # Get the uploaded logo file
        if logo:
            job.logo = logo  # Update the logo only if a new file is uploaded
        job.save()

        messages.success(request, 'Job updated successfully!')
        return redirect('home')

    else:
        return render(request, 'updateform.html', {'job': job})

  
