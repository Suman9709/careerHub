from django.urls import path
from .views import createjob, home, deleteJob, updateJob

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('createjob/', createjob, name='createjob'),
    path('delete/<int:id>/', deleteJob, name='deleteJob'),
    path('update/<int:id>/', updateJob, name='updateJob'),
]