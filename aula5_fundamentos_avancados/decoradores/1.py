def meu_decorador(funcao):
    def wrapper():
        print("Antes da função")
        funcao()
        print("Depois da função")

    return wrapper

@meu_decorador
def saudacao():
    print("Olá!")

saudacao()
          