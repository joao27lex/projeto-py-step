import requests
import bcrypt
from app.database.supabase_client import SUPABASE_URL, SUPABASE_KEY
import jwt
from datetime import datetime, timedelta
import os
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
EXPIRATION_MINUTES = int(os.getenv("EXPIRATION_MINUTES", 60))

ALGORITHM = "HS256"

def get_headers(extra_headers=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    if extra_headers:
        headers.update(extra_headers)

    return headers


def listar_usuarios():
    url = f"{SUPABASE_URL}/usuarios?select=*"

    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        raise Exception(f"Erro ao listar usuários: {response.text}")

    return response.json()


def buscar_usuario_por_email(email):
    url = f"{SUPABASE_URL}/usuarios?email=eq.{email}&select=*"

    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        raise Exception(f"Erro ao buscar usuário: {response.text}")

    usuarios = response.json()

    return usuarios[0] if usuarios else None


def cadastrar_usuario(email, senha):
    if buscar_usuario_por_email(email):
        raise Exception("Já existe um usuário cadastrado com este email.")

    senha_hash = bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    url = f"{SUPABASE_URL}/usuarios"

    data = {
        "email": email,
        "senha": senha_hash
    }

    response = requests.post(
        url,
        json=data,
        headers=get_headers({"Prefer": "return=representation"})
    )

    if response.status_code not in [200, 201]:
        raise Exception(f"Erro ao cadastrar usuário: {response.text}")

    usuario_criado = response.json()[0]

    return {
        "mensagem": "Usuário cadastrado com sucesso.",
        "usuario": {
            "id": usuario_criado.get("id"),
            "email": usuario_criado.get("email")
        }
    }

def gerar_token(usuario_id, email):
    payload = {
        "sub": usuario_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def login_usuario(email, senha):
    usuario = buscar_usuario_por_email(email)

    if not usuario:
        raise Exception("Email ou senha inválidos.")

    senha_hash = usuario.get("senha")

    if not bcrypt.checkpw(
        senha.encode("utf-8"),
        senha_hash.encode("utf-8")
    ):
        raise Exception("Email ou senha inválidos.")

    token = gerar_token(usuario.get("id"), usuario.get("email"))

    return {
        "mensagem": "Login realizado com sucesso.",
        "token": token,
        "usuario": {
            "id": usuario.get("id"),
            "email": usuario.get("email")
        }
    }
