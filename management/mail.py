from django.core.mail import send_mail
import uuid
from django.conf import settings


def send_forget_password_email(email,token):
    subject = 'Your forget password link '
    message = f'Click on the below link to reset your password \n http://192.168.143.106:8000/password/change/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return True