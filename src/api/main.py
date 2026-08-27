

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)) 

from loading.raw_db import load_table_as_series


app=FastAPI()



@app.get("/api/load")
def get_load(start_date, end_date):

    table_name="total_consumption"
    rows=load_table_as_series(table_name,start_date, end_date)
    date_time, value_mwh = zip(*rows) if rows else ((), ())
    series = {
                 "date_time": date_time,
                 "value_mwh": value_mwh
    }
    data={table_name: series}
    return data


app.mount("/", StaticFiles(directory=Path(__file__).resolve().parent.parent / "app", html=True), name="app")