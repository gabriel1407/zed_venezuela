from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from db.db import engine, get_db, Base
from models.saludo import Saludo
import os

app = Flask(__name__)

# Inicializar la base de datos
Base.metadata.create_all(bind=engine)

# Configurar la base de datos en Flask
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.errorhandler(400)
def bad_request(error):
    response = jsonify({'error': 'Bad Request', 'message': error.description})
    response.status_code = 400
    return response

@app.errorhandler(404)
def not_found(error):
    response = jsonify({'error': 'Not Found', 'message': error.description})
    response.status_code = 404
    return response

@app.errorhandler(500)
def internal_error(error):
    response = jsonify({'error': 'Internal Server Error', 'message': str(error)})
    response.status_code = 500
    return response

@app.route('/saludos/', methods=['GET'])
def get_saludos():
    session = next(get_db())
    saludos = session.query(Saludo).all()
    return jsonify([{'id': saludo.id, 'mensaje': saludo.mensaje} for saludo in saludos])

@app.route('/saludos/', methods=['POST'])
def create_saludo():
    session = next(get_db())
    data = request.get_json()
    if 'mensaje' not in data:
        abort(400, description="Falta el campo 'mensaje'")
    nuevo_saludo = Saludo(mensaje=data['mensaje'])
    session.add(nuevo_saludo)
    session.commit()
    return jsonify({'id': nuevo_saludo.id, 'mensaje': nuevo_saludo.mensaje}), 201

@app.route('/saludos/<int:id>', methods=['GET'])
def get_saludo(id):
    session = next(get_db())
    saludo = session.query(Saludo).filter(Saludo.id == id).first()
    if saludo is None:
        abort(404, description="Saludo no encontrado")
    return jsonify({'id': saludo.id, 'mensaje': saludo.mensaje})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
