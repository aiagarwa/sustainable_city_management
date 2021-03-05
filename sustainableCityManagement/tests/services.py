# Standard library imports...
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# Third-party imports...
import requests
from datetime import datetime, timedelta
import pytz

# Local imports...
BASE_URL = 'https://dublinbikes.staging.derilinx.com/api/v1/resources/'

LOCATION_URL = urljoin(BASE_URL, 'stations')


def get_location():
    response = requests.get(LOCATION_URL)
    if response.ok:
        return response
    else:
        return None


def get_bikedata_day(days_historical):
    now_time = datetime.now(pytz.utc)
    curr_time = (now_time - timedelta(days=days_historical)
                 ).strftime("%Y%m%d%H%M")
    delay_time = (now_time - timedelta(days=days_historical + 1)
                  ).strftime("%Y%m%d%H%M")
    url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom=" + \
        str(delay_time)+"&dto="+str(curr_time)
    response = requests.get(url)
    if response.ok:
        return response
    else:
        return None


def get_bikedata_minutes():
    now_time = datetime.now(pytz.utc)
    curr_time = now_time.strftime("%Y%m%d%H%M")
    url = ""
    delay_time = (now_time - timedelta(minutes=5)).strftime("%Y%m%d%H%M")
    url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom=" + \
        str(delay_time)+"&dto="+str(curr_time)
    response = requests.get(url)
    if response.ok:
        return response
    else:
        return None
