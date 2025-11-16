

## Что такое Pydantic

Pydantic — это библиотека Python для валидации данных и создания удобных моделей с типами.

## Основные возможности

* Валидация данных по типам
* Автоматическая сериализация/десериализация
* Работа с ORM
* Генерация JSON-схем

---

## Пример простой модели

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int | None = None
```

---

## Валидация данных

```python
user = User(id=1, name="Islam", age=17)
print(user)
```

Если данные не совпадают по типу:

```python
User(id="abc", name="Test")  # Ошибка
```

---

## Работа с вложенными моделями

```python
class Address(BaseModel):
    city: str
    street: str

class User(BaseModel):
    id: int
    name: str
    address: Address
```

---

## Настройки моделей (Config)

```python
class User(BaseModel):
    name: str

    class Config:
        validate_assignment = True
        extra = "ignore"  # игнорировать лишние поля
```

---

## Pydantic v2 отличие

* BaseModel переписан на pydantic-core
* `model_dump()` вместо `dict()`
* `model_validate()` вместо `parse_obj`

Пример:

```python
user = User.model_validate({"name": "Islam"})
print(user.model_dump())
```

---

## Пример для FastAPI

```python
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    title: str
    price: float

@app.post("/items")
def create_item(item: Item):
    return item
```


