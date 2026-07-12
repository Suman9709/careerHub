from django.urls import path
from .views import createjob, home, deleteJob, updateJob, register, logout_user

urlpatterns = [
    path('', home, name='home'),
    path('home/', home),
    path('createjob/', createjob, name='createjob'),
    path('delete/<int:id>/', deleteJob, name='deleteJob'),
    path('update/<int:id>/', updateJob, name='updateJob'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout_user'),
]
