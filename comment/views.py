from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import Comment
from blog.models import Blog
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def update_comment(request):
    text=request.POST.get('text','')# request.POST是字典
    if text=='':
        return render(request,'error.html',{'message':'评论内容为空'})
    object_id=int(request.POST.get('object_id',''))# request.POST是字典
    object_blog=request.POST.get('object_blog','')# request.POST是字典
    reply_comment_id=int(request.POST.get('reply_comment_id',''))
    
    comment=Comment()
    if reply_comment_id==0:
        comment.parent=None
        comment.root=None
    else:
        comment.parent=get_object_or_404(Comment,pk=reply_comment_id)
        if comment.parent.root==None:
            comment.root=comment.parent
        else:
            comment.root=comment.parent.root
    
    comment.user=request.user
    comment.text=text
    blog=get_object_or_404(Blog,pk=object_id)
    comment.comment_blog=blog
    comment.save()
    # 返回数据
    data={}
    data['status']="SUCCESS"
    data['username']=comment.user.username
    # data['comment_time']=comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
    data['text']=comment.text
    data['pk']=comment.pk
    if reply_comment_id!=0: #如果是回复评论，增加被回复人
        data['reply_to']=comment.parent.user.username
    return JsonResponse(data)
    #referer=request.META.get('HTTP_REFERER','/')# 回到原来的页面
    #return redirect(referer)
    
# 评论管理
def comment_manage(request):
    user=User.objects.get(username=request.user.username)
    my_comments=Comment.objects.filter(user=user)
    
    context={}
    context['my_comments']=my_comments
    context['count']=my_comments.count()
    return render(request,'comment_manage.html',context)
    
def comment_change(request,comment_pk):
    if request.method=='POST':
        text=request.POST.get('text','')
        c=get_object_or_404(Comment,pk=comment_pk)# 获取评论
        if c.user.username==request.user.username:# 验证是否是本人要修改评论
            c.text=text
            c.save()
            return redirect(reverse('comment_manage'))
    user=User.objects.get(username=request.user.username)
    comment=get_object_or_404(Comment,pk=comment_pk)
    if user.username==comment.user.username:# 验证当前用户是否是评论者
        context={}
        context['comment']=comment
        return render(request,'comment_change.html',context)
        
def comment_delete(request,comment_pk):# 删除评论
    comment=get_object_or_404(Comment,pk=comment_pk)
    if comment.user.username==request.user.username:# 验证是否是本人要删除评论
        comment.delete()
    return redirect(reverse('comment_manage'))