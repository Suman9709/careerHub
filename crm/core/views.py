from django.shortcuts import render
from .models import Agent, Property, Lead
# Create your views here.
def home(request):
    return render(request, 'index.html')

def agents(request):
    queryset = Agent.objects.all()

    context = {'agents': queryset}
    for agent in queryset:
        print(agent.user.first_name)
    return render(request, 'pages/agents.html', context)
    


def properties(request):
    queryset = Property.objects.all()

    context = {"propertys": queryset}
    return render(request, 'pages/properties.html', context)

def leads(request):
    return render(request, 'pages/leads.html')

def deals(request):
    return render(request, 'pages/deals.html')