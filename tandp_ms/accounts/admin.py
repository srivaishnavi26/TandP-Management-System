from .models import PlacementDrive
from django.contrib import admin
from .models import StaffProfile
from .models import Student  # import your model

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'designation', 'mobile', 'email')
    search_fields = ('name', 'designation', 'user__username')
    list_filter = ('designation',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'roll_number', 'branch', 'graduation_year')
    search_fields = ('full_name', 'roll_number', 'email', 'branch')

admin.site.register(PlacementDrive)
