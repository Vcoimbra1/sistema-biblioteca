from models.autor import Autor
from views.ui import (cabecalho, secao, sucesso, erro, aviso,
                      ler_texto, ler_inteiro, confirmar, pausar, limpar)


class ControladorAutor:

    def menu(self):
        while True:
            limpar()
            cabecalho("GERENCIAMENTO DE AUTORES")
            print("""
  [1] Listar todos os autores
  [2] Buscar autor por nome
  [3] Cadastrar novo autor
  [4] Editar autor
  [5] Excluir autor
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
        cabecalho("LISTA DE AUTORES")
        autores = Autor.listar_todos()
        if not autores:
            aviso("Nenhum autor cadastrado.")
        else:
            for a in autores:
                print(f"  {a}")
        pausar()

    def _buscar(self):
        limpar()
        cabecalho("BUSCAR AUTOR")
        nome = ler_texto("Nome (ou parte do nome)")
        autores = Autor.buscar_por_nome(nome)
        if not autores:
            aviso("Nenhum autor encontrado.")
        else:
            secao(f"{len(autores)} resultado(s):")
            for a in autores:
                print(f"  {a}")
        pausar()

    def _cadastrar(self):
        limpar()
        cabecalho("CADASTRAR AUTOR")
        nome = ler_texto("Nome completo")
        nacionalidade = ler_texto("Nacionalidade", obrigatorio=False)
        data_nasc = ler_texto("Data de nascimento (DD/MM/AAAA)", obrigatorio=False)

        autor = Autor(nome, nacionalidade, data_nasc)
        if autor.salvar():
            sucesso(f'Autor "{nome}" cadastrado com ID {autor.id}.')
        else:
            erro("Falha ao cadastrar o autor.")
        pausar()

    def _editar(self):
        limpar()
        cabecalho("EDITAR AUTOR")
        id_ = ler_inteiro("ID do autor")
        autor = Autor.buscar_por_id(id_)
        if not autor:
            aviso(f"Autor com ID {id_} não encontrado.")
            pausar()
            return

        print(f"\n  Dados atuais: {autor}")
        secao("Novos dados (ENTER para manter o valor atual):")

        novo_nome = input(f"  Nome [{autor.nome}]: ").strip() or autor.nome
        nova_nac  = input(f"  Nacionalidade [{autor.nacionalidade}]: ").strip() or autor.nacionalidade
        nova_nasc = input(f"  Nascimento [{autor.data_nascimento}]: ").strip() or autor.data_nascimento

        autor.nome = novo_nome
        autor.nacionalidade = nova_nac
        autor.data_nascimento = nova_nasc

        if confirmar():
            if autor.atualizar():
                sucesso("Autor atualizado com sucesso.")
            else:
                erro("Falha ao atualizar.")
        else:
            aviso("Operação cancelada.")
        pausar()

    def _excluir(self):
        limpar()
        cabecalho("EXCLUIR AUTOR")
        id_ = ler_inteiro("ID do autor")
        autor = Autor.buscar_por_id(id_)
        if not autor:
            aviso(f"Autor com ID {id_} não encontrado.")
            pausar()
            return

        print(f"\n  Dados: {autor}")
        if confirmar("Deseja excluir este autor? (s/n)"):
            if Autor.excluir(id_):
                sucesso("Autor excluído com sucesso.")
            else:
                erro("Não foi possível excluir. Verifique se há livros vinculados.")
        else:
            aviso("Operação cancelada.")
        pausar()
