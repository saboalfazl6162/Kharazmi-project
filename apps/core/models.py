from django.db import models
from apps.news.models import Post
from apps.users.models import CustomUser

class Comment(models.Model):
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name="نویسنده")
    to = models.ForeignKey(Post,on_delete=models.CASCADE,verbose_name="برای پست")
    content = models.TextField(verbose_name="محتوای")
    reply_to = models.ForeignKey("self",on_delete=models.CASCADE,blank=True,null=True,verbose_name="پاسخ به")
    write_date = models.DateTimeField("تاریخ نوشته شدن",auto_now_add=True)
    is_active = models.BooleanField("فعال",default=False)
    is_verify = models.BooleanField("مورد تائید",default=False)
    is_pin = models.BooleanField("پین",default=False)
    is_check_of_author_post = models.BooleanField("چک شده توسط نویسنده",default=False)
    @property
    def is_reply(self):
        return True if self.reply_to is not None else False
    def __str__(self):
        return self.content if len(self.content) < 50 else self.content[:50] + "..."
    
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"