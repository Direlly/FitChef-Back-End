from flask import Flask, request, jsonify
from models import db, Usuario, Receita

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitchef.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    
    if not nome or not email or not senha:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    
    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return jsonify({"error": "Usuário já cadastrado"}), 400
    
    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({"message": "Usuário cadastrado com sucesso"}), 201


@app.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        return jsonify({"id": usuario.id, "nome": usuario.nome, "email": usuario.email}), 200
    return jsonify({"error": "Usuário não encontrado"}), 404


@app.route('/receitas', methods=['POST'])
def adicionar_receita():
    data = request.get_json()
    nome = data.get('nome')
    ingredientes = data.get('ingredientes')
    modo_preparo = data.get('modo_preparo')
    usuario_id = data.get('usuario_id')
    
    if not nome or not ingredientes or not modo_preparo or not usuario_id:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    nova_receita = Receita(nome=nome, ingredientes=ingredientes, modo_preparo=modo_preparo, usuario_id=usuario_id)
    db.session.add(nova_receita)
    db.session.commit()
    
    return jsonify({"message": "Receita adicionada com sucesso"}), 201


@app.route('/receitas', methods=['GET'])
def buscar_receitas():
    receitas = Receita.query.all()
    resultado = []
    for receita in receitas:
        resultado.append({
            "id": receita.id,
            "nome": receita.nome,
            "ingredientes": receita.ingredientes,
            "modo_preparo": receita.modo_preparo
        })
    return jsonify(resultado), 200


@app.route('/receitas/<int:id>', methods=['GET'])
def buscar_receita(id):
    receita = Receita.query.get(id)
    if receita:
        return jsonify({
            "id": receita.id,
            "nome": receita.nome,
            "ingredientes": receita.ingredientes,
            "modo_preparo": receita.modo_preparo
        }), 200
    return jsonify({"error": "Receita não encontrada"}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)