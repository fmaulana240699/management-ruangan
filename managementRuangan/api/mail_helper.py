import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient_email, subject, message):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465) 
    server.login("fajar.8251@widyatama.ac.id", "")

    msg = MIMEMultipart()
    msg['From'] = "fajar.8251@widyatama.ac.id"
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Send the email
    server.sendmail("fajar.8251@widyatama.ac.id", recipient_email, msg.as_string())
    server.quit()

