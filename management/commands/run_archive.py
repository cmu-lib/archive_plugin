from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os

from crontab import CronTab

class Command(BaseCommand):
    help = "Set up crontask to automatically run archives."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #init cron, get virtualenv information
        cron = CronTab(user=True)
        virtualenv = os.environ.get('VIRTUAL_ENV', None)

        #add new cron job
        job = cron.new(command="{}/bin/python3 {}/manage.py create_archive".format(virtualenv, settings.BASE_DIR))


        #set job to run quarterly (every 3 months)
        job.month.every(3)

        cron.write()