from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ========== Home & General ==========
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('team/', views.team_view, name='team'),
    path('logout/', views.logout_view, name='logout'),

    # ========== Student ==========
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/resume/upload/', views.upload_resume, name='upload_resume'),
    path('student/drives/', views.available_drives, name='available_drives'),
    path('student/drives/registered/', views.registered_drives, name='registered_drives'),
    path('student/drives/register/<int:drive_id>/', views.register_for_drive, name='register_for_drive'),

    # ========== Staff ==========
    path('staff/login/', views.staff_login_view, name='staff_login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/drives/', views.view_drives, name='view_drives'),
    path('staff/drives/add/', views.add_drive, name='add_drive'),
    path('staff/drives/edit/<int:drive_id>/', views.edit_drive, name='edit_drive'),
    path('staff/drives/delete/<int:drive_id>/', views.delete_drive, name='delete_drive'),
    path('staff/verbal/upload/', views.upload_verbal_material, name='upload_verbal_material'),
    path('staff/verbal/delete/<int:material_id>/', views.delete_verbal_material, name='delete_verbal_material'),
    path('staff/aptitude/upload/', views.upload_aptitude_test, name='upload_aptitude_test'),
    path('delete_aptitude_test/<int:test_id>/', views.delete_aptitude_test, name='delete_aptitude_test'),
    path('staff/students/', views.view_students, name='view_students'),
    path('staff/technical/upload/', views.upload_technical_material, name='upload_technical_material'),
    path('staff/technical/delete/<int:material_id>/', views.delete_technical_material, name='delete_technical_material'),
    # ========== Admin ==========
    # ========== Admin ==========
    path('site-admin/login/', views.admin_login_view, name='admin_login'),
    path('site-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('site-admin/staff/add/', views.add_staff, name='add_staff'),
    path('site-admin/staff/edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('site-admin/staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('site-admin/staff/make_admin/<int:staff_id>/', views.make_staff_admin, name='make_staff_admin'),
    path('site-admin/messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),

    # ========== Department Coordinator ==========
    path('department/dashboard/', views.department_dashboard, name='department_dashboard'),
    path('department/student/add/', views.add_student, name='add_student'),
    path('department/student/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('department/student/delete/<int:student_id>/', views.delete_student, name='delete_student'),

    # ========== Verbal / Aptitude Viewing ==========
    path('verbal/materials/', views.view_verbal_material, name='view_verbal_material'),
    path('aptitude/tests/', views.view_aptitude_tests, name='view_aptitude_tests'),
    path('technical/materials/', views.view_technical_material, name='view_technical_material'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)