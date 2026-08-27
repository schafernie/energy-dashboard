# Energy Dashboard

ELT pipeline that pulls electricity consumption data from [SMARD](https://www.smard.de/) (the German electricity market data platform) and loads it into Postgres on a schedule, orchestrated by Airflow. The data is plottet in a small web dashboard for inspecting the data.

## Stack

- **Airflow** (`apache/airflow:2.9.3`) : scheduling and orchestration
- **Postgres 17** : raw data storage (`raw_db`) and Airflow metadata DB
- **Python** (pandas, psycopg2, requests) : the loading script
- **FastAPI + Uvicorn** : API serving the loaded data
- **Plotly.js** : charting in the dashboard frontend

## Structure

- `src/airflow/dags/` : DAG definitions (`elt_dag.py`)
- `src/loading/` : ELT scripts (`load_from_smard.py`, `raw_db.py`) mounted into the Airflow containers
- `src/sql/init.sql` : schema applied to `raw_db` on first startup
- `src/api/main.py` : FastAPI app (`app`) exposing `/api/load` and serving the dashboard
- `src/app/` : dashboard frontend (`index.html`, `plot.js`, Plotly)
- `compose.yml` : services: `raw_db_serv`, `airflow_db_serv`, `airflow_init_serv`, `airflow_webserver`, `airflow_scheduler`, `app_serv`

## Running

```bash
docker compose up -d
```

- Dashboard: [http://localhost:8000](http://localhost:8000)
- Airflow UI: [http://localhost:8080](http://localhost:8080) (username `user`, password `secret`)
- Raw Postgres DB: `localhost:5433` (username `user`, password `secret`, db `raw_db`)

The `loading_data_from_smard` DAG runs hourly, loading the **Stromverbrauch: Gesamt (Netzlast)** (total electricity consumption / total grid load) series from SMARD into the `total_consumption` table. The dashboard queries this data via `/api/load` and plots it with Plotly.