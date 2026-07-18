
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.humanize.templatetags.humanize import intword

# Create your models here.
class Agent(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE) # prefer to use get_user_model() instead of User model directly
    profile_picture = models.ImageField(upload_to='profile', default='profile/default.jpg')
    phone_number = models.CharField(max_length=10)
    region = models.CharField(max_length=50)
    commission_share = models.DecimalField(max_digits=4, decimal_places=2)
    monthly_target = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username



class Property(models.Model):
    class PropertyType(models.TextChoices):
        APARTMENT = "apartment", "Apartment"
        PLOT = "plot", "Plot"
        VILLA = "villa", "Villa"
        LAND = "land", "Land"
        COMMERCIAL = "commercial", "Commercial"

    class PropertyStatus(models.TextChoices):
        AVAILABLE = 'Available','available'
        SOLD = 'Sold','sold'


    title= models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    property_type = models.CharField(max_length = 255, choices=PropertyType.choices)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to = 'properties')
    status = models.CharField(max_length = 255, choices=PropertyStatus.choices, default=PropertyStatus.AVAILABLE)
    assigned_agent = models.ForeignKey(to=Agent, on_delete=models.SET_NULL, related_name='assigned_properties', null=True, blank=True)
    listing_at = models.DateTimeField(auto_now_add=True)
    sqft = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    

class Lead(models.Model):
    class LeadStatus(models.TextChoices):
        NEW = 'new','New'
        CONTACTED = 'contacted','Contacted'
        SITE_VISITED = 'Site Visited','Site Visited'
        NEGOTIATION = 'Negotiation','Negotiation'
        LOST = 'Lost','Lost'
        DONE = 'Done','Done'
    class SourceType(models.TextChoices):
        WEBSITE = 'Website','Website'
        WALKIN = 'Walkin','Walkin'
        SOCIAL_MEDIA = 'Social Media','Social Media'
        AGENT = 'Agent','Agent'

    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    source = models.CharField(max_length=255, choices = SourceType.choices) #webiste or walkin or social media post or agents
    interested_property_types = models.ForeignKey(to=Property, on_delete=models.SET_NULL, related_name='interested_leads', null=True, blank=True)
    min_budget = models.DecimalField(max_digits=12, decimal_places=2)
    max_budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=255, choices=LeadStatus.choices) #new, contacted, interested, not interested, closed
    assigned_agent = models.ForeignKey(to=Agent, on_delete=models.SET_NULL, related_name='assigned_leads', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"lead: {self.fullname}"
    
    def get_budget_range(self):
        start = intword(self.min_budget).split(" ")[0]
        end = intword(self.max_budget).split(" ")[0]
        unit = intword(self.max_budget).split(" ")[-1]
      
        return f"{start} - {end} {unit}"


class Deal(models.Model):
    class DealStatus(models.TextChoices):
        PENDING = 'Pending','Pending'
        CANCELLED = 'Cancelled','Cancelled'
        DONE = 'Done','Done'

    lead = models.ForeignKey(to=Lead, on_delete=models.CASCADE, related_name='deals')
    property = models.ForeignKey(to = Property, on_delete=models.CASCADE, related_name='deals')
    status = models.CharField(max_length=255, choices=DealStatus.choices, default=DealStatus.PENDING) #pending, cancelled, done, 
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expected_closing_date = models.DateField()
    actual_closing_date = models.DateField(null=True, blank=True)
    commission_percentage = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) 

 
    def __str__(self):
        return f"deal: {self.lead.fullname} - {self.property.title}"
    



