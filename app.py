from flask import Flask, render_template, jsonify, url_for, g
import sqlite3
import pandas as pd

app = Flask(__name__)

# Carregar dados
DATABASE = '.\\Data\\data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

try:
    df = pd.read_csv("data.csv")
    print("Dados carregados com sucesso!")
except Exception as e:
    print("Erro ao carregar dados:", e)
    df = pd.DataFrame()

@app.route()
def hello(name):
    return url_for('get_all_data')

@app.route('/')
def index():
    if df.empty:
        return "Erro: Dados não carregados. Verifique o arquivo data.csv."
    
    min_year = int(df['YEAR_SOLD'].min())
    max_year = int(df['YEAR_SOLD'].max())
    print(f"Ano mínimo: {min_year}, Ano máximo: {max_year}")
    return render_template('map.html', 
                         min_year=min_year,
                         max_year=max_year)

@app.route('/data/<int:year>')
def get_data(year):
    try:
        filtered = df[df['YEAR_SOLD'] == year]
        if filtered.empty:
            return jsonify({"error": "Nenhum dado encontrado para este ano."}), 404
        
        min_price = filtered['SALE PRICE'].min()
        max_price = filtered['SALE PRICE'].max()
        
        data = filtered[['LATITUDE', 'LONGITUDE', 'SALE PRICE']].to_dict(orient='records')
        return jsonify({
            'data': data,
            'min_price': min_price,
            'max_price': max_price
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/data/all')
def get_all_data():
    try:
        min_price = df['SALE PRICE'].min()
        max_price = df['SALE PRICE'].max()
        
        data = df[['LATITUDE', 'LONGITUDE', 'SALE PRICE']].to_dict(orient='records')
        return jsonify({
            'data': data,
            'min_price': min_price,
            'max_price': max_price
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)