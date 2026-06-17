from models.livro import Livro
from models.autor import Autor
from views.ui import (cabecalho, secao, sucesso, erro, aviso,
                      ler_texto, ler_inteiro, confirmar, pausar, limpar)


class ControladorLivro:

    def menu(self):
        while True:
            limpar()
            cabecalho("GERENCIAMENTO DE LIVROS")
            print("""
  [1] Listar todos os livros
  [2] Buscar livro por título
  [3] Cadastrar novo livro
  [4] Editar livro
  [5] Excluir livro
  [0] Voltar ao menu principal
            """)
            opcao = input("  Opção: ").strip()

            if opcao == "1":
                self._listar()
            elif opcao == "2":
                self._buscar()
            elif opcao == "3":
                self._cadastrar()
            elif opcao == "4":
                self._editar()
            elif opcao == "5":
                self._excluir()
            elif opcao == "0":
                break
            else:
                aviso("Opção inválida.")
                pausar()

    def _listar(self):
        limpar()
        cabecalho("ACERVO DE LIVROS")
        rows = Livro.listar_todos()
        if not rows:
            aviso("Nenhum livro cadastrado.")
        else:
            for r in rows:
                disp = "✅" if r["quantidade"] > 0 else "❌"
                print(f"  [{r['id']}] {r['titulo']} — {r['autor_nome']} "
                      f"| {r['genero'] or '—'} | {r['ano'] or '—'} | Qtd: {r['quantidade']} {disp}")
        pausar()

    def _buscar(self):
        limpar()
        cabecalho("BUSCAR LIVRO")
        titulo = ler_texto("Título (ou parte)")
        rows = Livro.buscar_por_titulo(titulo)
        if not rows:
            aviso("Nenhum livro encontrado.")
        else:
            secao(f"{len(rows)} resultado(s):")
            for r in rows:
                print(f"  [{r['id']}] {r['titulo']} — {r['autor_nome']} | {r['genero'] or '—'}")
        pausar()

    def _cadastrar(self):
        limpar()
        cabecalho("CADASTRAR LIVRO")

        autores = Autor.listar_todos()
        if not autores:
            erro("Cadastre pelo menos um autor antes de adicionar livros.")
            pausar()
            return

        secao("Autores disponíveis:")
        for a in autores:
            print(f"  {a}")

        titulo     = ler_texto("Título do livro")
        autor_id   = ler_inteiro("ID do autor", minimo=1)
        isbn       = ler_texto("ISBN", obrigatorio=False)
        ano        = ler_inteiro("Ano de publicação", obrigatorio=False)
        genero     = ler_texto("Gênero", obrigatorio=False)
        quantidade = ler_inteiro("Quantidade de exemplares", minimo=1) or 1

        livro = Livro(titulo, autor_id, isbn, ano, genero, quantidade)
        if livro.salvar():
            sucesso(f'Livro "{titulo}" cadastrado com ID {livro.id}.')
        else:
            erro("Falha ao cadastrar livro. Verifique o ID do autor.")
        pausar()

    def _editar(self):
        limpar()
        cabecalho("EDITAR LIVRO")
        id_ = ler_inteiro("ID do livro")
        livro = Livro.buscar_por_id(id_)
        if not livro:
            aviso(f"Livro com ID {id_} não encontrado.")
            pausar()
            return

        print(f"\n  Dados atuais: {livro}")
        secao("Novos dados (ENTER para manter o valor atual):")

        livro.titulo    = input(f"  Título [{livro.titulo}]: ").strip() or livro.titulo
        raw_autor       = input(f"  ID do Autor [{livro.autor_id}]: ").strip()
        livro.autor_id  = int(raw_autor) if raw_autor.isdigit() else livro.autor_id
        livro.isbn      = input(f"  ISBN [{livro.isbn}]: ").strip() or livro.isbn
        raw_ano         = input(f"  Ano [{livro.ano}]: ").strip()
        livro.ano       = int(raw_ano) if raw_ano.isdigit() else livro.ano
        livro.genero    = input(f"  Gênero [{livro.genero}]: ").strip() or livro.genero
        raw_qtd         = input(f"  Quantidade [{livro.quantidade}]: ").strip()
        livro.quantidade = int(raw_qtd) if raw_qtd.isdigit() else livro.quantidade

        if confirmar():
            if livro.atualizar():
                sucesso("Livro atualizado com sucesso.")
            else:
                erro("Falha ao atualizar livro.")
        else:
            aviso("Operação cancelada.")
        pausar()

    def _excluir(self):
        limpar()
        cabecalho("EXCLUIR LIVRO")
        id_ = ler_inteiro("ID do livro")
        livro = Livro.buscar_por_id(id_)
        if not livro:
            aviso(f"Livro com ID {id_} não encontrado.")
            pausar()
            return

        print(f"\n  Dados: {livro}")
        if confirmar("Deseja excluir este livro? (s/n)"):
            if Livro.excluir(id_):
                sucesso("Livro excluído com sucesso.")
            else:
                erro("Não foi possível excluir. Verifique se há empréstimos ativos.")
        else:
            aviso("Operação cancelada.")
        pausar()
