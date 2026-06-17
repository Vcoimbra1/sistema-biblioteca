from database.conexao import ConexaoBD


class Autor:

    def __init__(self, nome: str, nacionalidade: str = "", data_nascimento: str = "", id: int = None):
        self.id = id
        self.nome = nome
        self.nacionalidade = nacionalidade
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f"[{self.id}] {self.nome} | {self.nacionalidade or '—'} | Nasc.: {self.data_nascimento or '—'}"

    def salvar(self) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute(
                "INSERT INTO autores (nome, nacionalidade, data_nascimento) VALUES (?, ?, ?)",
                (self.nome, self.nacionalidade, self.data_nascimento)
            )
            bd.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"  Erro ao salvar autor: {e}")
            return False
        finally:
            bd.fechar()

    @staticmethod
    def listar_todos() -> list:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("SELECT * FROM autores ORDER BY nome")
            rows = cursor.fetchall()
            return [Autor(r["nome"], r["nacionalidade"], r["data_nascimento"], r["id"]) for r in rows]
        finally:
            bd.fechar()

    @staticmethod
    def buscar_por_id(id: int):
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("SELECT * FROM autores WHERE id = ?", (id,))
            r = cursor.fetchone()
            return Autor(r["nome"], r["nacionalidade"], r["data_nascimento"], r["id"]) if r else None
        finally:
            bd.fechar()

    @staticmethod
    def buscar_por_nome(nome: str) -> list:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("SELECT * FROM autores WHERE nome LIKE ? ORDER BY nome", (f"%{nome}%",))
            rows = cursor.fetchall()
            return [Autor(r["nome"], r["nacionalidade"], r["data_nascimento"], r["id"]) for r in rows]
        finally:
            bd.fechar()

    def atualizar(self) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute(
                "UPDATE autores SET nome=?, nacionalidade=?, data_nascimento=? WHERE id=?",
                (self.nome, self.nacionalidade, self.data_nascimento, self.id)
            )
            bd.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"  Erro ao atualizar autor: {e}")
            return False
        finally:
            bd.fechar()

    @staticmethod
    def excluir(id: int) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("DELETE FROM autores WHERE id = ?", (id,))
            bd.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"  Erro ao excluir autor: {e}")
            return False
        finally:
            bd.fechar()
