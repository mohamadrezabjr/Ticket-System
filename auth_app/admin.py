from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User , Provinces , Cities , Profile
from .forms import UserCreationForm , UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        ("User Information",{"fields":("phone" , "password")}),
        ("User Status",{"fields":("is_superuser" , "is_support" , "is_user" , "groups" , "user_permissions")}),
    )

    add_fieldsets = (
        ("Create User",{"fields":("phone" , "password", "confirm_password")}),
    )

    list_display = ["id" , "phone" , "is_superuser", "is_support", "is_user"]
    list_filter = ["is_superuser", "is_support", "is_user"]
    search_fields = ["phone"]
    ordering = ["-id"]
    filter_horizontal = ("groups" , "user_permissions")

    def get_fieldsets(self, request, obj = None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            fieldsets = (
                ("User Status",{"fields":("phone" , "password" ,"is_superuser" , "is_support" , "is_user")}),
            )
        return fieldsets
    
    def get_form(self, request, obj = None , **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields["is_superuser"].disabled = True
            form.base_fields["is_support"].disabled = True 
            form.base_fields["is_user"].disabled = True
        return form

admin.site.register(User,UserAdmin)
admin.site.register(Provinces)
admin.site.register(Cities)
admin.site.register(Profile)