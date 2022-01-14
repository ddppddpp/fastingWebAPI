# api that accepts a date as a query param and returns an int (0..6) as resposne
from typing import Optional, List
from datetime import date, datetime, timedelta
import calendar
import sys, os

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


class dateStatus(BaseModel):
    the_date: date
    status: conint(ge=0, le=6)


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
openapi_prefix = f"/{stage}" if stage else "/"

# hardcode to 'dev
app = FastAPI(title="Orthodox Fasting Dietary Status", openapi_prefix="/dev")

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


# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)
# def handler(event, context):
# return "Hello from AWS Lambda using Python" + sys.version + "!"


# to make it run locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
