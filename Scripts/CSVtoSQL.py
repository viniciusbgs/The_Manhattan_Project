import sqlite3
import pandas as pd

df = pd.read_csv("Data\\data.csv")
conn = sqlite3.connect('data.db')
df.to_sql('Manhattan Sales', conn, if_exists='replace', index=False)
conn.close()