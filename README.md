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
python manage.py runserver
```

For Bike Location density :

Use  http://127.0.0.1:8000/main/bikestands_details/?type=live for latest data.

Use  http://127.0.0.1:8000/main/bikestands_details/?type=historical for 1 day historical data.

Use  http://127.0.0.1:8000/main/bikestands_details/?type=locations for locations data.


