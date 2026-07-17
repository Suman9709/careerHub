from django.shortcuts import render

from .forms import AgentForm, PropertyForm, LeadForm, DealForm
from .models import Agent, Property, Lead, Deal
# Create your views here.
def home(request):
    return render(request, 'index.html')

def agents(request):
    form = AgentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    queryset = Agent.objects.all()
    context = {'agents': queryset, "form":form}
    for agent in queryset:
        print(agent.user.first_name)
    return render(request, 'pages/agents.html', context)
    


def properties(request):
    form = PropertyForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    queryset = Property.objects.all()
    context = {"propertys": queryset, "form": form}
    return render(request, 'pages/properties.html', context)

def leads(request):
    form = LeadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    queryset = Lead.objects.all()
    context = {"leads": queryset, "form": form}
    return render(request, 'pages/leads.html', context)

def deals(request):
    form = DealForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    queryset = Deal.objects.all()

    context = {"deals": queryset, "form": form}
    return render(request, 'pages/deals.html', context)