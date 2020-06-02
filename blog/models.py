from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class BlogType(models.Model):
    type_name=models.CharField(max_length=20,verbose_name='博客类型')
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    def __str__(self):
        return self.type_name
        
    class Meta:
        verbose_name='博客类型'
        verbose_name_plural=verbose_name
        
class Blog(models.Model):
    title=models.CharField(max_length=50,verbose_name='标题')
    blog_type=models.ForeignKey(BlogType,on_delete=models.DO_NOTHING,verbose_name='博客类型')
    # content=models.TextField(verbose_name='博客内容')
    # content=RichTextField()
    content=RichTextUploadingField()
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')   
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创作时间')
    last_update_time=models.DateTimeField(auto_now=True,verbose_name='上次修改时间')
    def readnum_function(self):
        try:
            return self.readnum.read_num
        except Exception as e:
            return 0
    readnum_function.short_description='阅读量'
    def __str__(self):
        return self.title
        
    class Meta:
        ordering=['-created_time']
        verbose_name='博客'
        verbose_name_plural=verbose_name
        
class ReadNum(models.Model):
    read_num=models.IntegerField(default=0,verbose_name='阅读量')
    blog=models.OneToOneField(Blog,on_delete=models.CASCADE,verbose_name='博客')
    
    class Meta:
        verbose_name='阅读量'
        verbose_name_plural=verbose_name