from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, ConfigDict
import uvicorn

app = FastAPI(
    title="Simple FastAPI App",
    description="Первое приложение на FastAPI",
    version="1.0.0"
)

db = {}

# Схема пользователя
class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(default=None, max_length=1000)

    model_config = ConfigDict(extra="forbid")  # запрет лишних полей

# Схема пользователя с возрастом
class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=70)

# Получить всех пользователей
@app.get("/users")
def get_users():
    return db

# Получить пользователя по email
@app.get("/user/{email}")
def read_user(email: str):
    if email in db:
        return db[email]
    raise HTTPException(status_code=404, detail="User not found")

# Создать нового пользователя
@app.post("/user")
def create_user(user: UserAgeSchema):
    if user.email in db:
        raise HTTPException(status_code=400, detail="User already exists")
    db[user.email] = user.dict()
    return db

# Удалить пользователя по email
@app.delete("/user/{email}")
def delete_user(email: str):
    if email in db:
        del db[email]
        return {"detail": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
