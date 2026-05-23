def exige_login(funcao):
    def wrapper(usuario):
        if not usuario.get("logado"):
            return "Acesso negado"

        return funcao(usuario)

    return wrapper

@exige_login
def acessar_painel(usuario):
    return f"Bem-vindo, {usuario['nome']}"

usuario1 = {
    "nome": "Fabio",
    "logado": True
}

usuario2 = {
    "nome": "Ana",
    "logado": False
}

print(acessar_painel(usuario1))
print(acessar_painel(usuario2))
          