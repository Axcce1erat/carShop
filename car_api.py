from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# DB connection
client = MongoClient('mongodb://localhost:27017/')
database = client['car_repair_shop']
cars_collection = database['cars']

# Example data
example_cars = [
    
    {
        'id': '1',
        'make': 'Honda',
        'model': 'Civic',
        'year': 2020
    },
    {
        'id': '2',
        'make': 'Ford',
        'model': 'Mustang',
        'year': 2022
    },
    {
        'id': '3',
        'make': 'Toyota',
        'model': 'Camry',
        'year': 2021
    }
]

# Insert the example cars into the collection
cars_collection.insert_many(example_cars)

# Test if all cars from the collection are in
cursor = cars_collection.find()
for car in cursor:
    print(car)

class Car(BaseModel):
    id: str
    make: str
    model: str
    year: int

# Retrieve cars
@app.get('/cars')
def get_all_cars():
    cars = cars_collection.find()
    return list(cars)

#  Create a new car
@app.post('/cars')
def create_car(car: Car):
    car_data = car.model_dump()
    cars_collection.insert_one(car_data)
    return {'message': 'created a car'}

# Retrieve a car by id
@app.get('/cars/{car_id}')
def get_car(car_id: str):
    car = cars_collection.find_one({'id': car_id})
    if car:
        return car
    raise HTTPException(status_code=404, detail='Car not found')

# Update an existing car by id
@app.put('/cars/{car_id}')
def update_car(car_id: str, updated_car: Car):
    car_data = updated_car.model_dump()
    result = cars_collection.update_one({'id': car_id}, {'$set': car_data})
    if result.modified_count == 1:
        return {'message': 'updated car'}
    raise HTTPException(status_code=404, detail='Car not found')

# Delete a specific car by id
@app.delete('/cars/{car_id}')
def delete_car(car_id: str):
    result = cars_collection.delete_one({'id': car_id})
    if result.deleted_count == 1:
        return {'message': 'deleted car'}
    raise HTTPException(status_code=404, detail='Car not found')


