lista = [numero for numero in range(1000000)]
gerador = (numero for numero in range(1000000))

print(type(lista))
print(type(gerador))