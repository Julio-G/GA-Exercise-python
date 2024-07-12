import pytest, json
from main import app

@pytest.fixture(scope='module')
def client():

    with app.test_client() as client:
        yield client


#------------------------------------------- test GET ------------------------------------------

def test_prueba(client):
    response = client.get('/')
    assert response.status_code == 200
