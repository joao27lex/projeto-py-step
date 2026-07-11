
from datetime import datetime, timedelta

# ============================================================
# CLASSE BASE E SUBCLASSES
# ============================================================
class ItemBiblioteca:
    """Classe base para todos os itens do acervo"""
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self._emprestado = False

    @property
    def emprestado(self):
        return self._emprestado

    def emprestar(self):
        if self._emprestado:
            return False
        self._emprestado = True
        return True

    def devolver(self):
        self._emprestado = False

    def calcular_multa(self, dias_atraso):
        raise NotImplementedError("Subclasses devem implementar")

    def __str__(self):
        status = "📕 Emprestado" if self._emprestado else "📗 Disponível"
        return f"{status} | '{self.titulo}' por {self.autor} ({self.ano})"

    def __eq__(self, outro):
        if isinstance(outro, ItemBiblioteca):
            return self.titulo == outro.titulo and self.autor == outro.autor
        return False


class Livro(ItemBiblioteca):
    def __init__(self, titulo, autor, ano, paginas, isbn):
        super().__init__(titulo, autor, ano)
        self.paginas = paginas
        self.isbn = isbn

    def calcular_multa(self, dias_atraso):
        return dias_atraso * 2.00

    def __str__(self):
        base = super().__str__()
        return f"{base} | {self.paginas} págs | ISBN: {self.isbn}"


class Revista(ItemBiblioteca):
    def __init__(self, titulo, autor, ano, edicao):
        super().__init__(titulo, autor, ano)
        self.edicao = edicao

    def calcular_multa(self, dias_atraso):
        return dias_atraso * 1.00

    def __str__(self):
        base = super().__str__()
        return f"{base} | Edição {self.edicao}"


class DVD(ItemBiblioteca):
    def __init__(self, titulo, autor, ano, duracao_min):
        super().__init__(titulo, autor, ano)
        self.duracao_min = duracao_min

    def calcular_multa(self, dias_atraso):
        return dias_atraso * 5.00

    def __str__(self):
        base = super().__str__()
        return f"{base} | {self.duracao_min} min"


# ============================================================
# USUÁRIO
# ============================================================
class Usuario:
    def __init__(self, nome, email, matricula):
        self.nome = nome
        self._email = None
        self.email = email
        self.matricula = matricula
        self.emprestimos = []   # lista de (ItemBiblioteca, data_emprestimo)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if '@' not in valor:
            raise ValueError("Email inválido")
        self._email = valor.lower()

    @property
    def itens_emprestados(self):
        return len(self.emprestimos)

    def __str__(self):
        return f"👤 {self.nome} ({self.matricula}) — {self.itens_emprestados} itens"

    def __eq__(self, outro):
        if isinstance(outro, Usuario):
            return self.matricula == outro.matricula
        return False


# ============================================================
# BIBLIOTECA (GERENCIADOR PRINCIPAL)
# ============================================================
class Biblioteca:
    def __init__(self, nome):
        self.nome = nome
        self._acervo = []       # lista de ItemBiblioteca
        self._usuarios = []     # lista de Usuario
        self._emprestimos = []  # lista de (usuario, item, data)

    # --- Métodos de acervo ---
    def adicionar_item(self, item):
        self._acervo.append(item)
        print(f"✅ Adicionado: {item.titulo}")

    def buscar_por_titulo(self, termo):
        resultados = [item for item in self._acervo
                      if termo.lower() in item.titulo.lower()]
        return resultados

    def listar_disponiveis(self):
        return [item for item in self._acervo if not item.emprestado]

    def listar_todos(self):
        return self._acervo

    # --- Métodos de usuário ---
    def cadastrar_usuario(self, usuario):
        if usuario in self._usuarios:
            print(f"❌ Usuário {usuario.matricula} já cadastrado.")
            return False
        self._usuarios.append(usuario)
        print(f"✅ Usuário cadastrado: {usuario.nome}")
        return True

    def buscar_usuario(self, matricula):
        for usuario in self._usuarios:
            if usuario.matricula == matricula:
                return usuario
        return None

    # --- Métodos de empréstimo ---
    def emprestar(self, matricula, titulo):
        usuario = self.buscar_usuario(matricula)
        if not usuario:
            print(f"❌ Usuário {matricula} não encontrado.")
            return False

        # Busca o item pelo título
        for item in self._acervo:
            if item.titulo.lower() == titulo.lower():
                if item.emprestado:
                    print(f"❌ '{item.titulo}' já está emprestado.")
                    return False

                if item.emprestar():
                    usuario.emprestimos.append((item, datetime.now()))
                    self._emprestimos.append((usuario, item, datetime.now()))
                    print(f"✅ '{item.titulo}' emprestado para {usuario.nome}.")
                    return True

        print(f"❌ Item '{titulo}' não encontrado no acervo.")
        return False

    def devolver(self, matricula, titulo):
        usuario = self.buscar_usuario(matricula)
        if not usuario:
            print(f"❌ Usuário {matricula} não encontrado.")
            return False

        for emp in usuario.emprestimos:
            item, data_emprestimo = emp
            if item.titulo.lower() == titulo.lower():
                dias = (datetime.now() - data_emprestimo).days
                if dias > 14:   # prazo de 14 dias
                    multa = item.calcular_multa(dias - 14)
                    print(f"⚠️  Atraso de {dias - 14} dias. Multa: R$ {multa:.2f}")
                else:
                    print(f"✅ Devolvido no prazo ({dias} dias).")

                item.devolver()
                usuario.emprestimos.remove(emp)
                return True

        print(f"❌ Usuário não possui '{titulo}' emprestado.")
        return False

    # --- Relatórios ---
    def relatorio_acervo(self):
        print(f"\n📋 Acervo da {self.nome}:")
        print(f"   Total: {len(self._acervo)} itens")
        disponiveis = len(self.listar_disponiveis())
        print(f"   Disponíveis: {disponiveis}")
        print(f"   Emprestados: {len(self._acervo) - disponiveis}")
        print()
        for item in self._acervo:
            print(f"   {item}")

    # --- Métodos mágicos ---
    def __len__(self):
        return len(self._acervo)

    def __contains__(self, titulo):
        return any(item.titulo.lower() == titulo.lower() for item in self._acervo)

    def __str__(self):
        return f"📚 {self.nome} — {len(self)} itens no acervo"
          


