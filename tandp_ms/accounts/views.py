from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from .forms import StudentForm
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

# =======================
# ===== Decorators ======
# =======================

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_superuser)(view_func)

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff)(view_func)

def strict_staff_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff and not u.is_superuser)(view_func)

def department_coordinator_required(view_func):
    return user_passes_test(lambda u: StaffProfile.objects.filter(user=u, role='department_coordinator').exists())(view_func)


# =======================
# ===== Login Views =====
# =======================

def student_login(request):
    if request.method == 'POST':
        roll_number = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=roll_number, password=password)
        if user and not user.is_staff and not user.is_superuser:
            login(request, user)
            return redirect('student_dashboard')
        messages.error(request, "Invalid roll number or password.")
    return render(request, 'accounts/student_login.html')


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
                messages.error(request, 'Your staff profile is not set up. Contact admin.')
                return render(request, 'accounts/staff_login.html')
            return redirect('admin_dashboard') if user.is_superuser else redirect('staff_dashboard')
        messages.error(request, 'Invalid credentials or not a staff member.')
    return render(request, 'accounts/staff_login.html')


def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid admin credentials.')
    return render(request, 'accounts/admin_login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# =======================
# ===== Dashboards ======
# =======================

@login_required
def student_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('home')
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'accounts/student_dashboard.html', {'student': student})


@login_required
@admin_required
def admin_dashboard(request):
    staff_profile = StaffProfile.objects.filter(user=request.user).first()
    context = {
        'staff_profile': staff_profile,
        'total_students': Student.objects.count(),
        'total_drives': PlacementDrive.objects.count(),
        'upcoming_drives': PlacementDrive.objects.filter(date__gte=timezone.now()).count(),
        'total_messages': ContactMessage.objects.count(),
        'contact_messages': ContactMessage.objects.all().order_by('-created_at'),
        'staff_profiles': StaffProfile.objects.all().order_by('designation'),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
@strict_staff_required
def staff_dashboard(request):
    staff_profile = get_object_or_404(StaffProfile, user=request.user)
    context = {
        'staff_profile': staff_profile,
        'role': staff_profile.role,
        'upcoming_drives': PlacementDrive.objects.filter(date__gte=timezone.now()).count(),
        'total_drives': PlacementDrive.objects.count(),
    }
    if staff_profile.role == 'verbal_trainer':
        context['verbal_materials'] = VerbalMaterial.objects.filter(uploaded_by=staff_profile).order_by('-uploaded_at')
    if staff_profile.role == 'aptitude_trainer':
        context['aptitude_tests'] = AptitudeTest.objects.filter(uploaded_by=staff_profile).order_by('-uploaded_at')
    return render(request, 'accounts/staff_dashboard.html', context)


@login_required
@department_coordinator_required
def department_dashboard(request):
    staff_profile = get_object_or_404(StaffProfile, user=request.user)
    students = Student.objects.filter(department=staff_profile.branch).order_by('roll_number')
    return render(request, 'accounts/department_dashboard.html', {'staff_profile': staff_profile, 'students': students})


# =======================
# ===== Placement Drives
# =======================

@login_required
@staff_required
def view_drives(request):
    drives = PlacementDrive.objects.all().order_by('-date')
    return render(request, 'accounts/view_drives.html', {'drives': drives})


@login_required
@staff_required
def add_drive(request):
    if request.method == 'POST':
        PlacementDrive.objects.create(
            company_name=request.POST['company_name'],
            job_role=request.POST['job_role'],
            date=request.POST['date'],
            package=request.POST['package'],
            description=request.POST['description']
        )
        messages.success(request, "Placement drive added successfully.")
        return redirect('view_drives')
    return render(request, 'accounts/add_drive.html')


@login_required
@staff_required
def edit_drive(request, drive_id):
    drive = get_object_or_404(PlacementDrive, id=drive_id)
    if request.method == 'POST':
        drive.company_name = request.POST['company_name']
        drive.job_role = request.POST['job_role']
        drive.date = request.POST['date']
        drive.package = request.POST['package']
        drive.description = request.POST['description']
        drive.save()
        messages.success(request, "Placement drive updated successfully.")
        return redirect('view_drives')
    return render(request, 'accounts/edit_drive.html', {'drive': drive})


@login_required
@admin_required
def delete_drive(request, drive_id):
    drive = get_object_or_404(PlacementDrive, id=drive_id)
    drive.delete()
    messages.success(request, "Drive deleted successfully.")
    return redirect('view_drives')


# =======================
# ===== Registrations ===
# =======================

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
        messages.success(request, f"Successfully registered for {drive.company_name}")
    else:
        messages.warning(request, "You have already registered for this drive.")
    return redirect('available_drives')


@login_required
def registered_drives(request):
    student = get_object_or_404(Student, user=request.user)
    registrations = Registration.objects.filter(student=student).select_related('drive').order_by('drive__date')
    return render(request, 'accounts/registered_drives.html', {'student': student, 'registrations': registrations})


# =======================
# ===== Verbal Material ==
# =======================

@login_required
@staff_required
def upload_verbal_material(request):
    staff_profile = get_object_or_404(StaffProfile, user=request.user)
    if staff_profile.role != 'verbal_trainer':
        raise PermissionDenied

    if request.method == 'POST' and request.FILES.get('file'):
        VerbalMaterial.objects.create(
            title=request.POST.get('title'),
            file=request.FILES['file'],
            uploaded_by=staff_profile
        )
        messages.success(request, "Material uploaded successfully.")
        return redirect('upload_verbal_material')

    materials = VerbalMaterial.objects.filter(uploaded_by=staff_profile).order_by('-uploaded_at')
    return render(request, 'accounts/upload_verbal.html', {'materials': materials})


@login_required
@staff_required
def delete_verbal_material(request, material_id):
    material = get_object_or_404(VerbalMaterial, id=material_id)
    material.file.delete()
    material.delete()
    messages.success(request, "Material deleted successfully.")
    return redirect('staff_dashboard')


# =======================
# ===== Aptitude Tests ==
# =======================

@login_required
@staff_required
def upload_aptitude_test(request):
    staff_profile = get_object_or_404(StaffProfile, user=request.user)
    if staff_profile.role != 'aptitude_trainer':
        raise PermissionDenied

    if request.method == 'POST' and request.FILES.get('file'):
        AptitudeTest.objects.create(
            title=request.POST['title'],
            file=request.FILES['file'],
            uploaded_by=staff_profile
        )
        messages.success(request, "Aptitude test uploaded successfully.")
        return redirect('upload_aptitude_test')

    tests = AptitudeTest.objects.filter(uploaded_by=staff_profile)
    return render(request, 'accounts/upload_aptitude.html', {'tests': tests})


@login_required
def view_aptitude_tests(request):
    tests = AptitudeTest.objects.all().order_by('-uploaded_at')
    return render(request, 'accounts/view_aptitude_tests.html', {'tests': tests})


# =======================
# ===== Students =======
# =======================

@login_required
@department_coordinator_required
def add_student(request):
    staff_profile = get_object_or_404(StaffProfile, user=request.user)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.department = staff_profile.branch
            student.save()
            messages.success(request, "Student added successfully.")
            return redirect('department_dashboard')
    else:
        form = StudentForm(initial={'department': staff_profile.branch})
    return render(request, 'accounts/add_student.html', {'form': form})


@login_required
@department_coordinator_required
def edit_student(request, student_id):
    staff_profile = get_object_or_404(StaffProfile, user=request.user)
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.department = staff_profile.branch
            student.save()
            messages.success(request, "Student updated successfully.")
            return redirect('department_dashboard')
    else:
        form = StudentForm(instance=student, initial={'department': staff_profile.branch})
    return render(request, 'accounts/edit_student.html', {'form': form, 'student': student})


@login_required
@department_coordinator_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect('department_dashboard')


# =======================
# ===== Staff/Admin =====
# =======================

@login_required
@admin_required
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
            role=request.POST.get('role'),
            branch=request.POST.get('branch')
        )
        messages.success(request, "Staff profile created successfully.")
        return redirect('admin_dashboard')
    return render(request, 'accounts/add_staff.html')


