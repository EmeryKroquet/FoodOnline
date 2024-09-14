from django.contrib import admin
from .models import Vendor
from .models import OpeningHour

class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'user', 'is_approved', 'created_at', 'modified_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('vendor_name', 'user__email', 'user__username')  # You can search by vendor name, user email, and username
    prepopulated_fields = {'vendor_slug': ('vendor_name',)}  # Automatically fill the slug field based on vendor_name
    readonly_fields = ('created_at', 'modified_at')

    # Adding inline to view related user information
    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj:
            from accounts.admin import UserProfileInline  # Assuming you have this inline defined in accounts admin
            inlines.append(UserProfileInline(self.model, self.admin_site))
        return inlines


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour', 'is_closed')
    list_filter = ('vendor', 'day', 'is_closed')
    search_fields = ('vendor__vendor_name',)
    ordering = ('day', 'from_hour')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # During editing
            return ['vendor', 'day']
        return []


admin.site.register(OpeningHour, OpeningHourAdmin)

admin.site.register(Vendor, VendorAdmin)
