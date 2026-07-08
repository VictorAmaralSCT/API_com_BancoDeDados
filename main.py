from flask import Flask, jsonify, request
import os
from models import db, Tarefas
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///tarefas.db"
)
#'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

""""
Criar a classe Alunos no models.py. Depois: 

1) Criar rotas GET para alunos
2) Criar rotas GET para alunos específico (por ID)
3) Criar rota POST para alunos
4) Criar rota PUT para alunos
5) Criar rota PATCH para alunos
6) Criar rota DELETE para alunos
"""


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


@app.route('/tarefas', methods=['POST'])
def criar_tarefas():
    data = request.get_json()

    if not data:
        return jsonify({
            "erro":"Nenhum dados foi enviado"
        }), 400

    campos_obrigatorios = ["titulo", "descricao"]

    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({
                "erro":f"O campo {campo} é obrigatorio"
            })

    nova_tarefa = Tarefas(
        titulo=data["titulo"],
        descricao=data["descricao"],
        concluida=data.get("concluida", False)
    )

    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify(nova_tarefa.to_dict()), 200


@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    # Criar a consulta:
    consulta = db.select(Tarefas).order_by(Tarefas.id)

    #Executar a consulta e salvar na variável 'resultado':
    resultado = db.session.execute(consulta)

    #Salvar os resultados na variável tarefas
    tarefas = resultado.scalars().all()

    #tarefas = Tarefas.query.order_by(Tarefas.id).all()

    lista_tarefas = []

    for tarefa in tarefas:
        lista_tarefas.append(tarefa.to_dict())

    return jsonify(lista_tarefas), 200


@app.route('/tarefas/<int:id_tarefas>', methods=['GET'])
def buscar_tarefas_id(id_tarefas):
    tarefa = db.session.get(Tarefas, id_tarefas)

    if tarefa is None:
        return jsonify({"erro":"Tarefa não encontrada"}), 404

    return jsonify(tarefa.to_dict()), 200


@app.route('/tarefas/<int:id_tarefa>', methods=['PUT'])
def atualizar_tarefa(id_tarefa):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi enviado"}), 400

    campos_obrigatorios = ["titulo", "descricao", "concluida"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo {campo} é obrigatorio"}), 400

    try:
        tarefa = db.session.get(Tarefas, id_tarefa)

        if tarefa is None:
            return jsonify({"erro": "Tarefa não encontrada"}), 404

        tarefa.titulo = dados["titulo"]
        tarefa.descricao = dados["descricao"]
        tarefa.concluida = dados["concluida"]

        db.session.commit()

        return jsonify(tarefa.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


@app.route('/tarefas/<int:id_tarefa>', methods=['PATCH'])
def alterar_tarefa(id_tarefa):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi enviado"}), 400

    tarefa = db.session.get(Tarefas, id_tarefa)

    if tarefa is None:
        return jsonify({"erro":"Tarefa não encontrada"}), 404

    if "titulo" in dados:
        tarefa.titulo = dados["titulo"]
    if "descricao" in dados:
        tarefa.descricao = dados["descricao"]
    if "concluida" in dados:
        tarefa.concluida = dados["concluida"]

    db.session.commit()
    return jsonify(tarefa.to_dict()), 200


@app.route('/tarefas/<int:id_tarefa>', methods=['DELETE'])
def deletar_tarefa(id_tarefa):
    tarefa = db.session.get(Tarefas, id_tarefa)
    if tarefa is None:
        return jsonify({"erro":"Tarefa não encontrada"}), 404

    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({"mensagem":"Tarefa deletada com sucesso"}), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)