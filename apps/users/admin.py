from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import CustomUser,MainPoint
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, SummernoteModelAdmin):
    
    list_display = ["username", "first_name", "last_name", "date_joined"]

    date_hierarchy = "date_joined"

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    readonly_fields = ("date_joined", "last_login")

    summernote_fields = ("bio",)

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "first_name", "last_name",
                "phone_number", "password1", "password2",
            ),
        }),
    )

    fieldsets = (
        ("فیلدهای ضروری", {
            "classes": ("wide",),
            "fields": ("username", "password", "email", "phone_number"),
        }),
        ("اطلاعات شخصی", {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "avatar", "bio",),
        }),
        ("اطلاعات پیشرفته", {
            "classes": ("collapse",),
            "fields": ("is_verified", "is_staff", "is_active", "is_superuser"),
        }),
        ("تاریخ‌ها", {
            "classes": ("collapse",),
            "fields": ("date_joined", "last_login"),
        }),
    )


@admin.register(MainPoint)
class MainPointAdmin(SummernoteModelAdmin):
    
    list_display = ['name',]


    readonly_fields = ("date_joined", "last_login")

    summernote_fields = ("description",)