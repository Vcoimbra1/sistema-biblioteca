"""
  Sistema de Biblioteca — Orientação a Objetos
  Banco: SQLite3
"""

import sys
import os


sys.path.insert(0, os.path.dirname(__file__))

from database.conexao import ConexaoBD
from controllers.controlador_autor import ControladorAutor
from controllers.controlador_livro import ControladorLivro
from controllers.controlador_emprestimo import ControladorEmprestimo
from views.ui import cabecalho, aviso, pausar, limpar, sucesso, info


class Aplicacao:
    

    def __init__(self):
        self._inicializar_banco()
        self.ctrl_autor     = ControladorAutor()
        self.ctrl_livro     = ControladorLivro()
        self.ctrl_emprestimo = ControladorEmprestimo()

    def _inicializar_banco(self):
        
        try:
            bd = ConexaoBD()
            bd.criar_tabelas()
        except Exception as e:
            print(f"Erro ao inicializar o banco de dados: {e}")
            sys.exit(1)

    def _menu_relatorios(self):
        from database.conexao import ConexaoBD
        limpar()
        cabecalho("RELATÓRIO GERAL")
        bd = ConexaoBD()
        cursor = bd.conectar()

        cursor.execute("SELECT COUNT(*) AS total FROM autores")
        info(f"Total de autores cadastrados : {cursor.fetchone()['total']}")

        cursor.execute("SELECT COUNT(*) AS total FROM livros")
        info(f"Total de livros no acervo    : {cursor.fetchone()['total']}")

        cursor.execute("SELECT SUM(quantidade) AS total FROM livros")
        r = cursor.fetchone()
        info(f"Total de exemplares          : {r['total'] or 0}")

        cursor.execute("SELECT COUNT(*) AS total FROM emprestimos WHERE devolvido=0")
        info(f"Empréstimos pendentes        : {cursor.fetchone()['total']}")

        cursor.execute("SELECT COUNT(*) AS total FROM emprestimos WHERE devolvido=1")
        info(f"Devoluções concluídas        : {cursor.fetchone()['total']}")

        print()
        bd.fechar()
        pausar()

    def executar(self):
        while True:
            limpar()
            cabecalho("SISTEMA DE BIBLIOTECA")
            print("""
  [1] Gerenciar Autores
  [2] Gerenciar Livros
  [3] Gerenciar Empréstimos
  [4] Relatório Geral
  [0] Sair do sistema
            """)
            opcao = input("  Opção: ").strip()

            if opcao == "1":
                self.ctrl_autor.menu()
            elif opcao == "2":
                self.ctrl_livro.menu()
            elif opcao == "3":
                self.ctrl_emprestimo.menu()
            elif opcao == "4":
                self._menu_relatorios()
            elif opcao == "0":
                self._sair()
            else:
                aviso("Opção inválida. Tente novamente.")
                pausar()

    def _sair(self):
        limpar()
        print("\n  ════════════════════════════════════════")
        print("  Obrigado por usar o Sistema de Biblioteca!")
        print("  Até logo. ")
        print("  ════════════════════════════════════════\n")
        sys.exit(0)


if __name__ == "__main__":
    app = Aplicacao()
    app.executar()
