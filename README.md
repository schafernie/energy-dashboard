# Energy Dashboard

ELT pipeline that pulls electricity consumption data from [SMARD](https://www.smard.de/) (the German electricity market data platform) and loads it into Postgres on a schedule, orchestrated by Airflow. The data is plottet in a small web dashboard for inspecting the data.

## Stack

- **Airflow** (`apache/airflow:2.9.3`) : scheduling and orchestration
- **Postgres 17** : raw data storage (`db`) and Airflow metadata DB
- **Python** (pandas, psycopg2, requests) : the loading script
- **dbt-core + dbt-postgres** (1.8.2) : SQL transformations on top of the raw data
- **FastAPI + Uvicorn** : API serving the loaded data
- **Plotly.js** : charting in the dashboard frontend

## Structure

- `src/airflow/dags/` : DAG definitions (`elt_dag.py`)
- `src/loading/` : ELT scripts (`load_from_smard.py`, `db.py`) mounted into the Airflow containers
- `src/sql_init/init.sql` : schema applied to `db` on first startup
- `src/transform/` : dbt project (`dbt_project.yml`, `profiles/profiles.yml`) mounted into the Airflow containers
  - `models/staging/stg_total_consumption.sql` : view over the raw `total_consumption` source table
  - `models/marts/avg_yearly_consumption.sql` : average consumption per year (`year`, `avg_total_consumption_mwh`), built on top of the staging model
- `src/api/main.py` : FastAPI app (`app`) exposing `/api/load`, `/api/load_avg_yearly`, and serving the dashboard
- `src/app/` : dashboard frontend (`index.html`, `plot.js`, Plotly)
- `compose.yml` : services: `db_serv`, `airflow_db_serv`, `airflow_init_serv`, `airflow_webserver_serv`, `airflow_scheduler_serv`, `app_serv`

## Running

```bash
docker compose up -d
```

- Dashboard: [http://localhost:8000](http://localhost:8000)
- Airflow UI: [http://localhost:8080](http://localhost:8080) (username `user`, password `secret`)
- Raw Postgres DB: `localhost:5433` (username `user`, password `secret`, db `db`)

The `extract_load_and_transform` DAG runs hourly and has two tasks:

1. `run_loading_from_smard_script` : loads the **Stromverbrauch: Gesamt (Netzlast)** (total electricity consumption / total grid load) series from SMARD into the `total_consumption` table.
2. `dbt_run` : runs the dbt project (`--full-refresh`) to (re)build the staging view and the `avg_yearly_consumption` mart from the raw data.

The dashboard queries this data via `/api/load` (time series) and `/api/load_avg_yearly` (yearly average, mart-backed) and plots both with Plotly.

To trigger the DAG manually instead of waiting for the hourly schedule:

```bash
docker exec energy-dashboard-airflow_scheduler_serv-1 airflow dags trigger extract_load_and_transform
```