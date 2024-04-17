from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import CustomUser, Manager, Employee, Customer


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'get_groups', 'is_active',
                    'is_superuser', 'date_joined', 'last_login')

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

    def get_groups(self, obj):
        return ', '.join([group.name for group in obj.groups.all()])

    get_groups.short_description = 'Group / Role'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile')


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile')
