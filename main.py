# api that accepts a date as a query param and returns an int (0..6) as resposne
from typing import Optional
from datetime import date, datetime

import pydantic
from context import bgchof
from bgchof import getStatusForDate
from fastapi import FastAPI, Query
from pydantic import BaseModel, conint


class dateStatus(BaseModel):
    the_date: date
    status: conint(ge=0, le=6)


app = FastAPI()


@app.get("/fastingStatus", response_model=dateStatus)
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
