from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os

from crontab import CronTab

class Command(BaseCommand):
    help = "Automatically run archive issue."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #init cron, get virtualenv information
        cron = CronTab(user=True)
        virtualenv = os.environ.get('VIRTUAL_ENV', None)
        archive_path = os.path.dirname(os.path.realpath(__file__))

        #add new cron job
        job = cron.new(command="{}/bin/python3 {}/run.py".format(virtualenv, archive_path))

        #set job to run quarterly (every 3 months)
        job.month.every(3)

        cron.write()