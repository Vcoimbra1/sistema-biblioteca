# 📚 Sistema de Biblioteca — Proposta e Documentação

## Proposta do Projeto

**Nome:** Sistema de Gerenciamento de Biblioteca  
**Linguagem:** Python 3.10+  
**Banco de Dados:** SQLite3  
**Paradigma:** Orientação a Objetos (OOP)

---

## Descrição

Aplicação de terminal para gerenciar o acervo de uma biblioteca, permitindo
o cadastro de autores, livros e o controle de empréstimos a leitores.

---

## Diagrama do Banco de Dados

```
┌─────────────┐          ┌──────────────────┐          ┌──────────────────────┐
│   AUTORES   │  1     N │     LIVROS       │  1     N │     EMPRÉSTIMOS      │
├─────────────┤──────────┤──────────────────┤──────────┤──────────────────────┤
│ id (PK)     │          │ id (PK)          │          │ id (PK)              │
│ nome        │          │ titulo           │          │ livro_id (FK)        │
│ nacionali.. │          │ autor_id (FK) ◄──┘          │ leitor_nome          │
│ data_nasc.  │          │ isbn             │          │ leitor_contato       │
│ criado_em   │          │ ano              │          │ data_emprestimo      │
└─────────────┘          │ genero           │          │ data_devolucao       │
                         │ quantidade       │          │ devolvido (0/1)      │
                         │ criado_em        │          └──────────────────────┘
                         └──────────────────┘
```

**Relacionamentos:**
- Um **Autor** pode ter vários **Livros** (1:N)
- Um **Livro** pode ter vários **Empréstimos** ao longo do tempo (1:N)

---

## Estrutura de Arquivos

```
biblioteca/
│
├── main.py                          # Ponto de entrada da aplicação
│
├── database/
│   └── conexao.py                   # Classe ConexaoBD (Singleton)
│
├── models/
│   ├── autor.py                     # Classe Autor + CRUD
│   ├── livro.py                     # Classe Livro + CRUD
│   └── emprestimo.py                # Classe Empréstimo + CRUD
│
├── views/
│   └── ui.py                        # Funções de exibição no terminal
│
└── controllers/
    ├── controlador_autor.py         # Menu e lógica de Autores
    ├── controlador_livro.py         # Menu e lógica de Livros
    └── controlador_emprestimo.py    # Menu e lógica de Empréstimos
```

---

## Funcionalidades (CRUD por tabela)

### Autores
| Operação | Descrição |
|----------|-----------|
| Create   | Cadastrar novo autor |
| Read     | Listar todos / Buscar por nome |
| Update   | Editar dados do autor |
| Delete   | Excluir autor (protegido por FK) |

### Livros
| Operação | Descrição |
|----------|-----------|
| Create   | Cadastrar novo livro (vinculado a um autor) |
| Read     | Listar acervo / Buscar por título |
| Update   | Editar dados do livro |
| Delete   | Excluir livro (protegido por FK) |

### Empréstimos
| Operação | Descrição |
|----------|-----------|
| Create   | Registrar novo empréstimo |
| Read     | Listar todos / Pendentes / Buscar por leitor |
| Update   | Editar dados / Registrar devolução |
| Delete   | Excluir registro de empréstimo |

---

## Conceitos de OOP Aplicados

| Conceito       | Onde é usado |
|----------------|-------------|
| **Classe**     | `Autor`, `Livro`, `Emprestimo`, `ConexaoBD`, `Aplicacao`, etc. |
| **Encapsulamento** | Métodos privados `_listar()`, `_cadastrar()` nos controllers |
| **Herança**    | Estrutura base reutilizável nos controllers |
| **Singleton**  | `ConexaoBD.__new__()` — única instância de conexão |
| **Abstração**  | Models encapsulam toda lógica SQL |
| **Métodos estáticos** | `Autor.listar_todos()`, `Livro.buscar_por_id()` etc. |

---

## Como Executar

```bash
# 1. Entrar na pasta do projeto
cd biblioteca

# 2. Executar a aplicação
python main.py
```

> Requisito: Python 3.10 ou superior (sem dependências externas — apenas stdlib)

---

## Dados de Exemplo (pré-carregados)

O banco já vem com dados de demonstração:

- **3 autores**: Machado de Assis, Clarice Lispector, George Orwell  
- **4 livros**: Dom Casmurro, Memórias Póstumas, A Hora da Estrela, 1984  
- **2 empréstimos** ativos para demonstração

---

*Projeto desenvolvido para a disciplina de Banco de Dados / POO*
