#criar uma api com crud para listar, cadastrar e procurar usuário por ip

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

favicon_path="favicon.ico"

app=FastAPI()

class User(BaseModel):
    ip: int

database:List[User]=[]

@app.get("/")
def read_root():
    return{"message": "Boas vindas!"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.post("/users/", response_model=User, status_code=201)
def create_user(user: User):
    for existing_user in database:
        if existing_user.ip == user.ip:
            raise HTTPException(status_code=400, detail="IP já existe.")
    database.append(user)
    return user

@app.get("/users/", response_model=List[User])
def get_users():
    return database

@app.get("/users/{user_ip}", response_model=User)
def get_user(user_ip: int):
    for user in database:
        if user.ip == user_ip:
            return user
    raise HTTPException(status_code=404, detail="IP não encontrado.")

@app.delete("/users/{user_ip}", response_model=dict)
def delete_user(user_ip: int):
    for index, user in enumerate(database):
        if user.ip == user_ip:
            del database[index]
            return{"message": "IP deletado."}
    raise HTTPException(status_code=404, detail="IP não encontrado.")
