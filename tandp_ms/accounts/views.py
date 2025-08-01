from django.shortcuts import render

def home(request):
    return render(request, 'accounts/home.html')

def admin_login(request):
    return render(request, 'accounts/admin_login.html')

def student_login(request):
    return render(request, 'accounts/student_login.html')
