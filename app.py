from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Configuração da API da OpenAI (gratuita via Trelis)
openai.api_base = "https://api.trelis.com/v1"
openai.api_key = os.getenv("OPENAI_API_KEY")  # Configure no Render

def gerar_anuncio_ia(texto):
    prompt = f"""
    Crie um post para Instagram profissional sobre: {texto}
    - Use emojis relevantes
    - Inclua 3 hashtags estratégicas
    - Linguagem persuasiva
    - Máximo de 3 linhas
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    texto = request.form['texto']
    anuncio = gerar_anuncio_ia(texto)
    return render_template('resultado.html', anuncio=anuncio)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)