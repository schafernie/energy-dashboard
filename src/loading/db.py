
import psycopg2 #PostgreSQL driver for interacting with database via python  
import os


HOST = os.getenv("DB_HOST", "db_serv")
PORT = os.getenv("DB_PORT", "5432")
USER = os.getenv("DB_USER", "user")
PASSWORD = os.getenv("DB_PASSWORD", "secret")
DB_NAME = os.getenv("DB_NAME", "db")
TABLE_NAMES=["total_consumption","forecast_total_consumption"] 



def get_connection():
    connection = psycopg2.connect(
            host = HOST,
            port = PORT, 
            user = USER, 
            password = PASSWORD,
            dbname = DB_NAME 
            )
    return connection 


def insert_rows(table_name, rows):
    connection = get_connection()
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
    connection.close()


def load_table_as_series(table_name,start_date=None, end_date=None):
    connection = get_connection() 
    with connection.cursor() as cursor:
        if start_date == None or end_date == None:
            cursor.execute(
                        f"""
                        SELECT date_time, value_mwh FROM {table_name}; 
                        """
                    )
            rows = cursor.fetchall()
        else:
            cursor.execute(
            f"""
            SELECT date_time, value_mwh FROM {table_name}
            WHERE date_time BETWEEN %s AND %s;
            """,
            (start_date, end_date)
            )
            rows = cursor.fetchall() 
    connection.close()
    return rows





def get_earliest_time(table_name):
    connection = get_connection() 
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT min(date_time) FROM {table_name};  
            """
        )
        earliest = cursor.fetchone()[0]    
    connection.close()
    return earliest




def get_latest_time(table_name):
    connection = get_connection() 
    with connection.cursor() as cursor:
        cursor.execute(
        f"""
        SELECT max(date_time) FROM {table_name}; 
        """
        )
        latest= cursor.fetchone()[0]
    connection.close()
    return latest


def load_avg_yearly_total_consumption():
    connection = get_connection() 
    with connection.cursor() as cursor:
            cursor.execute(
            f"""
            SELECT year, avg_total_consumption_mwh FROM avg_yearly_consumption
            ORDER BY year ASC;
            """
            )
            rows = cursor.fetchall() 
    connection.close()
    return rows





if __name__=="__main__":
    print("testing")

    ''' 
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
    '''
 

    



