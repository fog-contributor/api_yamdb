from django.contrib import admin

from .models import User

# class CustomUserAdmin(UserAdmin):
#     model = User
#     # list_display = ['email', 'username',]


admin.site.register(User)
