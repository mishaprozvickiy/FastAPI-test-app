from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=100)
    age: int = Field(ge=10, le=120)

    model_config = ConfigDict(extra="forbid")


data = {
    "email": "abc@mail.com",
    "bio": "Мне 12 лет, я живу в России",
    "age": 12,
    "test": 123
}

print(UserSchema(**data))
print(repr(UserSchema(**data)))
# test = UserSchema(bio=None, email="123", age=12)
# print(test.email)