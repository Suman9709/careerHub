from django import forms
from .models import Agent, Property, Lead, Deal

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = "__all__"

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = "__all__"


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = "__all__"

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = "__all__"