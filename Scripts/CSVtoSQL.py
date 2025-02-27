import sqlite3
import pandas as pd
from pathlib import Path

DATA = Path("Data") / Path("data.csv")

df = pd.read_csv(DATA)
conn = sqlite3.connect(DATA.parent / 'data.db')
df.to_sql('ManhattanSales', conn, if_exists='replace', index=False)
conn.close()