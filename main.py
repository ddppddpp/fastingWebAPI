# api that accepts a date as a query param and returns an int (0..6) as resposne
from typing import Optional
from datetime import date, datetime
from context import bgchof
from bgchof import getStatusForDate
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/fastingStatus")
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
    result = {"date": theDate, "status": bgchof.getStatusForDate(theDate)}
    return result
