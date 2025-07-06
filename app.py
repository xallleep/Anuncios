import os
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
import stripe
from dotenv import load_dotenv
import openai
from datetime import datetime, timedelta

# Configuração
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Extensões
db = SQLAlchemy(app)
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200/day"])
stripe.api_key = os.getenv('STRIPE_KEY')

# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    premium = db.Column(db.Boolean, default=False)
    premium_expires = db.Column(db.DateTime)

# Rotas Principais
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
@limiter.limit("10/hour")
def gerar_anuncio():
    texto = request.form.get('texto', '')
    if not texto:
        flash('Digite um texto para gerar o anúncio', 'error')
        return redirect(url_for('home'))
    
    # Lógica de geração com OpenAI (simplificada)
    anuncio = f"🌟 {texto[:100]}... #Promoção"
    
    return render_template('resultado.html', anuncio=anuncio)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)