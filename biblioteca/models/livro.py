from database.conexao import ConexaoBD


class Livro:
 

    def __init__(self, titulo: str, autor_id: int, isbn: str = "",
                 ano: int = None, genero: str = "", quantidade: int = 1, id: int = None):
        self.id = id
        self.titulo = titulo
        self.autor_id = autor_id
        self.isbn = isbn
        self.ano = ano
        self.genero = genero
        self.quantidade = quantidade

    def __str__(self):
        return (f"[{self.id}] {self.titulo} | Autor ID: {self.autor_id} | "
                f"Gênero: {self.genero or '—'} | Ano: {self.ano or '—'} | "
                f"ISBN: {self.isbn or '—'} | Qtd: {self.quantidade}")
    
    def salvar(self) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute(
                """INSERT INTO livros (titulo, autor_id, isbn, ano, genero, quantidade)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (self.titulo, self.autor_id, self.isbn, self.ano, self.genero, self.quantidade)
            )
            bd.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"  Erro ao salvar livro: {e}")
            return False
        finally:
            bd.fechar()

    @staticmethod
    def listar_todos() -> list:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("""
                SELECT l.*, a.nome AS autor_nome
                FROM livros l
                JOIN autores a ON l.autor_id = a.id
                ORDER BY l.titulo
            """)
            return cursor.fetchall()
        finally:
            bd.fechar()

    @staticmethod
    def buscar_por_id(id: int):
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
            r = cursor.fetchone()
            if r:
                return Livro(r["titulo"], r["autor_id"], r["isbn"],
                             r["ano"], r["genero"], r["quantidade"], r["id"])
            return None
        finally:
            bd.fechar()

    @staticmethod
    def buscar_por_titulo(titulo: str) -> list:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("""
                SELECT l.*, a.nome AS autor_nome
                FROM livros l
                JOIN autores a ON l.autor_id = a.id
                WHERE l.titulo LIKE ?
                ORDER BY l.titulo
            """, (f"%{titulo}%",))
            return cursor.fetchall()
        finally:
            bd.fechar()

    def disponivel(self) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute(
                "SELECT COUNT(*) AS total FROM emprestimos WHERE livro_id=? AND devolvido=0",
                (self.id,)
            )
            emprestados = cursor.fetchone()["total"]
            return self.quantidade > emprestados
        finally:
            bd.fechar()

    def atualizar(self) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute(
                """UPDATE livros SET titulo=?, autor_id=?, isbn=?, ano=?,
                   genero=?, quantidade=? WHERE id=?""",
                (self.titulo, self.autor_id, self.isbn, self.ano,
                 self.genero, self.quantidade, self.id)
            )
            bd.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"  Erro ao atualizar livro: {e}")
            return False
        finally:
            bd.fechar()

    @staticmethod
    def excluir(id: int) -> bool:
        bd = ConexaoBD()
        try:
            cursor = bd.conectar()
            cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
            bd.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"  Erro ao excluir livro: {e}")
            return False
        finally:
            bd.fechar()
