from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# DB connection
client = MongoClient('mongodb://localhost:27017/')
database = client['car_repair_shop']
cars_collection = database['cars']

class Car(BaseModel):
    id: str
    make: str
    model: str
    year: int

# Retrieve all cars
@app.get('/cars')
def get_cars():
    cars = cars_collection.find()
    return list(cars)

# Create a new car
@app.post('/cars')
def create_car(car: Car):
    car_data = car.dict()
    cars_collection.insert_one(car_data)
    return {'message': 'Car created successfully'}

# Get a specific car by id
@app.get('/cars/{car_id}')
def get_car(car_id: str):
    car = cars_collection.find_one({'id': car_id})
    if car:
        return car
    raise HTTPException(status_code=404, detail='Car not found')

# Update an existing car by id
@app.put('/cars/{car_id}')
def update_car(car_id: str, updated_car: Car):
    car_data = updated_car.dict()
    result = cars_collection.update_one({'id': car_id}, {'$set': car_data})
    if result.modified_count == 1:
        return {'message': 'Car updated successfully'}
    raise HTTPException(status_code=404, detail='Car not found')

# Delete a specific car by id
@app.delete('/cars/{car_id}')
def delete_car(car_id: str):
    result = cars_collection.delete_one({'id': car_id})
    if result.deleted_count == 1:
        return {'message': 'Car deleted successfully'}
    raise HTTPException(status_code=404, detail='Car not found')


