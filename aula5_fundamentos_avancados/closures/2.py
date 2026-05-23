def criar_validador(tamanho_minimo):
    def validar(texto):
        return len(texto) >= tamanho_minimo

    return validar

validar_senha = criar_validador(8)

print(validar_senha("abc"))
print(validar_senha("abc12345"))
          