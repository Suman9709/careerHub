from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import redirect, render, get_object_or_404

from .forms import AgentForm, PropertyForm, LeadForm, DealForm
from .models import Agent, Property, Lead, Deal
from django.views.decorators.http import require_POST
# Create your views here.
def home(request):
    agent_count = Agent.objects.count()
    lead_count = Lead.objects.count()
    property_count = Property.objects.count()
    deal_count = Deal.objects.count()
    available_properties = Property.objects.filter(status__iexact="Available").count()
    sold_properties = Property.objects.filter(status__iexact="Sold").count()
    assigned_leads = Lead.objects.filter(assigned_agent__isnull=False).count()
    unassigned_leads = lead_count - assigned_leads
    converted_leads = Lead.objects.filter(
        Q(status__iexact="Done") | Q(status__iexact="Converted")
    ).count()
    done_deals = Deal.objects.filter(status__iexact="Done").count()
    pending_deals = Deal.objects.filter(status__iexact="Pending").count()
    cancelled_deals = Deal.objects.filter(status__iexact="Cancelled").count()
    total_deal_amount = Deal.objects.aggregate(total=Sum("amount"))["total"] or 0
    avg_commission = Deal.objects.aggregate(avg=Avg("commission_percentage"))["avg"] or 0
    conversion_rate = round((converted_leads / lead_count) * 100, 1) if lead_count else 0
    lead_assignment_rate = round((assigned_leads / lead_count) * 100, 1) if lead_count else 0
    property_availability_rate = round((available_properties / property_count) * 100, 1) if property_count else 0

    context = {
        "agent_count": agent_count,
        "lead_count": lead_count,
        "property_count": property_count,
        "deal_count": deal_count,
        "available_properties": available_properties,
        "sold_properties": sold_properties,
        "assigned_leads": assigned_leads,
        "unassigned_leads": unassigned_leads,
        "converted_leads": converted_leads,
        "done_deals": done_deals,
        "pending_deals": pending_deals,
        "cancelled_deals": cancelled_deals,
        "total_deal_amount": total_deal_amount,
        "avg_commission": avg_commission,
        "conversion_rate": conversion_rate,
        "lead_assignment_rate": lead_assignment_rate,
        "property_availability_rate": property_availability_rate,
        "recent_leads": Lead.objects.select_related("assigned_agent__user").order_by("-created_at")[:5],
        "recent_deals": Deal.objects.select_related("lead", "property").order_by("-created_at")[:5],
        "top_agents": Agent.objects.select_related("user").annotate(
            lead_total=Count("assigned_leads", distinct=True),
            property_total=Count("assigned_properties", distinct=True),
        ).order_by("-lead_total", "-property_total")[:5],
    }
    return render(request, 'index.html', context)

def agents(request):
    form = AgentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('agents')

    queryset = Agent.objects.select_related("user").all()
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(
            Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(region__icontains=query)
        )
    context = {'agents': queryset, "form":form}
    return render(request, 'pages/agents.html', context)

def edit_agent(request, agent_id):
    # get the agent object based on the id
    # check the request method and validate the form
    # save the form and redirect to the agents page
    agent = Agent.objects.get(id=agent_id)
    form = AgentForm(request.POST or None, request.FILES or None, instance=agent)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('agents')
    context = {'form':form, 'agent': agent}
    return render(request, 'pages/editagent.html', context)

@require_POST
def delete_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    agent.delete()
    return redirect('agents')

# Property views

def properties(request):
    form = PropertyForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('properties')

    queryset = Property.objects.select_related("assigned_agent__user").all()
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(address__icontains=query)
            | Q(city__icontains=query)
            | Q(property_type__icontains=query)
            | Q(status__icontains=query)
            | Q(assigned_agent__user__username__icontains=query)
        )
    context = {"propertys": queryset, "form": form}
    return render(request, 'pages/properties.html', context)

def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    form = PropertyForm(request.POST or None, request.FILES or None, instance = property)
    if request.method == 'POST' and form.is_valid():
        form.save() 
        return redirect('properties')
    context = {'form': form, 'property': property}
    return render(request, 'pages/editproperty.html', context)

@require_POST
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    property.delete()
    return redirect('properties')
   

def leads(request):
    form = LeadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('leads')

    queryset = Lead.objects.select_related("assigned_agent__user", "interested_property_types").all()
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(
            Q(fullname__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(source__icontains=query)
            | Q(status__icontains=query)
            | Q(assigned_agent__user__username__icontains=query)
            | Q(interested_property_types__title__icontains=query)
        )
    context = {
        "leads": queryset,
        "form": form,
        "lead_status": Lead.LeadStatus.choices,
    }
    return render(request, 'pages/leads.html', context)

def edit_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    form = LeadForm(request.POST or None, request.FILES or None, instance=lead)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('leads')
    context = {'form': form, 'lead': lead}
    return render(request, 'pages/editlead.html', context)

def update_lead_status(request, lead_id):
    status = request.POST.get('status')
    lead = get_object_or_404(Lead, id=lead_id)
    valid_statuses = [value for value, label in Lead.LeadStatus.choices]
    if status in valid_statuses:
        lead.status = status
        lead.save()
    return redirect('leads')

@require_POST
def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    return redirect('leads')



def deals(request):
    form = DealForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('deals')

    queryset = Deal.objects.select_related("lead", "property", "lead__assigned_agent__user").all()
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(
            Q(status__icontains=query)
            | Q(lead__fullname__icontains=query)
            | Q(lead__phone_number__icontains=query)
            | Q(property__title__icontains=query)
            | Q(property__city__icontains=query)
            | Q(lead__assigned_agent__user__username__icontains=query)
        )

    context = {"deals": queryset, "form": form}
    return render(request, 'pages/deals.html', context)


def edit_deal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    form = DealForm(request.POST or None, request.FILES or None, instance=deal)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('deals')
    context = {'form': form, 'deal': deal}
    return render(request, 'pages/editdeal.html', context)


@require_POST
def delete_deal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    deal.delete()
    return redirect('deals')
