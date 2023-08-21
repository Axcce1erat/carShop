import unittest
from fastapi.testclient import TestClient
from main import app, cars_collection, Car

class TestCarAPI(unittest.TestCase):
    def setUp(self):
        # Insert test data into the collection
        self.test_cars = [
            {
                'id': '4',
                'make': 'Tesla',
                'model': 'Model S',
                'year': 2021
            },
            {
                'id': '5',
                'make': 'BMW',
                'model': 'M3',
                'year': 2022
            }
        ]
        cars_collection.insert_many(self.test_cars)
        self.client = TestClient(app)

    def tearDown(self):
        # Remove test data from the collection
        cars_collection.delete_many({'id': {'$in': ['4', '5']}})

    def test_get_all_cars(self):
        response = self.client.get('/cars')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_create_car(self):
        new_car = Car(id='6', make='Audi', model='A4', year=2022)
        response = self.client.post('/cars', json=new_car.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'created a car'})
        # Check if the new car was added to the collection
        car = cars_collection.find_one({'id': '6'})
        self.assertIsNotNone(car)

    def test_get_car(self):
        response = self.client.get('/cars/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['make'], 'Honda')

    def test_update_car(self):
        updated_car = Car(id='1', make='Honda', model='Civic', year=2021)
        response = self.client.put('/cars/1', json=updated_car.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'updated car'})
        # Check if the car was updated in the collection
        car = cars_collection.find_one({'id': '1'})
        self.assertEqual(car['year'], 2021)

    def test_delete_car(self):
        response = self.client.delete('/cars/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'deleted car'})
        # Check if the car was removed from the collection
        car = cars_collection.find_one({'id': '2'})
        self.assertIsNone(car)

if __name__ == '__main__':
    unittest.main()