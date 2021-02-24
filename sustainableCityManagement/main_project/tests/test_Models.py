

# Standard library imports...
import pytest
from pytest_mock import mocker
# Local imports...
from main_project.services import get_todos

""" @pytest.mark.django_db
def test_save_bike_stands_location(client, user_data):
    user_model = get_user_model()
    assert user_model.objects.count() == 0
    location_url = urls.reverse(
        'https://dublinbikes.staging.derilinx.com/api/v1/resources/stations')
    resp = client.post(location_url, user_data)
    assert user_model.objects.count() == 1
    assert resp.status_code == 200 """
