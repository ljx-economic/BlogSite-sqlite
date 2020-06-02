# 我的qq邮箱授权码：quzkwfziitoggdea
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import random

'''生成随机验证码'''
def code(n=6):
    s = ''
    for i in range(n):
        num = random.randint(0,9)
        s = s + str(num)
    print(s)
    return s

'''发送电子邮件'''
def send(my_email,license_code,dest_email,msg_subject,msg_content):
    #如名字所示Multipart就是分多个部分，构造一个MIMEMultipart对象代表邮件本身 
    msg = MIMEMultipart() 
    msg["Subject"] = msg_subject
    msg["From"]  = my_email
    msg["To"]   = dest_email
    #---这是文字部分--- 
    part = MIMEText(msg_content)
    msg.attach(part)
    #连接、登录、发送
    s = smtplib.SMTP("smtp.qq.com", timeout=30)#连接smtp邮件服务器,端口默认是25 
    s.login(my_email, license_code)#登陆服务器 
    s.sendmail(my_email, dest_email, msg.as_string())#发送邮件 
    s.close()
    print('发送成功')

if __name__=="__main__":
    my_email = '1084578612@qq.com'
    license_code = 'uretsbdogxlmjbja'
    dest_email = '15826774141@163.com'
    msg_subject = '验证码'
    msg_content = code()
    send(my_email,license_code,dest_email,msg_subject,msg_content)
