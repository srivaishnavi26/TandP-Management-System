from django.db import models
from django.contrib.auth.models import User

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.role})"
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    branch = models.CharField(max_length=50)
    graduation_year = models.IntegerField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class PlacementDrive(models.Model):
    company_name = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    date = models.DateField()
    package = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.company_name} - {self.job_role}"
class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    drive = models.ForeignKey(PlacementDrive, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'drive')

    def __str__(self):
        return f"{self.student.roll_number} registered for {self.drive.company_name}"

class VerbalMaterial(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='verbal_materials/')
    uploaded_by = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

class AptitudeTest(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='aptitude_tests/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
