"""
Módulo de conexão com o banco de dados SQLite3.
Gerencia a criação e manutenção das tabelas do sistema.
"""

import sqlite3
import os


class ConexaoBD:
    """Classe responsável pela conexão e gerenciamento do banco de dados."""

    _instancia = None  # Singleton

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if self._inicializado:
            return
        caminho = os.path.join(os.path.dirname(__file__), "biblioteca.db")
        self.caminho_db = caminho
        self.conexao = None
        self._inicializado = True

    def conectar(self):
        """Abre a conexão com o banco e retorna o cursor."""
        self.conexao = sqlite3.connect(self.caminho_db)
        self.conexao.execute("PRAGMA foreign_keys = ON")
        self.conexao.row_factory = sqlite3.Row
        return self.conexao.cursor()

    def commit(self):
        if self.conexao:
            self.conexao.commit()

    def fechar(self):
        if self.conexao:
            self.conexao.close()
            self.conexao = None

    def criar_tabelas(self):
        """Cria as tabelas do banco de dados caso não existam."""
        cursor = self.conectar()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS autores (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nome        TEXT    NOT NULL,
                nacionalidade TEXT,
                data_nascimento TEXT,
                criado_em   TEXT DEFAULT (datetime('now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS livros (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo      TEXT    NOT NULL,
                autor_id    INTEGER NOT NULL,
                isbn        TEXT    UNIQUE,
                ano         INTEGER,
                genero      TEXT,
                quantidade  INTEGER DEFAULT 1,
                criado_em   TEXT DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS emprestimos (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_id        INTEGER NOT NULL,
                leitor_nome     TEXT    NOT NULL,
                leitor_contato  TEXT,
                data_emprestimo TEXT    DEFAULT (date('now','localtime')),
                data_devolucao  TEXT,
                devolvido       INTEGER DEFAULT 0,
                FOREIGN KEY (livro_id) REFERENCES livros(id) ON DELETE RESTRICT
            );
        """)

        self.commit()
        self.fechar()
