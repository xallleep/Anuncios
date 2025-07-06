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
limiter = Limiter(app, key_func=get_remote_address)
stripe.api_key = os.getenv('STRIPE_KEY')

# Configuração OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

# Modelos de Banco de Dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    premium = db.Column(db.Boolean, default=False)
    premium_expires = db.Column(db.DateTime)
    api_calls = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))
    stripe_id = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Helpers
def is_premium(user_id):
    user = User.query.get(user_id)
    return user and user.premium and user.premium_expires > datetime.utcnow()

def check_limits(user_id):
    if not user_id:
        return False
    user = User.query.get(user_id)
    return is_premium(user_id) or (user and user.api_calls < 5)

def generate_ad(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "Você é um especialista em marketing digital. Crie posts criativos para Instagram com emojis e hashtags."
            }, {
                "role": "user",
                "content": f"Crie um anúncio sobre: {text}. Limite de 150 caracteres."
            }],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Erro na API: {str(e)}")
        return f"🌟 {text[:50]}... #Marketing #Promoção #Oferta"

# Rotas Principais
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
@limiter.limit("10/hour")
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

# Sistema de Pagamento
@app.route('/premium', methods=['GET', 'POST'])
def premium():
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': os.getenv('STRIPE_PRICE_ID'),
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('premium', _external=True),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            logging.error(f"Erro no pagamento: {str(e)}")
            flash('Erro ao processar pagamento. Tente novamente.', 'error')
    return render_template('premium.html')

@app.route('/success')
def success():
    session_id = request.args.get('session_id')
    if session_id:
        try:
            stripe_session = stripe.checkout.Session.retrieve(session_id)
            user = User.query.filter_by(email=stripe_session.customer_email).first()
            if user:
                user.premium = True
                user.premium_expires = datetime.utcnow() + timedelta(days=30)
                db.session.commit()
                session['user_id'] = user.id
        except Exception as e:
            logging.error(f"Erro ao verificar sessão: {str(e)}")
    return render_template('success.html')

# Painel Admin
@app.route('/admin')
def admin():
    if not session.get('admin'):
        abort(403)
    stats = {
        'users': User.query.count(),
        'premium_users': User.query.filter_by(premium=True).count(),
        'revenue': db.session.query(db.func.sum(Transaction.amount)).scalar() or 0
    }
    return render_template('admin.html', stats=stats)

# Inicialização
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))