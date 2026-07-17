from django.contrib import admin
from .models import Agent, Property, Lead, Deal
# Register your models here.

admin.site.register(Agent)
admin.site.register(Property)
admin.site.register(Lead)
admin.site.register(Deal)
