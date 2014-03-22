from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Sanitizes the db (removes dangling data form db, updates in_stock flag etc...)'

    def handle(self, *args, **options):

        sanitize_database.clean_user_settings()
        self.stdout.write('Done cleaning user_settings')
        sanitize_database.set_in_stock_flag()
        self.stdout.write('Done setting user_settings')