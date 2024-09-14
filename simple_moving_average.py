import pandas as pd
import psycopg2
from psycopg2 import sql
import numpy as np
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT 

db_params = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}

def fetch_data_from_db():
    conn = psycopg2.connect(**db_params)
    query = "SELECT * FROM stock_data ORDER BY datetime"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = fetch_data_from_db()

df['datetime'] = pd.to_datetime(df['datetime'])

df.set_index('datetime', inplace=True)

short_window = 20
long_window = 100

df['short_sma'] = df['close'].rolling(window=short_window, min_periods=1).mean()
df['long_sma'] = df['close'].rolling(window=long_window, min_periods=1).mean()

df['signal'] = 0
df['signal'][short_window:] = np.where(df['short_sma'][short_window:] > df['long_sma'][short_window:], 1, 0)
df['position'] = df['signal'].diff()

df['returns'] = df['close'].pct_change()
df['strategy_returns'] = df['returns'] * df['signal'].shift(1)

df['cumulative_returns'] = (1 + df['returns']).cumprod()
df['cumulative_strategy_returns'] = (1 + df['strategy_returns']).cumprod()

print(df[['close', 'short_sma', 'long_sma', 'signal', 'position', 'returns', 'strategy_returns']])
print(f"Strategy Final Return: {df['cumulative_strategy_returns'].iloc[-1]}")
print(f"Buy and Hold Final Return: {df['cumulative_returns'].iloc[-1]}")