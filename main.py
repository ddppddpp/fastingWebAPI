# api that accepts a date as a query param and returns an int (0..6) as resposne
from typing import Optional, List
from datetime import date, datetime, timedelta

import pydantic
import calendar
from context import bgchof
from bgchof import getStatusForDate
from fastapi import FastAPI, Query
from pydantic import BaseModel, conint


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


app = FastAPI()


@app.get("/fastingStatus/date", response_model=dateStatus)
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
@app.get("/fastingStatus/week", response_model=List[dateStatus])
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
@app.get("/fastingStatus/month", response_model=List[dateStatus])
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
