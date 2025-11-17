from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# --- CONFIG ---
config = AuthXConfig(
    JWT_SECRET_KEY="SECRET_KEY",
    JWT_TOKEN_LOCATION=["cookies"],    # токен хранится в cookie
    JWT_ACCESS_COOKIE_NAME="my_access_token",
    JWT_COOKIE_SECURE=False,           # True — если HTTPS
    JWT_COOKIE_SAMESITE="lax",
)
security = AuthX(config=config)

# --- SCHEMA ---
class UserLoginSchema(BaseModel):
    email: str
    password: str


# --- ROUTES ---
@app.post("/login")
def login(creds: UserLoginSchema, response: Response):
    # простой тестовый логин
    if creds.email == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345678")

        # установка куки
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            samesite="lax",
            secure=False,  # для localhost, HTTPS => True
        )

        return {"message": "Logged in!"}

    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    """
    Работает только если в запросе есть cookie "my_access_token"
    """
    return {"message": "Hello World"}


# --- START ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
