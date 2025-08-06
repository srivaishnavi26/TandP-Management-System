from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as flash_messages
from django.utils import timezone
from django.contrib.auth.models import User
from .models import (
    ContactMessage,
    Student,
    PlacementDrive,
    Registration,
    StaffProfile,
    VerbalMaterial,
    AptitudeTest
)

# ========== Access Control ==========

def is_admin(user):
    return user.is_superuser

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

def is_strict_admin(user):
    return user.is_authenticated and user.is_superuser

def is_strict_staff(user):
    return user.is_authenticated and user.is_staff and not user.is_superuser

# ========== Student Login & Dashboard ==========

def student_login(request):
    if request.method == 'POST':
        roll_number = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=roll_number, password=password)

        if user and not user.is_staff and not user.is_superuser:
            login(request, user)
            return redirect('student_dashboard')
        else:
            flash_messages.error(request, "Invalid roll number or password.")

    return render(request, 'accounts/student_login.html')

@login_required
def student_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('home')

    student = get_object_or_404(Student, user=request.user)
    return render(request, 'accounts/student_dashboard.html', {'student': student})

# ========== Staff/Admin Login ==========

def staff_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.is_authenticated and user.is_staff:
            login(request, user)

            staff_profile = StaffProfile.objects.filter(user=user).first()
            if not staff_profile:
                logout(request)
                return render(request, 'accounts/staff_login.html', {
                    'error': 'Your staff profile is not set up. Please contact admin.'
                })

            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('staff_dashboard')
        else:
            return render(request, 'accounts/staff_login.html', {
                'error': 'Invalid credentials or not a staff member.'
            })

    return render(request, 'accounts/staff_login.html')

# ========== Dashboards ==========

@login_required
@user_passes_test(is_strict_admin)
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
@user_passes_test(is_strict_staff)
def staff_dashboard(request):
    staff_profile = StaffProfile.objects.filter(user=request.user).first()

    if not staff_profile:
        flash_messages.error(request, "No staff profile found for your account.")
        return redirect('home')

    upcoming_drives = PlacementDrive.objects.filter(date__gte=timezone.now()).count()
    total_drives = PlacementDrive.objects.count()

    context = {
        'staff_profile': staff_profile,
        'role': staff_profile.role,
        'upcoming_drives': upcoming_drives,
        'total_drives': total_drives,
    }

    if staff_profile.role == 'verbal_trainer':
        verbal_materials = VerbalMaterial.objects.filter(uploaded_by=staff_profile).order_by('-uploaded_at')
        context['verbal_materials'] = verbal_materials
    if staff_profile.role == 'aptitude_trainer':
        aptitude_tests = AptitudeTest.objects.filter(uploaded_by=staff_profile).order_by('-uploaded_at')
        context['aptitude_tests'] = aptitude_tests

    return render(request, 'accounts/staff_dashboard.html', context)

# ========== Placement Drive ==========

@login_required
@user_passes_test(is_staff_user)
def view_drives(request):
    drives = PlacementDrive.objects.all().order_by('-date')
    return render(request, 'accounts/view_drives.html', {'drives': drives})

@login_required
@user_passes_test(is_staff_user)
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

@login_required
@user_passes_test(is_staff_user)
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

@login_required
@user_passes_test(is_strict_admin)
def delete_drive(request, drive_id):
    drive = get_object_or_404(PlacementDrive, id=drive_id)
    drive.delete()
    flash_messages.success(request, "Drive deleted successfully.")
    return redirect('view_drives')

# ========== Registration for Drives ==========

@login_required
def available_drives(request):
    student = get_object_or_404(Student, user=request.user)
    registered_drive_ids = Registration.objects.filter(student=student).values_list('drive_id', flat=True)
    drives = PlacementDrive.objects.exclude(id__in=registered_drive_ids).order_by('date')

    return render(request, 'accounts/available_drives.html', {'student': student, 'drives': drives})

@login_required
def register_for_drive(request, drive_id):
    student = get_object_or_404(Student, user=request.user)
    drive = get_object_or_404(PlacementDrive, id=drive_id)

    if not Registration.objects.filter(student=student, drive=drive).exists():
        Registration.objects.create(student=student, drive=drive)
        flash_messages.success(request, f"Successfully registered for {drive.company_name}")
    else:
        flash_messages.warning(request, "You have already registered for this drive.")

    return redirect('available_drives')

# ========== Verbal Material ==========

