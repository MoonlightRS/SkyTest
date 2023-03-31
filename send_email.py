
from django.conf import settings
from django.core.mail import send_mail

def send_email(user_email, checked_file):
    subject = 'File Checked'
    message = 'Your file {} has been checked and the result is {}'.format(checked_file.file.name, checked_file.result)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)