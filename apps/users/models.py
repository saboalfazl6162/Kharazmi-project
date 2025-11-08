from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def avatar_upload_path(instance, filename):
    now = timezone.now()
    instance_id = instance.pk or "temp"
    return f"users/profiles/{instance_id}/year-{now.year}/month-{now.month}/day-{now.day}/{filename}"

def main_point_upload_path(instance,filename):
    instance_id = instance.pk or "temp"
    return f"users/main_points/thumbnails/{instance_id}/{filename}"


class MainPoint(models.Model):
    name = models.CharField(verbose_name="نام محور")
    thumbnail = models.ImageField(verbose_name="تصویر محور",upload_to=main_point_upload_path,blank=True,null=True)
    description = models.TextField(verbose_name="توضیحات محور",blank=True,null=True)

    class Meta:
        verbose_name = "محور"
        verbose_name_plural = "محورها"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_("ایمیل"))  
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("شماره تلفن"))
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True, verbose_name=_("عکس پروفایل"))
    bio = models.TextField(blank=True, null=True, verbose_name=_("درباره من"))
    is_verified = models.BooleanField(default=False, verbose_name=_("تأیید شده"))
    confirmation_comments = models.BooleanField(default=False,verbose_name="تائیدی بودن نظرات",help_text="اگر فعال باشد نظرات با تائید شما ارسال می شوند")
    main_point = models.ForeignKey(MainPoint,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"