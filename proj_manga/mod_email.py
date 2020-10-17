import _thread

from proj_manga.mod_imports import *
from proj_manga.mod_safety import s_passdecrypt

from email.mime.application import MIMEApplication


def sendtestmail(email, s_host, s_port, s_pass):
    # 设置email信息
    msg = MIMEMultipart()
    # 邮件主题
    msg['Subject'] = "测试邮件"
    # 发送方信息
    msg['From'] = email
    receivers = [email]
    # 邮件正文是MIMEText:
    msg_content = "从自己邮箱发送至自己，用于测试邮箱是否可用"
    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
    try:
        # QQsmtp服务器的端口号为465或587
        s = smtplib.SMTP_SSL(s_host, s_port)
        s.set_debuglevel(1)
        s.login(email, s_passdecrypt(s_pass))
        # 给receivers列表中的联系人逐个发送邮件
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(email, to, msg.as_string())
            return (0)
    except smtplib.SMTPException as e:
        return (e)

def SendEmail_File(f_email, t_email, s_host, s_port, s_pass, file_path, filename):
    try:
        # 设置email信息
        msg = MIMEMultipart()
        # 邮件主题
        msg['Subject'] = "MangaHelper自动推送"
        # 发送方信息
        msg['From'] = f_email
        receivers = [t_email]
        # 邮件正文是MIMEText:
        msg_content = "MangaHelper自动推送kindle"
        msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))

        file = MIMEApplication(open(file_path, 'rb').read())
        file.add_header('Content-Disposition', 'attachment', filename=filename)

        msg.attach(file)
        # QQ SMTP 服务器的端口号为465或587
        s = smtplib.SMTP_SSL(s_host, s_port)
        s.set_debuglevel(1)
        s.login(f_email, s_passdecrypt(s_pass))
        # 给receivers列表中的联系人逐个发送邮件
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(f_email, to, msg.as_string())
        return (0)
    except smtplib.SMTPException as e:
        return (e)

def sendemail_file(f_email, t_email, s_host, s_port, s_pass, file_path, filename):
    try:
        _thread.start_new_thread(SendEmail_File,(f_email, t_email, s_host, s_port, s_pass, file_path, filename))
        return 0
    except Exception as e:
        return 1