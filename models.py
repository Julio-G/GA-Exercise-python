from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
db = SQLAlchemy()


class autor(db.Model):
    autorId = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    nacionalidad = db.Column(db.String(100), nullable = False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<autor {self.nombre}>'
    
class genero(db.Model):
    generoId = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f'<genero {self.nombre}>'
    
class libro(db.Model):
    libroId = db.Column(db.Integer, primary_key = True)
    ISBN = db.Column(db.String(100), nullable = False)
    nombre = db.Column(db.String(100), nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    fecha_publicacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    precio = db.Column(db.Numeric(9,2), nullable = False)
    autor = db.Column(db.Integer, db.ForeignKey('autor.autorId'), nullable=False)
    genero = db.Column(db.Integer, db.ForeignKey('genero.generoId'), nullable=False)

    genero2 = db.relationship('genero', backref=db.backref('libro', lazy=True))
    autor2 = db.relationship('autor', backref=db.backref('libro', lazy=True))

    def __repr__(self):
        return f'<libro {self.nombre}>'
    
class cliente(db.Model):
    clienteId = db.Column(db.Integer, primary_key = True)
    nit = db.Column(db.String(100), nullable = False)
    nombre = db.Column(db.String(100), nullable = False)
    correo = db.Column(db.String(100), nullable = False)
    telefono = db.Column(db.String(100), nullable = False)
    direccion = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f'<libro {self.nombre}>'