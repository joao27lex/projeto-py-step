def gerar_numeros(limite):
    numero = 1

    while numero <= limite:
        yield numero
        numero += 1

for n in gerar_numeros(5):
    print(n)
          