from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=255)
    companyName = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.IntegerField()
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    # __str__ method
    def __str__(self):
        return f"{self.companyName }-{self.title}"

