estoque = {
    "notebook": 10,
    "mouse": 25,
    "teclado": 15
}

produto = "mouse"

if estoque.get(produto, 0) > 0:
    print("Produto disponível")
else:
    print("Produto indisponível")
          