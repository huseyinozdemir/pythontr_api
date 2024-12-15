import time
import sys
from django.db import connections
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        connected = False
        while not connected:
            try:
                db_conn = connections["default"]
                if 'test' not in sys.argv:
                    db_conn.ensure_connection()
                self.stdout.write('Database is ready!...')
                connected = True
            except (OperationalError, Psycopg2Error):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
