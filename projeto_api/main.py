from fastapi import FastAPI
from app.controllers import usuario_controller

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bem-vindo à API de Usuários!"}

@app.get("/usuarios")
def listar():
    return usuario_controller.listar_usuarios()

@app.post("/usuarios")
def criar(nome: str):
    return usuario_controller.criar_usuario(nome)
          
