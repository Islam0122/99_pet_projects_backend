import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Simple FastAPI App",
    description="Первое приложение на FastAPI",
    version="1.0.0"
)

# ====================================
# 🔖 МОДЕЛИ
# ====================================

class Book(BaseModel):
    title: str
    author: str

class Car(BaseModel):
    title: str
    year: int
    price: int


# ====================================
# 📚 BOOK ROUTES
# ====================================

books = [
    {"id": 1, "title": "<UNK>", "author": "<UNK>"},
    {"id": 2, "title": "<books1>", "author": "Islam"},
]

@app.get("/books", tags=["Books"])
async def read_books():
    return books

@app.get("/books/{id}", tags=["Books"])
async def read_book(id: int):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", tags=["Books"])
async def create_book(new_book: Book):
    book_data = {
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author
    }
    books.append(book_data)
    return {"success": True, "message": "Book created successfully", "book": book_data}


# ====================================
# 🚗 CAR ROUTES
# ====================================

cars = [
    {"id": 1, "title": "Mercedes", "year": 2020, "price": 50000}
]

@app.get("/cars", tags=["Cars"])
async def read_cars():
    return cars

@app.get("/cars/{id}", tags=["Cars"])
async def read_car(id: int):
    for car in cars:
        if car["id"] == id:
            return car
    raise HTTPException(status_code=404, detail="Car not found")

@app.post("/cars", tags=["Cars"])
async def create_car(new_car: Car):
    car_data = {
        "id": len(cars) + 1,
        "title": new_car.title,
        "year": new_car.year,
        "price": new_car.price
    }
    cars.append(car_data)
    return {"success": True, "message": "Car created successfully", "car": car_data}

@app.put("/cars/{id}", tags=["Cars"])
async def update_car(id: int, new_car: Car):
    for car in cars:
        if car["id"] == id:
            car["title"] = new_car.title
            car["year"] = new_car.year
            car["price"] = new_car.price
            return {"success": True, "message": "Car updated successfully", "car": car}
    raise HTTPException(status_code=404, detail="Car not found")

@app.delete("/cars/{id}", tags=["Cars"])
async def delete_car(id: int):
    for index, car in enumerate(cars):
        if car["id"] == id:
            deleted_car = cars.pop(index)
            return {"success": True, "message": "Car deleted successfully", "car": deleted_car}
    raise HTTPException(status_code=404, detail="Car not found")

@app.patch("/cars/{id}", tags=["Cars"])
async def partial_update_car(id: int, new_car: Car):
    for car in cars:
        if car["id"] == id:
            # Обновим только те поля, которые переданы (упрощённо, без Optional)
            car["title"] = new_car.title or car["title"]
            car["year"] = new_car.year or car["year"]
            car["price"] = new_car.price or car["price"]
            return {"success": True, "message": "Car partially updated", "car": car}
    raise HTTPException(status_code=404, detail="Car not found")


# ====================================
# 🚀 Запуск приложения
# ====================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )