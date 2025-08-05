from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('student_login/', views.student_login, name='student_login'),
    path('team/', views.team_view, name='team'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('view_staff/', views.view_staff, name='view_staff'),
    path('edit_staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('logout/', views.logout_view, name='logout'),
    path('view_students/', views.view_students, name='view_students'),
    path('add_drive/', views.add_drive, name='add_drive'),
    path('view_drives/', views.view_drives, name='view_drives'),
    path('edit_drive/<int:drive_id>/', views.edit_drive, name='edit_drive'),
    path('delete_drive/<int:drive_id>/', views.delete_drive, name='delete_drive'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_contact_message'),


]
