from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os

from crontab import CronTab

class Command(BaseCommand):
    help = "Set up cron job to automatically run archives."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #init cron, get virtualenv information
        cron = CronTab(user=True)
        virtualenv = os.environ.get('VIRTUAL_ENV', None)

        #add new cron job
        job = cron.new(command="{}/bin/python {}/manage.py create_archive".format(virtualenv, settings.BASE_DIR), comment="Automatic journal archiving")

        #set job to run quarterly (every 3 months)
        job.setall('0 0 1 */3 *')
        
        cron.write()
