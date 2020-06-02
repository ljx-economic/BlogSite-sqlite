from django.db import models
from django.contrib.auth.models import User
from blog.models import Blog

# Create your models here.
class Comment(models.Model):
    comment_blog=models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='博客标题')
    text=models.TextField(verbose_name='评论内容')
    comment_time=models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    
    parent=models.ForeignKey('self',related_name='parent_comment',null=True,blank=True,on_delete=models.CASCADE,verbose_name='父级评论')
    root=models.ForeignKey('self',related_name='root_comment',null=True,blank=True,on_delete=models.CASCADE,verbose_name='根评论')
    
    def __str__(self):
        return self.text
    
    class Meta:
        ordering=['-comment_time']
        verbose_name='评论'
        verbose_name_plural=verbose_name