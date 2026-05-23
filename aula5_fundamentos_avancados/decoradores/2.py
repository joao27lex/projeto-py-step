def logar_execucao(funcao):
    def wrapper(*args, **kwargs):
        print(f"Executando a função {funcao.__name__}")
        resultado = funcao(*args, **kwargs)
        print("Execução finalizada")
        return resultado

    return wrapper

@logar_execucao
def somar(a, b):
    return a + b

resultado = somar(10, 5)
print(resultado)
          