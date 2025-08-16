import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import json

def validate_email(email):
    """简易邮箱格式验证"""
    return '@' in email and '.' in email.split('@')[-1]

def WYsend_email(request,WYEmail_SMTP_CONFIG):
    # 获取请求参数
    data = request
    
    # 参数校验
    if not data or 'email' not in data or 'content' not in data:
        return "缺少必要参数：email 或 content"
    
    if not validate_email(data['email']):
        return "邮箱格式不正确"

    # 构建邮件
    try:
        msg = MIMEText(data['content'], 'plain', 'utf-8')
        
        # 发件人设置（关键！必须与登录账号完全一致）
        msg['From'] = formataddr((
            str(Header(WYEmail_SMTP_CONFIG['sender_name'], 'utf-8')),
            WYEmail_SMTP_CONFIG['username']  # 实际发件地址
        ))
        
        msg['To'] = data['email']
        msg['Subject'] = Header('系统通知', 'utf-8')
        msg['X-SMTPAPI'] = json.dumps({"to": [data['email']]})
        print(msg)
        # 发送邮件
        with smtplib.SMTP_SSL(WYEmail_SMTP_CONFIG['server'], WYEmail_SMTP_CONFIG['port']) as server:
            server.login(WYEmail_SMTP_CONFIG['username'], WYEmail_SMTP_CONFIG['password'])
            server.sendmail(
                WYEmail_SMTP_CONFIG['username'], 
                [data['email']], 
                msg.as_string()
            )
        return "发送成功"

    except smtplib.SMTPAuthenticationError:
        return "SMTP认证失败，请检查账号/授权码"
    except smtplib.SMTPException as e:
        return  f"邮件发送失败"
    except Exception as e:
        return  e
