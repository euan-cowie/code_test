## With Docker (recommended!)

In the uppermost `code_test/` directory, run the following: 

```shell script
docker-compose -f local.yml up --build
```

Then head to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Cheers :)

## Without Docker
Assuming you have python3.8 installed, check with:
```shell script
python3 --version
```

First, make the uppermost `code_test/` directory your working 
directory and create a virtualenv:
```shell script
cd <user_path>/code_test
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:
```shell script
pip install -r requirements.txt
```

Finally, run the following commands from the root directory to 
get it working
```shell script
python manage.py makemigrations
python manage.py migrate
python manage.py parse_data airport data/airport-codes_csv.csv
python manage.py parse_data flight data/flighdata_B.csv
python manage.py parse_data segment data/flighdata_B_segments.csv
python manage.py runserver 127.0.0.1:8000
```

Then head to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Thank you :)