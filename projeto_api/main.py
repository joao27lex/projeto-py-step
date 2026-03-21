
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

    return {"msg": f"Usuário {nome} de idade {idade} criado"}
          
@app.delete("/usuarios")
def deletar_usuario(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM usuarios WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return {"msg": f"Usuário {id} deletado"}

@app.put("/usuarios")
def atualizar_usuario(id: int, nome: str, idade: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE usuarios SET nome = ?, idade = ? WHERE id = ?",
        (nome, idade, id)
    )
    conn.commit()
    conn.close()

    return {
        "id" : id,
        "nome" : nome,
        "idade" : idade
    }

@app.get("/usuarios/{id}")
def pegar_usuario(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (id, )
    )
    dados = cursor.fetchone()

    conn.close()

    return dados
