def calcular_total(preco, quantidade):
    total = preco * quantidade
    mensagem = "Compra calculada com sucesso"
    return total, mensagem

valor, texto = calcular_total(50, 3)

print(valor)
print(texto)
          