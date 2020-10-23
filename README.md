Run the following commands from the root directory to get it working

```shell script
python manage.py makemigrations
python manage.py migrate
python manage.py parse_data airport data/airport-codes_csv.csv
python manage.py parse_data flight data/flighdata_B.csv
python manage.py parse_data segment data/flighdata_B_segments.csv
python manage.py runserver 127.0.0.1:8000
```