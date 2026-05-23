usuarios = [
    {"nome": "Ana", "idade": 25},
    {"nome": "Carlos", "idade": 20},
    {"nome": "Marina", "idade": 30}
]

usuarios_ordenados = sorted(usuarios, key=lambda usuario: usuario["idade"])

print(usuarios_ordenados)
          