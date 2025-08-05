from django.urls import path
from . import views

urlpatterns = [

    # Public Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('team/', views.team_view, name='team'),

    # Authentication
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('staff_login/', views.staff_login_view, name='staff_login'),
    path('student_login/', views.student_login, name='student_login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # Staff Management (Admin Only)
    path('add-staff/', views.add_staff, name='add_staff'),
    path('staff/edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('staff/make_admin/<int:staff_id>/', views.make_staff_admin, name='make_staff_admin'),
    path('upload_verbal/', views.upload_verbal_material, name='upload_verbal_material'),

    # Student Management (Staff/Admin)
    path('view_students/', views.view_students, name='view_students'),

    # Drive Management (Staff/Admin)
    path('add_drive/', views.add_drive, name='add_drive'),
    path('view_drives/', views.view_drives, name='view_drives'),
    path('edit_drive/<int:drive_id>/', views.edit_drive, name='edit_drive'),
    path('delete_drive/<int:drive_id>/', views.delete_drive, name='delete_drive'),

    # Contact Message Management (Admin)
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_contact_message'),
]
