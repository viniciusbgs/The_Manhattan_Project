import sqlite3
import pandas as pd
from pathlib import Path

DATA = Path("Data") / Path("data.csv")

df = pd.read_csv(DATA)
conn = sqlite3.connect(DATA.parent / 'data.db')

# Rename the columns to avoid spaces
df.rename(columns={
    'ZIP CODE': 'ZIP_CODE',
    'RESIDENTIAL UNITS': 'RESIDENTIAL_UNITS',
    'COMMERCIAL UNITS': 'COMMERCIAL_UNITS',
    'LAND SQUARE FEET': 'LAND_SQUARE_FEET',
    'GROSS_SQUARE_FEET': 'GROSS_SQUARE_FEET',
    'SALE PRICE': 'SALE_PRICE',
    }, inplace=True)

df.to_sql('ManhattanSales', conn, if_exists='replace', index=False)
conn.close()