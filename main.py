from flask import Flask, jsonify, request
from models import db, Tarefas

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'mensagem': 'API com Banco de Dados funcionando!'
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok'
    }), 200



if __name__ == '__main__':
    app.run(debug=True)