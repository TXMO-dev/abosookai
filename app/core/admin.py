from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as \
    BaseUserAdmin
from core import models
from django.utils.translation import gettext as _

# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email',
                    'name',
                    'phone_number',
                    'user_type',
                    'address',
                    'city',
                    'state',
                    'zip',
                    'description',
                    'get_following',     
                    'is_active',
                    'is_staff']  
    fieldsets = (
        (_('Personal Information'), {
            "fields": (
                'name',
                'email',
                'description',
                'phone_number',
                'address',
                'city',
                'state',
                'zip'
            ),
        }),
        (_('Category'), {
            "fields": (
                'user_type',
                
            ),
        }),
        (_('Settings'), {
            "fields": (
                'is_active',
                'is_staff'
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email','password1','password2'),  
        }),
    )
    

admin.site.register(models.User, UserAdmin)                   
