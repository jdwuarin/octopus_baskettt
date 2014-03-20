import sanitize_database


def recommendation_automation():

    #go through all user_settings and only take the one that have an attached user
    sanitize_database.clean_user_settings()

    pass

