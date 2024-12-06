from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"<Usuario {self.nome}>"

class Receita(db.Model):
    __tablename__ = 'receitas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
    modo_preparo = db.Column(db.Text, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    usuario = db.relationship('Usuario', backref=db.backref('receitas', lazy=True))

    def __repr__(self):
        return f"<Receita {self.nome}>"