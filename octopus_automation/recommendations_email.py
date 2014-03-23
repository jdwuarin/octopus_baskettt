from octopus_user.models import UserSettings
from django.conf import settings
from datetime import *
import octopus_user
from octopus_recommendation_engine import basket_recommendation_engine
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from humanize import naturaldate


def create_recommendations_then_send_email():

    #go through all user_settings and only take the one that have an attached user
    user_settings_list = UserSettings.objects.filter(user__isnull=False)

    for user_settings in user_settings_list:
        user = user_settings.user
        send_date = user_settings.next_recommendation_email_date

        if not send_date:
            user_settings.next_recommendation_email_date = \
                date.today() + timedelta(days=user_settings.days)
            user_settings.save()

        # now find out if I am on the wanted day for user.

        if date.today() == user_settings.next_recommendation_email_date:
            #generate the recommendations
            basket, __ = basket_recommendation_engine.get_or_create_later_basket(user)

            if not basket:
                # this is a bug, just return for now
                return

            else:
                #send the email from new_basket_email.html
                send_recommendation_mail_to([user.email])

            #send the email


def send_recommendation_mail_to(user):
    template_html = get_template('new_basket_email.html')
    template_text = get_template('new_basket_email.txt')

    #from django.contrib.auth.models import User
    #user = User.objects.get(id=17)
    to = user.email
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = u"Your basket from " + (
        str(date.today()) + " is ready")
    d = Context({'user': user})

    html_content = template_html.render(d)
    text_content = template_text.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()