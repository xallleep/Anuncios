import os
from flask import Flask, request, render_template, redirect, url_for, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import stripe
from dotenv import load_dotenv
import openai
from datetime import datetime, timedelta
import logging

# Configuração inicial
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Extensões
db = SQLAlchemy(app)

# Correção principal: Inicialização do Limiter
limiter = Limiter(
    app=app,  # Aplicação Flask
    key_func=get_remote_address,  # Função para identificar clientes
    default_limits=["200 per day", "50 per hour"]  # Limites padrão
)

stripe.api_key = os.getenv('STRIPE_KEY')

# Configuração OpenAI - Atualizada para a nova API
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

# [Restante dos modelos e helpers permanecem iguais...]

# Rotas Principais
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
@limiter.limit("10/hour")  # Limite específico para esta rota
def gerar_anuncio():
    texto = request.form.get('texto', '').strip()
    if not texto:
        flash('Por favor, insira um texto para gerar o anúncio', 'error')
        return redirect(url_for('home'))
    
    user_id = session.get('user_id')
    if not check_limits(user_id):
        flash('Limite diário atingido! Assine Premium para continuar.', 'warning')
        return redirect(url_for('premium'))
    
    anuncio = generate_ad(texto)
    
    if user_id:
        user = User.query.get(user_id)
        user.api_calls += 1
        db.session.commit()
    
    return render_template('resultado.html', 
                         anuncio=anuncio, 
                         is_premium=is_premium(user_id))

# [Restante das rotas permanece igual...]

# Inicialização
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))