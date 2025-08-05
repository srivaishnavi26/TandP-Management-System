from .models import PlacementDrive
from django.contrib import admin
from .models import StaffProfile

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'designation', 'mobile', 'email')
    search_fields = ('name', 'designation', 'user__username')
    list_filter = ('designation',)


admin.site.register(PlacementDrive)
