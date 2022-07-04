from django.contrib.admin.options import BaseModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from customer.models import Customer, User


class UserModelAdmin(UserAdmin):
    list_display = (
        'first_name',
        'last_name',
        'phone',
    )
    list_display_links = (
        'first_name',
        'last_name'
    )


class CustomerModelAdmin(BaseModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'phone',
        'email',
        'company',
        'reference'
    )
    list_display_links = (
        'first_name',
        'last_name',
        'email'
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'reference',)


admin.site.register(User)
admin.site.register(Customer)
