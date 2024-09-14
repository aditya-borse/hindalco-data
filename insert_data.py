import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT 

db_params = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}

csv_file_path = 'HINDALCO.csv'

def create_table_if_not_exists(cur):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS stock_data (
        id SERIAL PRIMARY KEY,
        datetime TIMESTAMP,
        close DECIMAL(10, 2),
        high DECIMAL(10, 2),
        low DECIMAL(10, 2),
        open DECIMAL(10, 2),
        volume INTEGER,
        instrument VARCHAR(20)
    );
    '''
    cur.execute(create_table_query)

def insert_data_from_csv(csv_path, conn):
    df = pd.read_csv(csv_path)
    
    df['datetime'] = pd.to_datetime(df['datetime'], format='%d-%m-%Y %H:%M')
    
    cur = conn.cursor()
    
    create_table_if_not_exists(cur)
    
    insert_query = sql.SQL('''
    INSERT INTO stock_data (datetime, close, high, low, open, volume, instrument)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''')
    
    for _, row in df.iterrows():
        cur.execute(insert_query, (
            row['datetime'],
            row['close'],
            row['high'],
            row['low'],
            row['open'],
            row['volume'],
            row['instrument']
        ))
    
    conn.commit()
    
    cur.close()

def main():
    try:
        conn = psycopg2.connect(**db_params)
        
        insert_data_from_csv(csv_file_path, conn)
        
        print("Data inserted successfully!")
    
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")
    
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()