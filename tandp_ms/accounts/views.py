from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as flash_messages
from django.utils import timezone

from .models import (
    ContactMessage, Student, PlacementDrive,
    Registration, StaffProfile
)

def is_admin(user):
    return user.is_superuser

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url='admin_login')
@user_passes_test(is_staff_user)
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_drives = PlacementDrive.objects.count()
    upcoming_drives = PlacementDrive.objects.filter(date__gte=timezone.now()).count()
    total_messages = ContactMessage.objects.count()

    staff_profile = StaffProfile.objects.filter(user=request.user).first()
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    staff_profiles = StaffProfile.objects.all().order_by('designation')

    context = {
        'staff_profile': staff_profile,
        'contact_messages': contact_messages,
        'staff_profiles': staff_profiles,
        'total_students': total_students,
        'total_drives': total_drives,
        'upcoming_drives': upcoming_drives,
        'total_messages': total_messages
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def view_staff(request):
    query = request.GET.get('q')
    if query:
        staff_list = StaffProfile.objects.filter(name__icontains=query) | StaffProfile.objects.filter(designation__icontains=query)
    else:
        staff_list = StaffProfile.objects.all()
    return render(request, 'accounts/view_staff.html', {'staff_list': staff_list})

def home(request):
    return render(request, 'accounts/home.html')

def about(request):
    return render(request, 'accounts/about.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def student_login(request):
    return render(request, 'accounts/student_login.html')

def available_drives(request):
    student_email = request.session.get('student_email')
    if not student_email:
        return redirect('student_login')

    student = get_object_or_404(Student, email=student_email)
    registered_drive_ids = Registration.objects.filter(student=student).values_list('drive_id', flat=True)
    drives = PlacementDrive.objects.exclude(id__in=registered_drive_ids).order_by('date')

    return render(request, 'accounts/available_drives.html', {'student': student, 'drives': drives})

def register_for_drive(request, drive_id):
    student_email = request.session.get('student_email')
    if not student_email:
        return redirect('student_login')

    student = get_object_or_404(Student, email=student_email)
    drive = get_object_or_404(PlacementDrive, id=drive_id)

    if not Registration.objects.filter(student=student, drive=drive).exists():
        Registration.objects.create(student=student, drive=drive)
        flash_messages.success(request, f"Successfully registered for {drive.company_name}")
    else:
        flash_messages.warning(request, "You have already registered for this drive.")

    return redirect('available_drives')

def add_drive(request):
    if request.method == 'POST':
        PlacementDrive.objects.create(
            company_name=request.POST['company_name'],
            job_role=request.POST['job_role'],
            date=request.POST['date'],
            package=request.POST['package'],
            description=request.POST['description']
        )
        flash_messages.success(request, "Placement drive added successfully.")
        return redirect('view_drives')
    return render(request, 'accounts/add_drive.html')

def view_drives(request):
    drives = PlacementDrive.objects.all().order_by('-date')
    return render(request, 'accounts/view_drives.html', {'drives': drives})

def edit_drive(request, drive_id):
    drive = get_object_or_404(PlacementDrive, id=drive_id)
    if request.method == 'POST':
        drive.company_name = request.POST['company_name']
        drive.job_role = request.POST['job_role']
        drive.date = request.POST['date']
        drive.package = request.POST['package']
        drive.description = request.POST['description']
        drive.save()
        flash_messages.success(request, "Placement drive updated.")
        return redirect('view_drives')
    return render(request, 'accounts/edit_drive.html', {'drive': drive})

def delete_drive(request, drive_id):
    drive = get_object_or_404(PlacementDrive, id=drive_id)
    drive.delete()
    flash_messages.success(request, "Drive deleted successfully.")
    return redirect('view_drives')

def admin_login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'accounts/admin_login.html', {'error': 'Invalid credentials or not an admin.'})
    return render(request, 'accounts/admin_login.html')

@login_required
@user_passes_test(is_staff_user)
def delete_message(request, message_id):
    try:
        msg = ContactMessage.objects.get(id=message_id)
        msg.delete()
        flash_messages.success(request, "Message deleted successfully.")
    except ContactMessage.DoesNotExist:
        flash_messages.error(request, "Message not found.")
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_staff_user)
def view_students(request):
    students = Student.objects.all().order_by('roll_number')
    return render(request, 'accounts/view_students.html', {'students': students})

@login_required
@user_passes_test(is_staff_user)
def edit_staff(request, staff_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    if request.method == 'POST':
        staff.name = request.POST['name']
        staff.designation = request.POST['role']
        staff.phone = request.POST['mobile']
        staff.email = request.POST['email']
        staff.save()
        flash_messages.success(request, "Staff profile updated.")
        return redirect('admin_dashboard')
    return render(request, 'accounts/edit_staff.html', {'staff': staff})

@login_required
@user_passes_test(is_staff_user)
def delete_staff(request, staff_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    staff.delete()
    flash_messages.success(request, "Staff profile deleted.")
    return redirect('admin_dashboard')

def team_view(request):
    team_members = [
        {"sno": 1, "name": "Mr. C. Y. Balu", "designation": "Head – Corporate Relations", "mobile": "9900944775", "email": "balucy@srit.ac.in"},
        {"sno": 2, "name": "Dr. S Bhargava Reddy", "designation": "Training & Placement Officer", "mobile": "9515811111", "email": "tpo@srit.ac.in"},
        {"sno": 3, "name": "Dr. D Anil Kumar", "designation": "Alumni Relations Officer & Verbal Trainer", "mobile": "9791265918", "email": "alumni@srit.ac.in"},
        {"sno": 4, "name": "Dr. G. Hemanth Kumar Yadav", "designation": "Industry Relations Officer & Technical Trainer", "mobile": "9848169943", "email": "iiicell@srit.ac.in"},
        {"sno": 5, "name": "Mr. S Moin Ahmed", "designation": "Associate TPO & Coordinator – MEC", "mobile": "8328220829", "email": "atpo@srit.ac.in"},
        {"sno": 6, "name": "Mrs. T A Swathi", "designation": "Coordinator – Civil", "mobile": "8074669931", "email": "swathi.civ@srit.ac.in"},
        {"sno": 7, "name": "Mr. Y. Sathish Kumar", "designation": "Coordinator – EEE", "mobile": "8309918031", "email": "sathishkumar.eee@srit.ac.in"},
        {"sno": 8, "name": "Mr. D. Sreekanth Reddy", "designation": "Coordinator – ECE", "mobile": "9963917078", "email": "sreekanthreddy.ece@srit.ac.in"},
        {"sno": 9, "name": "Mr. K Kondanna", "designation": "Coordinator – CSD & Technical Trainer (Global Certifications)", "mobile": "9985502062", "email": "kondanna.cse@srit.ac.in"},
        {"sno": 10, "name": "Dr. D. Rajesh Babu", "designation": "Coordinator – CSE & CSM", "mobile": "9966982288", "email": "rajeshbabud.cse@srit.ac.in"},
        {"sno": 11, "name": "Mr. M Prabhakar", "designation": "Aptitude & Reasoning Trainer", "mobile": "9441553074", "email": "prabhakar.hs@srit.ac.in"},
        {"sno": 12, "name": "Mr. V Naveen Kumar", "designation": "Clerk – AIRP", "mobile": "9398023404", "email": "clerk.tpcell@srit.ac.in"},
    ]
    return render(request, 'accounts/team.html', {'team_members': team_members})

def contact_view(request):
    message_sent = False
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )
        message_sent = True
    return render(request, 'accounts/contact.html', {'message_sent': message_sent})
