
import psycopg2 #PostgreSQL driver for interacting with database via python  



HOST = "raw_db_serv"
PORT = "5432"
USER = "user"
PASSWORD = "secret"
DB_NAME = "raw_db"

TABLE_NAMES=["total_consumption","forecast"] 



def get_connection():
    connection = psycopg2.connect(
            host = HOST,
            port = PORT, 
            user = USER, 
            password = PASSWORD,
            dbname = DB_NAME 
            )
    return connection 


def insert_rows(connection, table_name, rows):
    with connection.cursor() as cursor:
        cursor.executemany(
            f"""
            INSERT INTO {table_name} (date_time, bidding_zone, value_mwh)
            VALUES (%s, %s, %s)
            ON CONFLICT (date_time, bidding_zone)
                DO UPDATE SET value_mwh = EXCLUDED.value_mwh
            """,
            rows
        )
        connection.commit() #make insert permanent


def load_table_as_series(connection, table_name):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT date_time, value_mwh FROM {table_name}; 
            """
        )
        rows = cursor.fetchall() 
    return rows


def get_earliest_time(connection, table_name):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT date_time FROM {table_name} 
            ORDER BY date_time ASC LIMIT 1;  
            """
        )
        earliest = cursor.fetchone() 
    if earliest:
        return earliest[0]
    else:
        return None



def get_latest_time(connection,table_name):
    with connection.cursor() as cursor:
        cursor.execute(
        f"""
        SELECT date_time FROM {table_name}
        ORDER BY date_time DESC LIMIT 1; 
        """
        )
        latest = cursor.fetchone()
    if latest:
        return latest[0]
    else:
        return None




if __name__=="__main__":
    print("testing")
    from datetime import datetime, timezone,timedelta
   # time_stamp = datetime(2026,1,1,tzinfo=timezone.utc)
    #print(time_stamp)
  #  row=(time_stamp, 'DE-LU',-1)
   # rows=[row]
   # row=(time_stamp+timedelta(1),'DE-LU',-2)
   # rows.append(row)
    connection = get_connection() 
    table_name = "total_consumption"
   # insert_rows(connection, table_name, rows)
    earliest=get_earliest_time(connection,table_name)
    latest=get_latest_time(connection,table_name)
    print(earliest)
    print(latest)
    
    t1=earliest
    t2=earliest+timedelta(49)

    import pandas as pd 
    from matplotlib import pyplot as plt 

    series = load_table_as_series(connection,table_name)
    df = pd.DataFrame(series, columns=['date_time','value_mwh'])
    mask = df['date_time'].between(t1,t2)

    df_window = df[mask]

    fig, ax = plt.subplots( )
    ax.set_xlabel('day and time')
    ax.set_ylabel('measurements in MWh')

    ax.plot(df_window['date_time'],df_window['value_mwh'])







   # since = datetime(2025,1,1,tzinfo=timezone.utc)
    
 

    



