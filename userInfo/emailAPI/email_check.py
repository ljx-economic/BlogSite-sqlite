import re

def is_email(mail):
    ma=re.match(r'[a-zA-Z0-9]{1,20}@(163|126|qq)\.com$',mail)
    if ma:
        return True
    else:
        return False

if __name__=="__main__":
    mails=['1@163.com','%65566@163.com哈','bond@126.com',\
           'hello1111@qq.com','234@163.com','12345678901234567890@163.com']
    for mail in mails:
        print(is_email(mail))
        
