from database.conexao import ConexaoBD


class Emprestimo:

    def __init__(self, livro_id: int, leitor_nome: str, leitor_contato: str = "",
                 data_emprestimo: str = None, data_devolucao: str = None,
                 devolvido: bool = False, id: int = None):
        self.id = id
        self.livro_id = livro_id
        self.leitor_nome = leitor_nome
        self.leitor_contato = leitor_contato
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
        self.devolvido = devolvido

    def __str__(self):
        status = "✔ Devolvido" if self.devolvido else "⏳ Pendente"
        return (f"[{self.id}] Livro ID: {self.livro_id} | Leitor: {self.leitor_nome} | "
                f"Empréstimo: {self.data_emprestimo} | "
                f"Devolução: {self.data_devolucao or '—'} | {status}")

    # ─── CREATE ────────────────────────────────────────────────────────────────
    def salvar(self) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute(
                """INSERT INTO emprestimos (livro_id, leitor_nome, leitor_contato,
                   data_emprestimo, data_devolucao, devolvido)
                   VALUES (?, ?, ?, date('now','localtime'), ?, 0)""",
                (self.livro_id, self.leitor_nome, self.leitor_contato, self.data_devolucao)
            )
            bd.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"  Erro ao registrar empréstimo: {e}")
            return False
        finally:
            bd.fechar()

    @staticmethod
    def listar_todos() -> list:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("""
                SELECT e.*, l.titulo AS livro_titulo
                FROM emprestimos e
                JOIN livros l ON e.livro_id = l.id
                ORDER BY e.devolvido, e.data_emprestimo DESC
            """)
            return cursor.fetchall()
        finally:
            bd.fechar()

    @staticmethod
    def listar_pendentes() -> list:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("""
                SELECT e.*, l.titulo AS livro_titulo
                FROM emprestimos e
                JOIN livros l ON e.livro_id = l.id
                WHERE e.devolvido = 0
                ORDER BY e.data_emprestimo
            """)
            return cursor.fetchall()
        finally:
            bd.fechar()

    @staticmethod
    def buscar_por_id(id: int):
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("SELECT * FROM emprestimos WHERE id = ?", (id,))
            r = cursor.fetchone()
            if r:
                return Emprestimo(r["livro_id"], r["leitor_nome"], r["leitor_contato"],
                                  r["data_emprestimo"], r["data_devolucao"],
                                  bool(r["devolvido"]), r["id"])
            return None
        finally:
            bd.fechar()

    @staticmethod
    def buscar_por_leitor(nome: str) -> list:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("""
                SELECT e.*, l.titulo AS livro_titulo
                FROM emprestimos e
                JOIN livros l ON e.livro_id = l.id
                WHERE e.leitor_nome LIKE ?
                ORDER BY e.data_emprestimo DESC
            """, (f"%{nome}%",))
            return cursor.fetchall()
        finally:
            bd.fechar()

    def registrar_devolucao(self) -> bool:
        """Marca o empréstimo como devolvido com a data atual."""
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute(
                """UPDATE emprestimos
                   SET devolvido=1, data_devolucao=date('now','localtime')
                   WHERE id=?""",
                (self.id,)
            )
            bd.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"  Erro ao registrar devolução: {e}")
            return False
        finally:
            bd.fechar()

    def atualizar(self) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute(
                """UPDATE emprestimos
                   SET leitor_nome=?, leitor_contato=?, data_devolucao=?, devolvido=?
                   WHERE id=?""",
                (self.leitor_nome, self.leitor_contato,
                 self.data_devolucao, int(self.devolvido), self.id)
            )
            bd.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"  Erro ao atualizar empréstimo: {e}")
            return False
        finally:
            bd.fechar()

    @staticmethod
    def excluir(id: int) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("DELETE FROM emprestimos WHERE id = ?", (id,))
            bd.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"  Erro ao excluir empréstimo: {e}")
            return False
        finally:
            bd.fechar()
