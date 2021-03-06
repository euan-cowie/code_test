import csv
from django.core.management.base import BaseCommand, CommandError
from code_test.flight_data.models import Flight, Segment, Airport


def format_none(val):
    if val == '':
        return None
    return val


# TODO - tidy up minor code duplication - open csv
def bulk_create_flight(context, file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        next(csv_reader)
        objs = [
            Flight(
                id=row[0], dep_air_id=row[1], dest_air_id=row[2], in_depart_code_id=format_none(row[3]),
                in_arrive_code_id=format_none(row[4]), out_flight_no=row[5], out_depart_date=format_none(row[6]),
                out_depart_time=row[7], out_arrival_date=format_none(row[8]), out_arrival_time=row[9],
                out_booking_class=row[10], out_flight_class=row[11], out_carrier_code=row[12],
                in_flight_no=row[13], in_depart_date=format_none(row[14]), in_depart_time=row[15],
                in_arrival_date=format_none(row[16]), in_arrival_time=row[17], in_booking_class=row[18],
                in_flight_class=row[19], in_carrier_code=row[20], original_price=row[21],
                original_currency=row[22], reservation=row[23], carrier=row[24], oneway=row[25],
            )
            for row in csv_reader
        ]
        # TODO - should be an update from flat file - dockerization hack
        if not Flight.objects.exists():
            count = len(Flight.objects.bulk_create(objs))

    context.stdout.write(context.style.SUCCESS(f'Processed {count} Flight rows.'))


def bulk_create_segment(context, file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        next(csv_reader)
        objs = [
            Segment(
                flight_id=row[0], dep_code_id=row[1], arr_code_id=row[2], dep_date=format_none(row[3]),
                arr_date=format_none(row[4]), dep_time=row[5], arr_time=row[6], dep_terminal=row[7],
                arr_terminal=row[8], flight_no=row[9], journey=row[10], seg_class=row[11],
                booking_class=row[12],
            )
            for row in csv_reader
        ]
        if not Segment.objects.exists():
            count = len(Segment.objects.bulk_create(objs))

    context.stdout.write(context.style.SUCCESS(f'Processed {count} Segment rows.'))


def bulk_create_airport(context, file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        next(csv_reader)
        objs = [
            Airport(
                iata_code=row[9], name=row[2], continent=row[4], iso_country=row[5],
            )
            for row in csv_reader if row[9] and row[1] != 'closed'
        ]
        if not Airport.objects.exists():
            count = len(Airport.objects.bulk_create(objs, ignore_conflicts=True))

    context.stdout.write(context.style.SUCCESS(f'Processed {count} Airport rows.'))


class Command(BaseCommand):
    help = 'Updates the Flight Data from flat file'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = options['file_path']
        model_name = options['model'].lower()

        if model_name == 'flight':
            bulk_create_flight(self, file_path)
        elif model_name == 'segment':
            bulk_create_segment(self, file_path)
        elif model_name == 'airport':
            bulk_create_airport(self, file_path)
        else:
            raise CommandError(f'Model "{model_name.title()}" does not exist')
