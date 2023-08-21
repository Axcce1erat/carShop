# carShop
start 
uvicorn main:app --reload

show all cars
http://127.0.0.1:8000/cars

delete car
curl -X DELETE http://127.0.0.1:8000/cars/1

Add car
curl -X POST http://127.0.0.1:8000/cars -H "Content-Type: application/json" -d '{"id": "4", "make": "Tesla", "model": "Model 3", "year": 2023}'

change car
curl -X PUT http://127.0.0.1:8000/cars/1 -H "Content-Type: application/json" -d '{"id": "1", "make": "Honda", "model": "Civic", "year": 2020}'