@login_required
@admin_required
def edit_staff(request, staff_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    if request.method == 'POST':
        staff.name = request.POST.get('name')
        staff.designation = request.POST.get('designation')
        staff.mobile = request.POST.get('mobile')
        staff.email = request.POST.get('email')
        staff.role = request.POST.get('role')
        staff.branch = request.POST.get('branch')
        staff.save()
        messages.success(request, "Staff profile updated.")
        return redirect('admin_dashboard')
    return render(request, 'accounts/edit_staff.html', {'staff': staff})


@login_required
@admin_required
def delete_staff(request, staff_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    staff.delete()
    messages.success(request, "Staff profile deleted.")
    return redirect('admin_dashboard')


@login_required
@admin_required
def make_staff_admin(request, staff_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    staff.user.is_staff = True
    staff.user.is_superuser = True
    staff.user.save()
    messages.success(request, f"{staff.name} is now an admin.")
    return redirect('admin_dashboard')


# =======================
# ===== Other Pages =====
# =======================

def home(request):
    return render(request, 'accounts/home.html')


def about(request):
    return render(request, 'accounts/about.html')


def contact_view(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )
        messages.success(request, "Message sent successfully.")
    return render(request, 'accounts/contact.html')


@login_required
@admin_required
def delete_message(request, message_id):
    msg = get_object_or_404(ContactMessage, id=message_id)
    msg.delete()
    messages.success(request, "Message deleted successfully.")
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
@login_required
def upload_resume(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST' and request.FILES.get('resume'):
        student.resume = request.FILES['resume']
        student.save()
        messages.success(request, "Resume uploaded successfully.")
    return render(request, 'accounts/upload_resume.html', {'student': student})
@login_required
@staff_required
def view_students(request):
    students = Student.objects.all().order_by('roll_number')
    return render(request, 'accounts/view_students.html', {'students': students})
@login_required
@staff_required
def view_verbal_material(request):
    staff_profile = get_object_or_404(StaffProfile, user=request.user)
    materials = VerbalMaterial.objects.filter(uploaded_by=staff_profile).order_by('-uploaded_at')
    return render(request, 'accounts/view_verbal.html', {'materials': materials})
