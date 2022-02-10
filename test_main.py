from http import client
from urllib import request, response
from requests import Request
from datetime import date

from fastapi.testclient import TestClient


from .main import app, firstDayOfWeekforDate

client = TestClient(app)


def test_first_day_of_week_for_date():
    assert firstDayOfWeekforDate(
        date.fromisoformat("2022-01-20")
    ) == date.fromisoformat("2022-01-17")


def test_get_fastingstatus_date():
    response = client.get("/fastingStatus/date", headers={"inputDate": "2022-01-20"})
    assert response.status_code == 200
    assert response.json() == {"the_date": "2022-01-20", "status": 6}


def test_get_fastingstatus_week():
    response = client.get("/fastingStatus/week", headers={"inputDate": "2022-01-20"})
    assert response.status_code == 200
    assert response.json() == [
        {"the_date": "2022-01-17", "status": 6},
        {"the_date": "2022-01-18", "status": 6},
        {"the_date": "2022-01-19", "status": 4},
        {"the_date": "2022-01-20", "status": 6},
        {"the_date": "2022-01-21", "status": 4},
        {"the_date": "2022-01-22", "status": 6},
        {"the_date": "2022-01-23", "status": 6},
    ]


def test_get_fastingstatus_month():
    response = client.get("/fastingStatus/month", headers={"inputDate": "2022-01-20"})
    assert response.status_code == 200
    assert response.json() == [
        {"the_date": "2022-01-01", "status": 6},
        {"the_date": "2022-01-02", "status": 6},
        {"the_date": "2022-01-03", "status": 6},
        {"the_date": "2022-01-04", "status": 6},
        {"the_date": "2022-01-05", "status": 2},
        {"the_date": "2022-01-06", "status": 6},
        {"the_date": "2022-01-07", "status": 4},
        {"the_date": "2022-01-08", "status": 6},
        {"the_date": "2022-01-09", "status": 6},
        {"the_date": "2022-01-10", "status": 6},
        {"the_date": "2022-01-11", "status": 6},
        {"the_date": "2022-01-12", "status": 4},
        {"the_date": "2022-01-13", "status": 6},
        {"the_date": "2022-01-14", "status": 4},
        {"the_date": "2022-01-15", "status": 6},
        {"the_date": "2022-01-16", "status": 6},
        {"the_date": "2022-01-17", "status": 6},
        {"the_date": "2022-01-18", "status": 6},
        {"the_date": "2022-01-19", "status": 4},
        {"the_date": "2022-01-20", "status": 6},
        {"the_date": "2022-01-21", "status": 4},
        {"the_date": "2022-01-22", "status": 6},
        {"the_date": "2022-01-23", "status": 6},
        {"the_date": "2022-01-24", "status": 6},
        {"the_date": "2022-01-25", "status": 6},
        {"the_date": "2022-01-26", "status": 4},
        {"the_date": "2022-01-27", "status": 6},
        {"the_date": "2022-01-28", "status": 4},
        {"the_date": "2022-01-29", "status": 6},
        {"the_date": "2022-01-30", "status": 6},
        {"the_date": "2022-01-31", "status": 6},
    ]
