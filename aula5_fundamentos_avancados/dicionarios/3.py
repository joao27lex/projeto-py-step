produto = {
    "nome": "Notebook",
    "preco": 3500,
    "estoque": 10
}

print(produto.get("nome"))
print(produto.get("categoria", "Sem categoria"))

produto.update({"preco": 3200, "categoria": "Informática"})

for chave, valor in produto.items():
    print(chave, valor)

estoque_removido = produto.pop("estoque")
print(estoque_removido)
print(produto)
          