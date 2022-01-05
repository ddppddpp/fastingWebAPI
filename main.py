# api that accepts a date as a query param and returns an int (0..6) as resposne
from typing import Optional, List
from datetime import date, datetime, timedelta
from fastapi import FastAPI, Query, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, conint
import calendar

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


app = FastAPI()

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
        description="Date in YYYY-MM-DD format for which to calculate the Fasting Status. If Empty defaults to today.",
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
