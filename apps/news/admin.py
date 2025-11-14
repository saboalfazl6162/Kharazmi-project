from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post
from .actions import actions

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ("title","author","write_date","update_date","is_active","is_pin","is_verify")
    search_fields = ("title","description","author",)
    list_filter = ("write_date","update_date","is_active","is_pin","is_verify")
    readonly_fields = ('write_date','update_date')
    summernote_fields = ("description",)
    date_hierarchy = "write_date"
    fieldsets = (
        ("اطلاعات اصلی", {
            'classes':("wide",),
            'fields': (
                'title','description','thumbnail','author','post_mainpoint'
            ),
        }),
        ("تاریخ ها(فقط خواندن)", {
            'classes':("collapse",),
            'fields': (
                'write_date','update_date'
            ),
        }),
        ("اطلاعات پیشرفته", {
            'classes':("collapse",),
            'fields': (
                'is_active','is_pin','is_verify'
            ),
        }),
        ("اطلاعات سئو", {
            'classes':("collapse",),
            'fields': (
                'meta_name','meta_description','meta_keywords'
            ),
        }),
    )
    actions = actions

