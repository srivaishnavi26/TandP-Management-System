from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
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
    package = models.DecimalField(max_digits=10, decimal_places=2)
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
