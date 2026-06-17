from models.emprestimo import Emprestimo
from models.livro import Livro
from views.ui import (cabecalho, secao, sucesso, erro, aviso,
                      ler_texto, ler_inteiro, confirmar, pausar, limpar)


class ControladorEmprestimo:

    def menu(self):
        while True:
            limpar()
            cabecalho("GERENCIAMENTO DE EMPRÉSTIMOS")
            print("""
  [1] Listar todos os empréstimos
  [2] Listar empréstimos pendentes
  [3] Buscar por leitor
  [4] Registrar novo empréstimo
  [5] Registrar devolução
  [6] Editar empréstimo
  [7] Excluir empréstimo
  [0] Voltar ao menu principal
            """)
            opcao = input("  Opção: ").strip()

            if opcao == "1":
                self._listar_todos()
            elif opcao == "2":
                self._listar_pendentes()
            elif opcao == "3":
                self._buscar_leitor()
            elif opcao == "4":
                self._registrar()
            elif opcao == "5":
                self._devolver()
            elif opcao == "6":
                self._editar()
            elif opcao == "7":
                self._excluir()
            elif opcao == "0":
                break
            else:
                aviso("Opção inválida.")
                pausar()
    def _listar_todos(self):
        limpar()
        cabecalho("TODOS OS EMPRÉSTIMOS")
        rows = Emprestimo.listar_todos()
        if not rows:
            aviso("Nenhum empréstimo registrado.")
        else:
            for r in rows:
                status = "✔ Devolvido" if r["devolvido"] else "⏳ Pendente"
                print(f"  [{r['id']}] {r['livro_titulo']} → {r['leitor_nome']} "
                      f"| Empréstimo: {r['data_emprestimo']} | {status}")
        pausar()

    def _listar_pendentes(self):
        limpar()
        cabecalho("EMPRÉSTIMOS PENDENTES")
        rows = Emprestimo.listar_pendentes()
        if not rows:
            aviso("Nenhum empréstimo pendente.")
        else:
            secao(f"{len(rows)} empréstimo(s) em aberto:")
            for r in rows:
                print(f"  [{r['id']}] {r['livro_titulo']} → {r['leitor_nome']} "
                      f"| Data: {r['data_emprestimo']} | Prev. devolução: {r['data_devolucao'] or '—'}")
        pausar()

    def _buscar_leitor(self):
        limpar()
        cabecalho("BUSCAR POR LEITOR")
        nome = ler_texto("Nome do leitor (ou parte)")
        rows = Emprestimo.buscar_por_leitor(nome)
        if not rows:
            aviso("Nenhum registro encontrado.")
        else:
            secao(f"{len(rows)} resultado(s):")
            for r in rows:
                status = "✔" if r["devolvido"] else "⏳"
                print(f"  [{r['id']}] {r['livro_titulo']} | {r['data_emprestimo']} {status}")
        pausar()
    def _registrar(self):
        limpar()
        cabecalho("REGISTRAR EMPRÉSTIMO")

        rows = Livro.listar_todos()
        if not rows:
            erro("Nenhum livro cadastrado.")
            pausar()
            return

        secao("Livros disponíveis:")
        disponiveis = []
        for r in rows:
            livro = Livro.buscar_por_id(r["id"])
            if livro and livro.disponivel():
                disponiveis.append(r)
                print(f"  [{r['id']}] {r['titulo']} — {r['autor_nome']} | Qtd: {r['quantidade']}")

        if not disponiveis:
            aviso("Não há livros disponíveis para empréstimo no momento.")
            pausar()
            return

        livro_id       = ler_inteiro("ID do livro", minimo=1)
        leitor_nome    = ler_texto("Nome do leitor")
        leitor_contato = ler_texto("Contato do leitor (email/telefone)", obrigatorio=False)
        data_prev      = ler_texto("Data prevista de devolução (DD/MM/AAAA)", obrigatorio=False)

        emp = Emprestimo(livro_id, leitor_nome, leitor_contato, data_devolucao=data_prev)
        if emp.salvar():
            sucesso(f"Empréstimo registrado com ID {emp.id}.")
        else:
            erro("Falha ao registrar empréstimo. Verifique o ID do livro.")
        pausar()

    def _devolver(self):
        limpar()
        cabecalho("REGISTRAR DEVOLUÇÃO")

        rows = Emprestimo.listar_pendentes()
        if not rows:
            aviso("Nenhum empréstimo pendente.")
            pausar()
            return

        secao("Empréstimos pendentes:")
        for r in rows:
            print(f"  [{r['id']}] {r['livro_titulo']} → {r['leitor_nome']} | {r['data_emprestimo']}")

        id_ = ler_inteiro("ID do empréstimo a devolver")
        emp = Emprestimo.buscar_por_id(id_)
        if not emp:
            aviso(f"Empréstimo {id_} não encontrado.")
            pausar()
            return
        if emp.devolvido:
            aviso("Este empréstimo já foi devolvido.")
            pausar()
            return

        if confirmar("Confirmar devolução? (s/n)"):
            if emp.registrar_devolucao():
                sucesso("Devolução registrada com sucesso!")
            else:
                erro("Falha ao registrar devolução.")
        else:
            aviso("Operação cancelada.")
        pausar()

    def _editar(self):
        limpar()
        cabecalho("EDITAR EMPRÉSTIMO")
        id_ = ler_inteiro("ID do empréstimo")
        emp = Emprestimo.buscar_por_id(id_)
        if not emp:
            aviso(f"Empréstimo {id_} não encontrado.")
            pausar()
            return

        print(f"\n  Dados atuais: {emp}")
        secao("Novos dados (ENTER para manter):")

        emp.leitor_nome    = input(f"  Leitor [{emp.leitor_nome}]: ").strip() or emp.leitor_nome
        emp.leitor_contato = input(f"  Contato [{emp.leitor_contato}]: ").strip() or emp.leitor_contato
        emp.data_devolucao = input(f"  Prev. devolução [{emp.data_devolucao}]: ").strip() or emp.data_devolucao
        raw_dev = input(f"  Devolvido? 0=Não 1=Sim [{int(emp.devolvido)}]: ").strip()
        if raw_dev in ("0", "1"):
            emp.devolvido = bool(int(raw_dev))

        if confirmar():
            if emp.atualizar():
                sucesso("Empréstimo atualizado.")
            else:
                erro("Falha ao atualizar.")
        else:
            aviso("Operação cancelada.")
        pausar()
        
    def _excluir(self):
        limpar()
        cabecalho("EXCLUIR EMPRÉSTIMO")
        id_ = ler_inteiro("ID do empréstimo")
        emp = Emprestimo.buscar_por_id(id_)
        if not emp:
            aviso(f"Empréstimo {id_} não encontrado.")
            pausar()
            return

        print(f"\n  Dados: {emp}")
        if confirmar("Confirmar exclusão? (s/n)"):
            if Emprestimo.excluir(id_):
                sucesso("Empréstimo excluído.")
            else:
                erro("Falha ao excluir.")
        else:
            aviso("Operação cancelada.")
        pausar()
