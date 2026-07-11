from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Job

# Create your views here.

def home(request):
    jobs = Job.objects.all()
    return render(request, 'index.html', {'jobs': jobs})


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
    

def deleteJob(request, id):
    job = Job.objects.get(id=id)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('home')
    else:
        return redirect('home')

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

  