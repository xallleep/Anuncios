from flask import Flask, request, render_template, flash, redirect, url_for
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'supersecretkey'

# Configuração da API da OpenAI (gratuita via Trelis)
openai.api_base = "https://api.trelis.com/v1"
openai.api_key = os.getenv("OPENAI_API_KEY")

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
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Erro na geração: {str(e)}")
        return None

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
    if not anuncio:
        flash('Erro ao gerar o anúncio. Tente novamente!', 'error')
        return redirect(url_for('home'))
    
    return render_template('resultado.html', anuncio=anuncio, texto_original=texto)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)