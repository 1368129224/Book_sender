import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(to_addr, path, file_name):
    from_addr = 'zzc1368129224@qq.com'
    password = 'igntewjxbovxgdhb'
    smtp_server = 'smtp.qq.com'
    msg = MIMEMultipart()
    msg["Subject"] = "send book"
    msg["From"] =  from_addr
    msg["To"] =  to_addr
    file = MIMEApplication(open(os.path.join(path, file_name), 'rb').read())
    file.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(file)
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=2)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        return 0
    except Exception as e:
        print(e)
        return -1

if __name__ == '__main__':
    pass
