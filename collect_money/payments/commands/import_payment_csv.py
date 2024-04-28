import csv
import csv

from django.core.management.base import BaseCommand
from django.conf import settings
import psycopg

dbname = settings.DATABASES["default"]["NAME"]
user = settings.DATABASES["default"]["USER"]
password = settings.DATABASES["default"]["PASSWORD"]
host = settings.DATABASES["default"]["HOST"]
port = settings.DATABASES["default"]["PORT"]

con = psycopg.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port,
)


def import_payments(csv_file: str):
    cur = con.cursor()
    with open(csv_file, "r") as f:
        with cur.copy(
            "COPY payments_payment "
            "(id,amount,date,collect_id,user_id) "
            "FROM STDIN"
        ) as copy:
            for line in csv.reader(f):
                copy.write_row(line)
    set_max_id = (
        "SELECT setval('payments_payment_id_seq', "
        "(SELECT MAX(id) FROM payments_payment));"
    )
    cur.execute(set_max_id)
    con.commit()
    con.close()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, filename, *args, **options):
        import_payments(filename)
