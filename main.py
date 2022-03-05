# api that accepts a date as a query param and returns an int (0..6) as resposne
from pickletools import int4
from typing import Optional, List
from datetime import date, datetime, timedelta
import calendar
import sys, os
from unittest import result

from mangum import Mangum
import uvicorn
from fastapi import FastAPI, Query, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, conint

# TODO: Add this line
from starlette.middleware.cors import CORSMiddleware

import bgchof
from bgchof import getStatusForDate
from calculateEasterSunday import calcEaster


class dateStatus(BaseModel):
    the_date: date
    status: conint(ge=0, le=6)


class dateResponse(BaseModel):
    the_year: int
    EasterSunday: date


def firstDayOfWeekforDate(inputDate: date):
    dayOfWeek = inputDate.weekday()
    weeknumber = inputDate.isocalendar()[1]
    resultFirstDayOfWeek = datetime.strptime(
        f"{inputDate.year}-{weeknumber}-1", "%Y-%W-%w"
    ).date()
    return resultFirstDayOfWeek


templates = Jinja2Templates(directory="templates")

# use this to expose the docs in AWS
stage = os.environ.get("STAGE", None)
openapi_prefix_uri = f"/{stage}/openapi.json" if stage else "/openapi.json"
docs_url = f"/{stage}/docs" if stage else "/docs"
redoc_url = f"/{stage}/redoc" if stage else "/redoc"
root_path = f"/{stage}" if stage else "/"

# add description
my_descripiton = """
Orthodox Fasting Dietary Status API that returns a status code for dates.

## fastingStatus/date
Returns a date status, consisting of the inputDate and integer (0..6) showing the status for inputDate. Date format should be YYYY-MM-DD.

## fastingStatus/week
Returns a list of date statuses, consisting of the inputDate and integer (0..6) showing the status for the week in which inputDate falls. Date format should be YYYY-MM-DD.

## fastingStatus/month
Returns a list of date statuses, consisting of the inputDate and integer (0..6) showing the status for the month in which inputDate falls. Date format should be YYYY-MM-DD.

"""


# hardcode docs to 'dev. try chainging openapi_url to openapi_prefix
app = FastAPI(
    title="Orthodox Fasting Dietary Status",
    description=my_descripiton,
    version="0.2",
    contact={"name": "Ivailo Djilianov", "email": "djidji.perroto@gmail.com"},
    license_info={
        "name": "GNU GPLv3",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html",
    },
    #    openapi_url="/dev/openapi.json",
    # openapi_url=openapi_prefix_uri,
    # docs_url=docs_url,
    # redoc_url=redoc_url,
    root_path=root_path,
    # now try with stage
    # openapi_prefix=stage,
)

# TODO: Add these lines
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["x-apigateway-header", "Content-Type", "X-Amz-Date"],
)


# index.html
@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get(
    "/fastingStatus/date", response_model=dateStatus, status_code=status.HTTP_200_OK
)
async def read_items(
    inputDate: Optional[date] = Query(
        None,
        description="Date in YYYY-MM-DD format for which to calculate the Fasting Status. If Empty defaults to today.",
    )
):
    if inputDate:
        theDate = inputDate
    else:
        theDate = date.today()

    result = {"the_date": theDate, "status": bgchof.getStatusForDate(theDate)}
    return result


# week of dates
@app.get(
    "/fastingStatus/week",
    response_model=List[dateStatus],
    status_code=status.HTTP_200_OK,
)
async def read_items(
    inputDate: Optional[date] = Query(
        None,
        description="Date in YYYY-MM-DD format within the week for which to calculate the Fasting Status. If Empty defaults to today.",
    )
):
    if inputDate:
        theDate = inputDate
    else:
        theDate = date.today()
    mondayForThisWeek = firstDayOfWeekforDate(theDate)

    result = list[dateStatus]()
    for i in range(0, 7):
        tempDate = mondayForThisWeek + timedelta(days=i)
        result.append(
            {"the_date": tempDate, "status": bgchof.getStatusForDate(tempDate)}
        )
    return result


# month of dates
@app.get(
    "/fastingStatus/month",
    response_model=List[dateStatus],
    status_code=status.HTTP_200_OK,
)
async def read_items(
    inputDate: Optional[date] = Query(
        None,
        description="Date in YYYY-MM-DD format for which to calculate the Fasting Status. If Empty defaults to today.",
    )
):
    if inputDate:
        theDate = inputDate
    else:
        theDate = date.today()
    result = list[dateStatus]()
    for i in range(1, calendar.monthrange(theDate.year, theDate.month)[1] + 1):
        tempDate = date(theDate.year, theDate.month, i)
        result.append(
            {"the_date": tempDate, "status": bgchof.getStatusForDate(tempDate)}
        )
    return result


@app.get(
    "/calculateEasterSunday/",
    response_model=dateResponse,
    status_code=status.HTTP_200_OK,
)
async def read_items(
    inputYear: Optional[int] = Query(
        None,
        description="Year number in YYYY format for which to calculate the Easter Sunday. If Empty defaults to today.",
    )
):
    if inputYear:
        theYear = inputYear
    else:
        theYear = date.today().year

    result = {"the_year": theYear, "EasterSunday": calcEaster(int(theYear))}
    return result


# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)
# def handler(event, context):
# return "Hello from AWS Lambda using Python" + sys.version + "!"


# to make it run locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
