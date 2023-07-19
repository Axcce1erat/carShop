from fastapi.testclient import TestClient
from car_api import app
from car_api import Car

client = TestClient(app)  # Create a TestClient instance

def test_get_all_cars():
    response = client.get('/cars')
    assert response.status_code == 200
    assert response.json() == [
        {'id': '1', 'make': 'Honda', 'model': 'Civic', 'year': 2020},
        {'id': '2', 'make': 'Ford', 'model': 'Mustang', 'year': 2022},
        {'id': '3', 'make': 'Toyota', 'model': 'Camry', 'year': 2021}
    ]

def test_get_car():
    car = client.get('/cars/1')
    assert car.status_code == 200
    assert car.json() == {'id': '1', 'make': 'Honda', 'model': 'Civic', 'year': 2020}

def test_create_car():
    new_car = Car(id='4', make='Tesla', model='Model S', year=2023)
    response = client.post('/cars', json=new_car.model_dump())
    assert response.status_code == 200
    assert response.json() == {'message': 'created a car'}
    
def test_update_car():
    updated_car = Car(id='1', make='Honda', model='Accord', year=2022)
    response = client.put('/cars/1')
