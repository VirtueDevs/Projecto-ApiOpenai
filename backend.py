import os
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Date, MetaData, DECIMAL
from sqlalchemy.orm import sessionmaker
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] =  api_key 

# Ruta a la base de datos
rutadb = 'db_clientes.db'  # Reemplaza con la ruta a tu base de datos
db = SQLDatabase.from_uri(f"sqlite:///{rutadb}")

# Crear el LLM
llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

# Crear la cadena utilizando el método recomendado from_llm
cadena = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=False)

# Formato personalizado de respuesta
formato = """
Dada una pregunta del usuario:
1. Crea una consulta de SQLite.
2. Revisa los resultados.
3. Devuelve el dato.
4. Si tienes que hacer alguna aclaración o devolver cualquier texto que sea siempre en español.
#{question}
"""

# Función para hacer la consulta
def consulta(input_usuario):
    consulta_formateada = formato.format(question=input_usuario)
    resultado = cadena({"query": consulta_formateada})
    return resultado

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    question = data.get('query')
    result = consulta(question)
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
