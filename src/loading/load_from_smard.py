    
from datetime import datetime, timezone
import requests
import raw_db



SMARD_URL = "https://www.smard.de/app"
REGION = "DE-LU"
TIME_RESOLUTION = "hour" 


TABLES_INFO = {
        "total_consumption" : 410
}



def load_table(table_name,connection,since):
    
    #get timestamps
    data_id=TABLES_INFO[table_name]
    url = f"{SMARD_URL}/chart_data/{data_id}/{REGION}/index_{TIME_RESOLUTION}.json"
    response=requests.get(url,timeout=30)
    response.raise_for_status()
    smard_timestamps = response.json()['timestamps']
    smard_timestamps = sorted(smard_timestamps)
    smard_since = int(since.timestamp() * 1000)
    if smard_since >= max(smard_timestamps):
        smard_timestamps=smard_timestamps[-1:]    
    else:
        for i, t in enumerate(smard_timestamps):
            if t > smard_since:
                if i>0:
                    smard_timestamps=smard_timestamps[i-1:]
                break

    #fetch data        
    rows=[]
    for t in smard_timestamps:  
        print(t/max(smard_timestamps))
        url = (
               f"{SMARD_URL}/chart_data/{data_id}/{REGION}/"
               f"{data_id}_{REGION}_{TIME_RESOLUTION}_{t}.json"
               ) 
        response = requests.get(url,timeout=30) 
        response.raise_for_status()
        series = response.json()["series"]
        for i, elem in enumerate(series):
            if not None in elem:
                time = datetime.fromtimestamp(elem[0]/1000,tz=timezone.utc)
                value=elem[1]
                row = (time, REGION, value)
                rows.append(row)

    #insert to data base    
    raw_db.insert_rows(connection, table_name, rows)
    print(f"table {table_name} with data id {data_id} was sucsessfully inserted to raw db.")


if __name__=="__main__":
    #parameters
    since = datetime(2025,1,1,0,0,0,tzinfo=timezone.utc) #earlist time in tabel
    table_name="total_consumption"

    #insert data
    connection=raw_db.get_connection()
    earliest=raw_db.get_earliest_time(connection,table_name)
    latest=raw_db.get_latest_time(connection,table_name)
    if earliest is not None and latest is not None:
        if earliest <= since:    
            since = latest
    load_table(table_name,connection,since)
    connection.close()


        