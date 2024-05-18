from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para enviar la consulta al backend
@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    response = requests.post('http://127.0.0.1:8000/query', json={"query": question})
    if response.status_code == 200:
        data = response.json()
        answer = data.get('result', {}).get('result', 'Sin respuesta')
        return jsonify({'question': question, 'answer': answer})
    else:
        return jsonify({'question': question, 'answer': 'Error en la respuesta del servidor.'})

if __name__ == '__main__':
    app.run(debug=True)
