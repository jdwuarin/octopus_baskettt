from octopus_user.models import UserSettings
from datetime import *
import octopus_user


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

            #send the email

            # see if user has some baskets
        ugb = octopus_user.models.UserGeneratedBasket.objects.filter(
            user=user).order_by('created_at')
        urb = octopus_user.models.UserRecommendedBasket.objects.filter(
            user=user).order_by('created_at')
        # find out if recommendation should be made


