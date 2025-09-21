from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel, Field

app = FastAPI()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"  # держать в безопасности
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)


class UserLoginSchema(BaseModel):
    username: str = Field(max_length=20)
    password: str = Field(max_length=20)


@app.post("/login")
def login(credentials: UserLoginSchema, response: Response):
    if credentials.username == "admin" and credentials.password == "123":
        token = security.create_access_token(uid="12345")  # не передавать секретные данные, так как токен чувствителен
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}

    raise HTTPException(status_code=401, detail="incorrect username or password")

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "top_secret"}