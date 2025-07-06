from flask import Flask, request, render_template, flash, redirect, url_for
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'supersecretkey'

# Configuração da API
openai.api_key = os.getenv("OPENAI_API_KEY")
API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")  # Padrão para API oficial
openai.api_base = API_BASE

# Respostas padrão para falhas na API
RESPOSTAS_PADRAO = [
    "✨ [Seu produto] é a escolha perfeita! Experimente hoje mesmo! #Oferta #Qualidade #Satisfação",
    "🔥 Destaque-se com [seu produto]! Entrega rápida e qualidade garantida. #Exclusivo #Promoção #Destaque",
    "🌟 [Seu produto] transformando experiências! Adquira já e comprove. #Inovação #Qualidade #Recomendo"
]

def gerar_anuncio_ia(texto):
    try:
        prompt = f"""
        Crie um post para Instagram profissional sobre: {texto}
        - Use emojis relevantes
        - Inclua 3-5 hashtags estratégicas
        - Linguagem persuasiva e criativa
        - Máximo de 150 caracteres
        - Formato: Texto principal + hashtags
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message['content'].strip()
    
    except Exception as e:
        print(f"Erro na API: {str(e)}")
        # Fallback inteligente - usa respostas padrão personalizadas
        produto = texto[:30] + "..." if len(texto) > 30 else texto
        resposta = RESPOSTAS_PADRAO[hash(texto) % len(RESPOSTAS_PADRAO)]
        return resposta.replace("[seu produto]", produto)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    texto = request.form.get('texto', '').strip()
    if not texto:
        flash('Por favor, digite algo para gerar o anúncio!', 'error')
        return redirect(url_for('home'))
    
    anuncio = gerar_anuncio_ia(texto)
    return render_template('resultado.html', anuncio=anuncio, texto_original=texto)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))