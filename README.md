# Sustainable City Management

Make a directory, say sustainable_city_managment.
```
mkdir sustainable_city_managment
git clone https://gitlab.scss.tcd.ie/fleschb/sustainable-city-management.git
virtualenv -p python .
source bin/activate
cd sustainable-city-management
pip install -r requirements.txt
cd sustainableCityManagement
python manage.py runserver --noreload
```

Crontab setting (to regularly fetch data from third-party APIs):
```
python manage.py cronjob add
python manage.py cronjob show
```

For Bike Location density :

Use  http://127.0.0.1:8000/main/bikestands_details/?type=historical&days_historic=5 for 5 day historical data.

Use  http://127.0.0.1:8000/main/bikestands_details/?type=locations for locations data.

Use http://127.0.0.1:8000/main/bikestands_graph/?location_based=no&days_historic=5 for getting the graph values (overall).

use http://127.0.0.1:8000/main/bikestands_graph/?location_based=yes&days_historic=5 for getting the graph values (location based).