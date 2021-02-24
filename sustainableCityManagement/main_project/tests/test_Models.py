# Standard library imports...
from unittest.mock import Mock, patch

# Third-party imports...
from nose.tools import assert_is_not_none, assert_list_equal, assert_true

# Local imports...
from main_project.tests.services import get_location, get_bikedata_day, get_bikedata_minutes


@patch('main_project.tests.services.requests.get')
def test_get_day_request_response(mock_get):
    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = True

    # Call the service, which will send a request to the server.
    response = get_location()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)


@patch('main_project.tests.services.requests.get')
def test_get_minutes_request_response(mock_get):
    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = True

    # Call the service, which will send a request to the server.
    response = get_bikedata_day(0)

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)


@patch('main_project.tests.services.requests.get')
def test_getting_todos(mock_get):
    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = True

    # Call the service, which will send a request to the server.
    response = get_bikedata_minutes()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)


def test_location_contract():
    # Call the service to hit the actual API.
    actual = get_location()
    actual_keys = actual.json().pop().keys()

    # Call the service to hit the mocked API.
    with patch('main_project.tests.services.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = [
            {
                "st_ADDRESS": "Clarendon Row",
                "st_CONTRACTNAME": "Dublin",
                "st_ID": 1,
                "st_LATITUDE": 53.340927,
                "st_LONGITUDE": -6.262501,
                "st_NAME": "CLARENDON ROW"
            }]

        mocked = get_location()
        mocked_keys = mocked.json().pop().keys()

    # An object from the actual API and an object from the mocked API should have
    # the same data structure.
    assert_list_equal(list(actual_keys), list(mocked_keys))


def test_bikedata_contract():
    # Call the service to hit the actual API.
    actual = get_bikedata_day(0)
    actual_keys = actual.json().pop().keys()

    # Call the service to hit the mocked API.
    with patch('main_project.tests.services.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = [
            {
                "address": "Heuston Bridge (South)",
                "banking": "False",
                "historic": [
                    {
                        "available_bike_stands": 0,
                        "available_bikes": 25,
                        "bike_stands": 25,
                        "status": "open",
                        "time": "2019-03-08T20:00:05Z"
                    }],
                "id": 100,
                "latitude": 53.347107,
                "longitude": -6.292041,
                "name": "HEUSTON BRIDGE (SOUTH)"}]

        mocked = get_bikedata_day(0)
        mocked_keys = mocked.json().pop().keys()

    # An object from the actual API and an object from the mocked API should have
    # the same data structure.
    assert_list_equal(list(actual_keys), list(mocked_keys))
