from proj_manga.mod_imports import *
def sendtestmail(email,s_host,s_port,s_pass):
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
        s.login(email, s_pass)
        # 给receivers列表中的联系人逐个发送邮件
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(email, to, msg.as_string())
            return(0)
    except smtplib.SMTPException as e:
        return(e)