import smtplib
from email.mime.text import MIMEText
def send_mail(name,email,subject,message,namet,emailt,phonet,date,time,peoplet,messaget):
    port=2525
    smtp_server="smtp.mailtrap.io"
    login="ae62bddbdeac9d"
    password="9359477476febf"
    message=f"<h3>new message sub</h3><ul><li>name:{name}</li><li>email:{email}</li><li>subject:{subject}</li><li>message:{message}</li><li>namet:{namet}</li><li>emailt:{emailt}</li><li>phonet:{phonet}</li><li>date:{date}</li><li>time:{time}</li><li>peoplet:{peoplet}</li><li>messaget:{messaget}</li></ul>"
    
    sender_email='jamiu@ajenipa.com'
    receiver_email='email2@example.com'
    msg = MIMEText(message,'html')
    msg['Subject']="RESTAURANT"
    msg['From']='sender_email'
    msg['To']='receiver_email'
    #send mail
    with smtplib.SMTP(smtp_server, port) as server:
        server.login("ae62bddbdeac9d", "9359477476febf")
        server.sendmail(sender_email, receiver_email, msg.as_string())
