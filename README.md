# Energy Dashboard

ELT pipeline that pulls electricity consumption data from [SMARD](https://www.smard.de/) (the German electricity market data platform) and loads it into Postgres on a schedule, orchestrated by Airflow.

## Stack

- **Airflow** (`apache/airflow:2.9.3`) — scheduling and orchestration
- **Postgres 17** — raw data storage (`raw_db`) and Airflow metadata DB
- **Python** (pandas, psycopg2, requests) — the loading script

## Structure

- `src/airflow/dags/` — DAG definitions (`elt_dag.py`)
- `src/loading/` — ELT scripts (`load_from_smard.py`, `raw_db.py`) mounted into the Airflow containers
- `src/sql/init.sql` — schema applied to `raw_db` on first startup
- `compose.yml` — services: `raw_db_serv`, `airflow_db_serv`, `airflow_init_serv`, `airflow_webserver`, `airflow_scheduler`

## Running

```bash
docker compose up -d
```

- Airflow UI: [http://localhost:8080](http://localhost:8080) (username `airflow`, password `secret`)
- Raw Postgres DB: `localhost:5433` (username `user`, password `secret`, db `raw_db`)

The `loading_data_from_smard` DAG runs every 5 minutes, loading electricity consumption data into the `total_consumption` table.