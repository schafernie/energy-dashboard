

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)) 

from loading.db import load_table_as_series, load_avg_yearly_total_consumption


app=FastAPI()



@app.get("/api/load")
def load_table_from_db(start_date, end_date):

    table_name="total_consumption"
    rows=load_table_as_series(table_name,start_date, end_date)
    date_time, value_mwh = zip(*rows) if rows else ((), ())
    series = {
                 "date_time": date_time,
                 "value_mwh": value_mwh
    }
    data={table_name: series}
    return data


@app.get("/api/load_avg_yearly")
def load_avg_yearly_total_consumption_from_db():
    rows=load_avg_yearly_total_consumption()
    year, avg_mwh = zip(*rows) if rows else ((), ())
    series = {
                 "year": year,
                 "avg_mwh": avg_mwh
    }
    data={"avg_yearly_total_consumption": series}
    return data






app.mount("/", StaticFiles(directory=Path(__file__).resolve().parent.parent / "app", html=True), name="app")