from ninja import Router, Schema
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

router = Router()

class UserCreateSchema(Schema):
    username: str
    password: str

@router.post("/register")
def register(request, data: UserCreateSchema):
    user = User.objects.create(
        username=data.username,
        password=make_password(data.password)
    )
    return {"id": user.id, "username": user.username}
