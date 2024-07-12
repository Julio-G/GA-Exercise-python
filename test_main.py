import pytest, json
from main import app

@pytest.fixture(scope='module')
def client():
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:1234@localhost/dbbiblio"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with app.test_client() as client:
        yield client


#------------------------------------------- test GET ------------------------------------------

def test_prueba(client):
    response = client.get('/')
    assert response.status_code == 200


def test_get_libroId(client):
    response = client.get('/libro/1')
    json_data = response.get_json()
    assert response.status_code == 200
    assert len(json_data)>0

def test_get_buscarISBN(client):
    response = client.get('/libro/isbn?ISBN=9876554321')
    json_data = response.get_json()
    assert response.status_code == 200
    assert len(json_data)>0

def test_get_buscarGenero(client):
    response = client.get('/libro/BuscarGenero/10')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['message'] == 'No existen libros con ese genero'


#------------------------------------------- test POST ------------------------------------------

def test_post_libro(client):
    libro_data = {
        "ISBN": "9876588888",
        "nombre": "nuevo libro 2",
        "cantidad": 5,
        "precio": 45.4,
        "fecha_publicacion":"13/10/90",
        "genero": 2,
        "autor": 1
    }
    response = client.post('/libro', data=json.dumps(libro_data), content_type='application/json')
    
    assert response.status_code == 201

def test_post_genero(client):
    genero_data = {
        "nombre": "accion"
    }
    response = client.post('/genero', data=json.dumps(genero_data), content_type='application/json')
    
    assert response.status_code == 201

def test_post_autor(client):
    autor_data = {
        "nombre": "autor 4",
        "nacionalidad": 5,
        "fecha_nacimiento":"13/10/80"
    }
    response = client.post('/autor', data=json.dumps(autor_data), content_type='application/json')
    
    assert response.status_code == 201

#------------------------------------------- test PUT ------------------------------------------

def test_put_libro(client):
    libro_data = {
        "nombre": "update 2",
        "precio": 60,
        "genero": 1,
        "autor": 1
    }
    response = client.put('/libro/2', data=json.dumps(libro_data), content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Libro actualizado correctamente.'