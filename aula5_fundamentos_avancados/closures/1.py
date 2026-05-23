def criar_multiplicador(fator):
    def multiplicar(numero):
        return numero * fator

    return multiplicar

dobrar = criar_multiplicador(2)
triplicar = criar_multiplicador(3)

print(dobrar(10))
print(triplicar(10))
          