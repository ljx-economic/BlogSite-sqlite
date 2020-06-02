from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.DO_NOTHING,verbose_name='用户')
    code=models.CharField(max_length=20,verbose_name='验证码')
    introduction=models.TextField(verbose_name='简介')
    
    class Meta:
        verbose_name='用户信息'
        verbose_name_plural=verbose_name