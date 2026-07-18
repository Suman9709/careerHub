from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name = 'home' ),

    # agent urls
    path("agents/", views.agents, name = 'agents' ),
    path("agents/edit/<int:agent_id>/", views.edit_agent, name='edit_agent'),
    path("agents/delete/<int:agent_id>/", views.delete_agent, name='delete_agent'),

    # property urls
    path("properties/", views.properties, name = 'properties' ),
    path("properties/edit/<int:property_id>/", views.edit_property, name='edit_property'),
    path("properties/delete/<int:property_id>/", views.delete_property, name='delete_property'),

    # lead urls
    path("lead/", views.leads, name = 'leads' ),
    path("lead/edit/<int:lead_id>/", views.edit_lead, name='edit_lead'),
    path("lead/delete/<int:lead_id>/", views.delete_lead, name='delete_lead'),
    path("lead/status/<int:lead_id>/", views.update_lead_status, name='update_lead_status'),

    # deal urls
    path("deals/", views.deals, name ='deals'),
    path("deals/edit/<int:deal_id>/", views.edit_deal, name='edit_deal'),
    path("deals/delete/<int:deal_id>/", views.delete_deal, name='delete_deal'),
]



