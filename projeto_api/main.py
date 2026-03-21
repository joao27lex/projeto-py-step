
from fastapi import FastAPI
import sqlite3

# IMPORTANTE: executa a criação do banco/tabela
import app.database.db

app = FastAPI()

def get_connection():
    return sqlite3.connect("database.db")

@app.get("/")
def home():
    return {"msg": "API rodando"}

@app.get("/usuarios")
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    dados = cursor.fetchall()

    conn.close()
    return dados

@app.post("/usuarios")
def criar_usuario(nome: str, idade: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usuarios (nome, idade) VALUES (?, ?)",
        (nome, idade)
    )

    conn.commit()
    conn.close()

    return {"msg": "Usuário criado"}
          