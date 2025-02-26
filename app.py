from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imoveis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de dados
class Imovel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    year_sold = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'LATITUDE': self.latitude,
            'LONGITUDE': self.longitude,
            'SALE PRICE': self.sale_price
        }

# Função para inicializar o banco de dados
def init_db():
    # Cria as tabelas
    with app.app_context():
        db.create_all()
        
        # Verifica se já existem dados no banco
        if Imovel.query.count() == 0:
            try:
                # Importa dados do CSV se disponível
                df = pd.read_csv("Data/data.csv")
                print("Dados do CSV carregados com sucesso! Importando para o banco de dados...")
                
                # Importa os dados para o banco
                for index, row in df.iterrows():
                    novo_imovel = Imovel(
                        latitude=row['LATITUDE'],
                        longitude=row['LONGITUDE'],
                        sale_price=row['SALE PRICE'],
                        year_sold=row['YEAR_SOLD']
                    )
                    db.session.add(novo_imovel)
                
                db.session.commit()
                print(f"{Imovel.query.count()} imóveis importados para o banco de dados.")
            except Exception as e:
                print("Erro ao importar dados do CSV:", e)

@app.route('/')
def index():
    try:
        min_year = db.session.query(db.func.min(Imovel.year_sold)).scalar()
        max_year = db.session.query(db.func.max(Imovel.year_sold)).scalar()
        
        if min_year is None or max_year is None:
            return "Erro: Banco de dados vazio. Execute init_db() para importar dados."
        
        print(f"Ano mínimo: {min_year}, Ano máximo: {max_year}")
        return render_template('map.html',
                              min_year=min_year,
                              max_year=max_year)
    except Exception as e:
        return f"Erro ao acessar o banco de dados: {str(e)}"
    
@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/data/<int:year>')
def get_data(year):
    try:
        # Consulta os imóveis do ano específico
        imoveis = Imovel.query.filter_by(year_sold=year).all()
        
        if not imoveis:
            return jsonify({"error": "Nenhum dado encontrado para este ano."}), 404
        
        # Prepara os dados para retorno
        data = [imovel.to_dict() for imovel in imoveis]
        min_price = min(imovel.sale_price for imovel in imoveis)
        max_price = max(imovel.sale_price for imovel in imoveis)
        
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
        # Consulta todos os imóveis
        imoveis = Imovel.query.all()
        
        if not imoveis:
            return jsonify({"error": "Nenhum dado encontrado no banco de dados."}), 404
        
        # Prepara os dados para retorno
        data = [imovel.to_dict() for imovel in imoveis]
        min_price = db.session.query(db.func.min(Imovel.sale_price)).scalar()
        max_price = db.session.query(db.func.max(Imovel.sale_price)).scalar()
        
        return jsonify({
            'data': data,
            'min_price': min_price,
            'max_price': max_price
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados antes de executar o app
    app.run(debug=True)