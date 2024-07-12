from flask import Flask, jsonify, request
from datetime import datetime
from dotenv import load_dotenv
from models import db, genero, autor, libro
import os
load_dotenv() 



app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db = SQLAlchemy(app)

db.init_app(app)

#------------------------------------------- RUTAS --------------------------------------------------------

@app.route('/', methods=['GET'])
def main():
    return jsonify({"message": "hola"}), 200


#--------------------------------------------- genero ----------------------------------------------------


@app.route('/genero', methods=['POST'])
def creategenero():
    data = request.get_json()

    if 'nombre' not in data:
        return jsonify({"error": "Los datos son incorrectos"}), 400
    
    new = genero(nombre=data['nombre'])
    db.session.add(new)
    db.session.commit()
    return jsonify({ "message": "genero creado correctamente"}), 201

#--------------------------------------------- autor ----------------------------------------------------


@app.route('/autor', methods=['POST'])
def createAutor():
    data = request.get_json()

    if 'nombre' not in data or 'nacionalidad' not in data:
        return jsonify({"error": "Los datos son incorrectos"}), 400
    
    new = autor(nombre=data['nombre'], nacionalidad=data['nacionalidad'], fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%d/%m/%y'))
    db.session.add(new)
    db.session.commit()
    return jsonify({ "message": "autor creado correctamente"}), 201

#--------------------------------------------libro-------------------------------------


@app.route('/libro/<int:id>', methods=['GET'])
def get_libro(id):
    data = libro.query.get(id)

    if data is None:
        return jsonify({"message": "El libro no existe"}), 404
    response = {
        'titulo': data.nombre,
        'autor': data.autor2.nombre,
        'genero': data.genero2.nombre
    }
    return jsonify(response), 200

@app.route('/libro/BuscarGenero/<int:id>', methods=['GET'])
def get_libros_genero(id):
    TGenero = genero.query.get(id)

    if TGenero is None:
        return jsonify({"message": "No existen libros con ese genero"}), 404

    libros = libro.query.filter_by(genero=id).all()
    result= []

    for Tlibro in libros:
        result.append({
            'id': Tlibro.libroId,
            'nombre': Tlibro.nombre,
            'autor': Tlibro.autor2.nombre
        })
    response = {
        'libros': result
    }
    return jsonify(response), 200


@app.route('/libro', methods=['POST'])
def createLibro():
    data = request.get_json()

    if 'nombre' not in data or 'ISBN' not in data:
        return jsonify({"message": "Los datos son incorrectos"}), 400
    
    repetido = libro.query.filter_by(ISBN=data['ISBN']).first()

    if repetido:
        return jsonify({"message": "El ISBN ya existe"}), 400
    
    new = libro(ISBN=data['ISBN'],fecha_publicacion=datetime.strptime(data['fecha_publicacion'], '%d/%m/%y'),precio=data['precio'],cantidad=data['cantidad'], nombre=data['nombre'], autor=1,genero=1)
    db.session.add(new)
    db.session.commit()
    return jsonify({ "message": "libro creado correctamente"}), 201

@app.route('/libro/<int:id>', methods=['PUT'])
def updateLibro(id):
    data = request.get_json()
    Ulibro = libro.query.get_or_404(id)
    try:
        Ulibro.nombre = data.get('nombre', Ulibro.nombre)
        Ulibro.precio = data.get('precio', Ulibro.precio)
        Ulibro.genero = data.get('genero', Ulibro.genero)
        Ulibro.autor = data.get('autor', Ulibro.autor)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": "Parametros incorrectos"}), 400

    response = {
        'message': 'Libro actualizado correctamente.',
        'libro': {
            'id': Ulibro.libroId,
            'nombre': Ulibro.nombre,
            'genero': Ulibro.genero2.nombre,
            'autor': Ulibro.autor2.nombre
        }
    }
    return jsonify(response), 200


@app.route('/libro/isbn', methods=['GET'])
def searchLibroISBN():
    ISBN = request.args.get('ISBN')

    if not ISBN:        

        return jsonify({'message': 'Falto el ISBN en la consulta'}), 400
    
    libros = libro.query.filter(libro.ISBN.like(f'%{ISBN}%')).all()

    result= []

    for Blibro in libros:
        result.append({
            'id': Blibro.libroId,
            'ISBN': Blibro.ISBN,
            'nombre': Blibro.nombre,
            'autor': Blibro.autor2.nombre,
            'genero': Blibro.genero2.nombre
        })
    response = {
        'libros': result
    }
    
    return jsonify(response), 200



@app.route('/libro/title', methods=['GET'])
def searchLibroTitle():
    nombre = request.args.get('nombre')

    if not nombre:        

        return jsonify({'message': 'Falto el nombre en la consulta'}), 400
    
    libros = libro.query.filter(libro.nombre.like(f'%{nombre}%')).all()

    result= []

    for Blibro in libros:
        result.append({
            'id': Blibro.libroId,
            'ISBN': Blibro.ISBN,
            'nombre': Blibro.nombre,
            'precio': Blibro.precio,
            'autor': Blibro.autor2.nombre,
            'genero': Blibro.genero2.nombre
        })
    response = {
        'libros': result
    }
    
    return jsonify(response), 200



@app.route('/libro/autor/<int:id>', methods=['GET'])
def searchLibroAuthor(id):
    autor = id

    if not autor:        

        return jsonify({'message': 'Falto el autor en la consulta'}), 400
    
    libros = libro.query.filter(libro.autor.like(f'%{autor}%')).all()

    result= []

    for Blibro in libros:
        result.append({
            'id': Blibro.libroId,
            'ISBN': Blibro.ISBN,
            'nombre': Blibro.nombre,
            'precio': Blibro.precio,
            'autor': Blibro.autor2.nombre,
            'genero': Blibro.genero2.nombre
        })
    response = {
        'libros': result
    }
    
    return jsonify(response), 200




@app.route('/libro/venta/<int:id>', methods=['PUT'])
def venta(id):
    try:
        
        libroid = id
        cantidad= int(request.args.get('cantidad'))

        Libro = libro.query.get(libroid)
        Libro.cantidad = Libro.cantidad - cantidad
        db.session.commit()

    except Exception as e:
        return jsonify({"error": "Parametros incorrectos"}), 400

    response = {
        'message': "Libro vendido correctamente"
    }
    
    return jsonify(response), 200

app.run()