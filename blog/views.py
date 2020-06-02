from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import Blog,BlogType,ReadNum
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.
def blog_list(request,username):
    page_num=request.GET.get('page',1)#获取页面参数(request.GET是字典)，page_num是字符串
    user=User.objects.get(username=username)
    blogs_all_list=Blog.objects.filter(author=user)
    paginator=Paginator(blogs_all_list,5)#每5个进行分页
    page_of_blogs=paginator.get_page(page_num)
    
    blog_types=BlogType.objects.filter(author=user)
    my_blog_types=[]
    for blog_type in blog_types:# 添加每种类型对应的博客数量，利用python可以临时添加实例变量和类变量的属性
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        my_blog_types.append(blog_type)
    
    context={}
    context['page_of_blogs']=page_of_blogs
    context['blog_types']=my_blog_types
    context['author']=username
    return render(request,'blog_list.html',context)
    
def blog_detail(request,blog_pk):
    context={}
    blog=get_object_or_404(Blog,pk=blog_pk)
    #阅读量加一
    if not request.COOKIES.get('blog_%s_read'%blog_pk):#字典
        if ReadNum.objects.filter(blog=blog).count():
            #存在记录
            readnum=ReadNum.objects.get(blog=blog)
            readnum.read_num+=1
            readnum.save()
        else:
            #不存在记录
            readnum=ReadNum()
            readnum.read_num=1
            readnum.blog=blog
            readnum.save()
    #获取评论
    comments=Comment.objects.filter(comment_blog=blog,parent=None)
    
    context['previous_blog']=Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog']=Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog']=blog
    context['comments']=comments
    context['comment_form']=CommentForm(initial={'object_blog':blog.title,'object_id':blog_pk,'reply_comment_id':0})#设置表单value
    response=render(request,'blog_detail.html',context)
    response.set_cookie('blog_%s_read'%blog_pk,'true',max_age=600)
    return response
    
def blogs_with_type(request,blog_type_pk):#参数变量名必须与urls中的相同
    page_num=request.GET.get('page',1)#获取页面参数(request.GET是字典)
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)# 是个对象
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)
    paginator=Paginator(blogs_all_list,5)#每3页进行分页
    page_of_blogs=paginator.get_page(page_num)#django特有的,错误就第一页/实际是最后一页
    
    blog_types=BlogType.objects.filter(author=blog_type.author)
    my_blog_types=[]
    for per_blog_type in blog_types:# 添加每种类型对应的博客数量，利用python可以临时添加实例变量和类变量的属性
        per_blog_type.blog_count = Blog.objects.filter(blog_type=per_blog_type).count()
        my_blog_types.append(per_blog_type)
    
    context={}
    #blog_type=get_object_or_404(BlogType,pk=blog_type_pk)# 是个对象
    #context['blogs']=Blog.objects.filter(blog_type=blog_type)
    context['page_of_blogs']=page_of_blogs# 加的
    context['blog_type']=blog_type
    context['blog_types']=my_blog_types
    return render(request,'blogs_with_type.html',context)

# 博客管理    
def blog_manage(request):
    user=User.objects.get(username=request.user.username)
    my_blogs=Blog.objects.filter(author=user)
    
    context={}
    context['my_blogs']=my_blogs
    context['count']=my_blogs.count()
    return render(request,'blog_manage.html',context)
    
def blog_add(request):# 增加博客
    if request.method=='POST':
        title=request.POST.get('title','')
        blog_type_pk=int(request.POST.get('blog_type',''))
        blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
        content=request.POST.get('content','')
        user=User.objects.get(username=request.user.username)
        b=Blog(title=title,blog_type=blog_type,content=content,author=user)# 开始增加博客
        b.save()
        return redirect(reverse('blog_manage'))
    user=User.objects.get(username=request.user.username)  
    context={}
    context['blog_types']=BlogType.objects.filter(author=user)
    return render(request,'blog_add.html',context)
    
def blog_change(request,blog_pk):# 修改博客
    if request.method=='POST':
        title=request.POST.get('title','')
        blog_type_pk=int(request.POST.get('blog_type',''))
        blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
        content=request.POST.get('content','')
        b=get_object_or_404(Blog,pk=blog_pk)# 获取博客
        if b.author.username==request.user.username:# 验证是否是本作者要修改博客
            b.title=title # 开始修改博客
            b.blog_type=blog_type
            b.content=content
            b.save()
            return redirect(reverse('blog_manage'))
    user=User.objects.get(username=request.user.username)
    blog=get_object_or_404(Blog,pk=blog_pk)
    if user.username==blog.author.username:# 验证是否是本人要修改博客
        context={}
        context['blog']=blog
        context['blog_types']=BlogType.objects.filter(author=user)
        return render(request,'blog_change.html',context)
    
def blog_delete(request,blog_pk):# 删除博客
    blog=get_object_or_404(Blog,pk=blog_pk)
    if blog.author.username==request.user.username:# 验证是否是本作者要删除博客
        blog.delete()
    return redirect(reverse('blog_manage'))

# 博客类型管理    
def blog_type_manage(request):
    user=User.objects.get(username=request.user.username)
    blog_types=BlogType.objects.filter(author=user)
    my_blog_types=[]
    for blog_type in blog_types:# 添加每种类型对应的博客数量，利用python可以临时添加实例变量和类变量的属性
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        my_blog_types.append(blog_type)
    context={}
    context['my_blog_types']=my_blog_types
    context['count']=blog_types.count()
    return render(request,'blog_type_manage.html',context)
    
def blog_type_add(request):# 增加博客类型
    if request.method=='POST':
        blog_type=request.POST.get('blog_type','')
        user=User.objects.get(username=request.user.username)
        bt=BlogType(type_name=blog_type,author=user)# 开始增加博客
        bt.save()
        return redirect(reverse('blog_type_manage'))  
    context={}
    return render(request,'blog_type_add.html',context)
    
def blog_type_change(request,blog_type_pk):# 修改博客类型
    if request.method=='POST':
        blog_type=request.POST.get('blog_type','')
        bt=get_object_or_404(BlogType,pk=blog_type_pk)# 获取博客类型
        if bt.author.username==request.user.username:# 验证是否是本作者要修改博客类型
            bt.type_name=blog_type
            bt.save()
            return redirect(reverse('blog_type_manage'))
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    if blog_type.author.username==request.user.username:# 验证是否是本作者要修改博客类型
        context={}
        context['blog_type']=blog_type
        return render(request,'blog_type_change.html',context)
        
def blog_type_delete(request,blog_type_pk):# 删除博客类型
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    if blog_type.author.username==request.user.username:# 验证是否是本作者要删除博客类型
        blog_type.delete()
    return redirect(reverse('blog_type_manage'))