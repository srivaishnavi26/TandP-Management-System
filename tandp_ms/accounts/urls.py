from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('student_login/', views.student_login, name='student_login'),
    path('team/', views.team_view, name='team'),
]
