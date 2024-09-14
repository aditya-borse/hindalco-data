import unittest
import pandas as pd
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT 

db_params = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}

def fetch_data_from_db():
    """Fetches stock data from the database."""
    conn = psycopg2.connect(**db_params)
    query = "SELECT * FROM stock_data ORDER BY datetime"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def load_and_validate_data():
    """Loads data from the database and converts datetime column to datetime type."""
    df = fetch_data_from_db()
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

df = load_and_validate_data()

class TestDataValidation(unittest.TestCase):

    def test_decimal_columns(self):
        """Check if open, high, low, and close columns are decimal type."""
        decimal_cols = ['open', 'high', 'low', 'close']
        for col in decimal_cols:
            self.assertTrue(pd.api.types.is_numeric_dtype(df[col]), 
                            f"Column '{col}' should be decimal type.")

    def test_volume_integer(self):
        """Check if volume column is integer type."""
        self.assertTrue(pd.api.types.is_integer_dtype(df['volume']), 
                        "Column 'volume' should be integer type.")

    def test_instrument_string(self):
        """Check if instrument column is string type."""
        self.assertTrue(pd.api.types.is_string_dtype(df['instrument']), 
                        "Column 'instrument' should be string type.")

    def test_datetime_datetime(self):
        """Check if datetime column is datetime type."""
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['datetime']), 
                        "Column 'datetime' should be datetime type.")

if __name__ == '__main__':
    unittest.main()