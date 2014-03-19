
from django.core.mail import send_mail


def send_reminder_email():

    # first get the next basket for all users that need will be doing their
    # groceries soon




    send_mail('Subject here', 'Here is the message.', "unused@unused.com",
        recipient_list=['john.dwuarin@gmail.com'], fail_silently=False)