# ============================================================
# DADOS DE EXEMPLO (pré-carregados)
# ============================================================
def popular_biblioteca(bib):
    bib.adicionar_item(Livro("Dom Casmurro", "Machado de Assis", 1899, 256, "978-85-359-0277-8"))
    bib.adicionar_item(Livro("1984", "George Orwell", 1949, 328, "978-85-359-0277-9"))
    bib.adicionar_item(Livro("Python Fluente", "Luciano Ramalho", 2015, 800, "978-85-7522-600-2"))
    bib.adicionar_item(Revista("Superinteressante", "Editora Abril", 2026, 450))
    bib.adicionar_item(Revista("Veja", "Editora Abril", 2026, 2890))
    bib.adicionar_item(DVD("Matrix", "Wachowski", 1999, 136))
    bib.adicionar_item(DVD("Inception", "Christopher Nolan", 2010, 148))

    bib.cadastrar_usuario(Usuario("Ana Silva", "ana@email.com", "2024001"))
    bib.cadastrar_usuario(Usuario("Carlos Souza", "carlos@email.com", "2024002"))


# ============================================================
# MENU PRINCIPAL
# ============================================================
def menu():
    bib = Biblioteca("Biblioteca Central")
    popular_biblioteca(bib)

    while True:
        print("\n" + "=" * 55)
        print(f"  {bib}")
        print("=" * 55)
        print("  1. Listar acervo completo")
        print("  2. Listar itens disponíveis")
        print("  3. Buscar por título")
        print("  4. Emprestar item")
        print("  5. Devolver item")
        print("  6. Cadastrar usuário")
        print("  7. Relatório do acervo")
        print("  0. Sair")
        print("=" * 55)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n📋 Todos os itens:")
            for item in bib.listar_todos():
                print(f"   {item}")

        elif opcao == "2":
            print("\n📗 Itens disponíveis:")
            disponiveis = bib.listar_disponiveis()
            if disponiveis:
                for item in disponiveis:
                    print(f"   {item}")
            else:
                print("   Nenhum item disponível no momento.")

        elif opcao == "3":
            termo = input("Digite o título ou parte dele: ").strip()
            resultados = bib.buscar_por_titulo(termo)
            if resultados:
                print(f"\n🔍 {len(resultados)} resultado(s):")
                for item in resultados:
                    print(f"   {item}")
            else:
                print(f"❌ Nenhum item encontrado para '{termo}'.")

        elif opcao == "4":
            matricula = input("Matrícula do usuário: ").strip()
            titulo = input("Título do item: ").strip()
            bib.emprestar(matricula, titulo)

        elif opcao == "5":
            matricula = input("Matrícula do usuário: ").strip()
            titulo = input("Título do item: ").strip()
            bib.devolver(matricula, titulo)

        elif opcao == "6":
            nome = input("Nome: ").strip()
            email = input("Email: ").strip()
            matricula = input("Matrícula: ").strip()
            try:
                bib.cadastrar_usuario(Usuario(nome, email, matricula))
            except ValueError as e:
                print(f"❌ Erro: {e}")

        elif opcao == "7":
            bib.relatorio_acervo()

        elif opcao == "0":
            print("👋 Até logo!")
            break

        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    menu()
          