import csv

import psycopg

from django.conf import settings
from django.core.management.base import BaseCommand


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


def import_collects(csv_file: str):
    cur = con.cursor()
    with open(csv_file, "r") as f:
        with cur.copy(
            "COPY collects_collect "
            "(id,name,cause,description,goal_amount,current_amount,"
            "bakers_count,image,close_date,author_id) "
            "FROM STDIN"
        ) as copy:
            for line in csv.reader(f):
                copy.write_row(line)
    set_max_id = (
        "SELECT setval('collects_collect_id_seq', "
        "(SELECT MAX(id) FROM collects_collect));"
    )
    cur.execute(set_max_id)
    con.commit()
    con.close()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, filename, *args, **options):
        import_collects(filename)
