from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# DB connection
client = MongoClient('mongodb://localhost:27017/')
database = client['car_repair_shop']
cars_collection = database['cars']

# Car model
class Car(BaseModel):
    id: str
    make: str
    model: str
    year: int

# GET /cars - Retrieve all cars
@app.get('/cars')
def get_all_cars():
    cars = cars_collection.find()
    return list(cars)

# POST /cars - Create a new car
@app.post('/cars')
def create_car(car: Car):
    car_data = car.model_dump()
    cars_collection.insert_one(car_data)
    return {'message': 'created a car'}

# GET /cars/{id} - Retrieve a specific car
@app.get('/cars/{car_id}')
def get_car(car_id: str):
    car = cars_collection.find_one({'id': car_id})
    if car:
        return car
    raise HTTPException(status_code=404, detail='Car not found')

# PUT /cars/{id} - Update an existing car
@app.put('/cars/{car_id}')
def update_car(car_id: str, updated_car: Car):
    car_data = updated_car.model_dump()
    result = cars_collection.update_one({'id': car_id}, {'$set': car_data})
    if result.modified_count == 1:
        return {'message': 'updated car'}
    raise HTTPException(status_code=404, detail='Car not found')

# DELETE /cars/{id} - Delete a specific car
@app.delete('/cars/{car_id}')
def delete_car(car_id: str):
    result = cars_collection.delete_one({'id': car_id})
    if result.deleted_count == 1:
        return {'message': 'deleted car'}
    raise HTTPException(status_code=404, detail='Car not found')


