from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        count_tries = 0
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections["default"]
                db_conn.cursor()
                count_tries += 1
            except OperationalError:
                if count_tries == 5:
                    raise CommandError("Database unavailable.")

                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write("Database connected.")