@login_required
@user_passes_test(lambda u: u.is_authenticated and StaffProfile.objects.filter(user=u, role='verbal_trainer').exists())
def upload_verbal_material(request):
    staff_profile = StaffProfile.objects.get(user=request.user)

    if request.method == 'POST' and request.FILES.get('file'):
        VerbalMaterial.objects.create(
            title=request.POST.get('title'),
            file=request.FILES['file'],
            uploaded_by=staff_profile
        )
        flash_messages.success(request, "Material uploaded successfully.")
        return redirect('upload_verbal_material')

    materials = VerbalMaterial.objects.filter(uploaded_by=staff_profile).order_by('-uploaded_at')
    return render(request, 'accounts/upload_verbal.html', {'materials': materials})

@login_required
def delete_verbal_material(request, material_id):
    if request.method == 'POST':
        material = get_object_or_404(VerbalMaterial, id=material_id)
        material.file.delete()
        material.delete()
        flash_messages.success(request, "Material deleted successfully.")
    return redirect('staff_dashboard')

# ========== Staff Management ==========
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # make sure this name exists in urls.py
        else:
            return render(request, 'accounts/admin_login.html', {
                'error': 'Invalid admin credentials.'
            })

    return render(request, 'accounts/admin_login.html')

@login_required
@user_passes_test(is_strict_admin)
def add_staff(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.create_user(username=username, password=password, email=email, is_staff=True)

        StaffProfile.objects.create(
            user=user,
            name=request.POST.get('name'),
            designation=request.POST.get('designation'),
            mobile=request.POST.get('mobile'),
            email=email,
            role=request.POST.get('role')
        )
        flash_messages.success(request, "New staff profile created.")
        return redirect('admin_dashboard')

    return render(request, 'accounts/add_staff.html')

@login_required
@user_passes_test(is_strict_admin)
def edit_staff(request, staff_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    if request.method == 'POST':
        staff.name = request.POST.get('name')
        staff.designation = request.POST.get('designation')
        staff.mobile = request.POST.get('mobile')
        staff.email = request.POST.get('email')
        staff.role = request.POST.get('role')
        staff.save()
        flash_messages.success(request, "Staff profile updated.")
        return redirect('admin_dashboard')
    return render(request, 'accounts/edit_staff.html', {'staff': staff})

@login_required
@user_passes_test(is_strict_admin)
def delete_staff(request, staff_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    staff.delete()
    flash_messages.success(request, "Staff profile deleted.")
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_strict_admin)
def make_staff_admin(request, staff_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    staff.user.is_staff = True
    staff.user.is_superuser = True
    staff.user.save()
    flash_messages.success(request, f"{staff.name} is now an admin.")
    return redirect('admin_dashboard')

# ========== Others ==========

def home(request):
    return render(request, 'accounts/home.html')

def about(request):
    return render(request, 'accounts/about.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
@user_passes_test(is_staff_user)
def view_students(request):
    students = Student.objects.all().order_by('roll_number')
    return render(request, 'accounts/view_students.html', {'students': students})

@login_required
@user_passes_test(is_strict_admin)
def delete_message(request, message_id):
    try:
        msg = ContactMessage.objects.get(id=message_id)
        msg.delete()
        flash_messages.success(request, "Message deleted successfully.")
    except ContactMessage.DoesNotExist:
        flash_messages.error(request, "Message not found.")
    return redirect('admin_dashboard')

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
@login_required
def registered_drives(request):
    student = get_object_or_404(Student, user=request.user)
    registrations = Registration.objects.filter(student=student).select_related('drive').order_by('drive__date')

    return render(request, 'accounts/registered_drives.html', {
        'student': student,
        'registrations': registrations
    })
@login_required
def upload_resume(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST' and request.FILES.get('resume'):
        student.resume = request.FILES['resume']
        student.save()
        flash_messages.success(request, "Resume uploaded successfully.")

    return render(request, 'accounts/upload_resume.html', {'student': student})
from .models import VerbalMaterial

@login_required
def view_verbal_material(request):
    materials = VerbalMaterial.objects.all()
    return render(request, 'accounts/view_verbal_material.html', {'materials': materials})
@login_required
@user_passes_test(is_staff_user)
def upload_aptitude_test(request):
    if request.method == 'POST':
        title = request.POST['title']
        file = request.FILES['file']
        staff = request.user.staffprofile
        AptitudeTest.objects.create(title=title, file=file, uploaded_by=staff)
        flash_messages.success(request, "Aptitude test uploaded successfully.")
        return redirect('upload_aptitude_test')

    tests = AptitudeTest.objects.filter(uploaded_by=request.user.staffprofile)
    return render(request, 'accounts/upload_aptitude.html', {'tests': tests})
@login_required
def view_aptitude_tests(request):
    tests = AptitudeTest.objects.all().order_by('-uploaded_at')
    return render(request, 'accounts/view_aptitude_tests.html', {'tests': tests})
