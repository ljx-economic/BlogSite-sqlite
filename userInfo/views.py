from django.shortcuts import render,render_to_response,redirect
from django.contrib import auth
from .forms import *
from django.contrib.auth.models import User
from .emailAPI.send_code import code,send
from .models import UserInfo
    
def login(request):
    if request.method=='POST':
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            user=auth.authenticate(request,username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect(request.GET.get('from','/'))
            else:
                login_form.add_error(None,'用户名或密码不正确')
    else:
        login_form=LoginForm()
    context={}
    context['login_form']=login_form
    return render(request,'login.html',context)
    
def register(request):
    if request.method=='POST':
        reg_form=RegForm(request.POST)
        if reg_form.is_valid():
            username=reg_form.cleaned_data['username']
            email=reg_form.cleaned_data['email']
            password=reg_form.cleaned_data['password']
            #创建用户
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            #向扩展的用户列表中添加信息
            ve_code=code()
            introduction="这个人很懒，什么都没写"
            user_info=UserInfo(user=user,code=ve_code,introduction=introduction)
            user_info.save()
            #登录用户
            user=auth.authenticate(request,username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from','/'))
    else:
        reg_form=RegForm()
    context={}
    context['reg_form']=reg_form
    return render(request,'register.html',context)
    
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from','/'))
    
def forget(request):
    context={}
    return render(request,'forget.html',context)
    
def ve_code(request):
    my_email = '1084578612@qq.com'
    license_code = 'uretsbdogxlmjbja'
    dest_email = request.POST.get('email','')
    msg_subject = '验证码'
    msg_content = code()
    
    # 存入数据库
    try:
        user=User.objects.get(email=dest_email)# 如果找不到会报错
    except:
        context={}
        return render(request,'email_error.html',context)
    user_info=UserInfo.objects.get(user=user)
    user_info.code=msg_content
    user_info.save()
    print(user_info)
    
    # 发送验证码
    try:
        send(my_email,license_code,dest_email,msg_subject,msg_content)
    except:
        print('验证码发送失败了')
        
    context={}
    context['email']=dest_email
    return render(request,'ve_code.html',context)
    
def change_password(request):
    if request.method=='POST':
        dest_email = request.POST.get('email','')
        user=User.objects.get(email=dest_email)# 如果找不到会报错
        user_info=UserInfo.objects.get(user=user)
        if user_info.code==request.POST.get('code',''):# 验证码是否匹配           
            context={}
            context['email']=dest_email
            return render(request,'change_password.html',context)
        else:
            context={}
            return render(request,'code_error.html',context)
    user=User.objects.get(username=request.user.username)    # 在个人中心中修改密码
    context={}
    context['email']=user.email
    return render(request,'change_password.html',context)
            
# 还没验证前后密码是否输入一致            
def change(request):
    if request.method=='POST':
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        user=User.objects.get(email=email)
        username=user.username# 获取用户名
        user.set_password(password)
        user.save()
        #登录用户
        user=auth.authenticate(request,username=username,password=password)
        auth.login(request,user)
        return redirect(request.GET.get('from','/'))
        
def change_info(request):
    if request.method=='POST':
        change_info_form=ChangeInfoForm(request.POST)
        if change_info_form.is_valid():
            username=change_info_form.cleaned_data['username']
            text=change_info_form.cleaned_data['text']
            # 开始修改数据库
            user=User.objects.get(username=request.user.username)
            user.username=username
            request.user.username=username # 修改request
            user.save()
            user_info=UserInfo.objects.get(user=user)
            user_info.introduction=text
            user_info.save()
            change_info_form=ChangeInfoForm(initial={'username':user.username,'text':user_info.introduction}) #设置表单value
    else:
        print(request.user.username)
        user=User.objects.get(username=request.user.username)
        user_info=UserInfo.objects.get(user=user)
        change_info_form=ChangeInfoForm(initial={'username':user.username,'text':user_info.introduction}) #设置表单value
    context={}
    context['change_info_form']=change_info_form
    return render(request,'change_info.html',context)
    
    