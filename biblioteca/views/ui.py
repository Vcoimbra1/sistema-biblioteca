

LINHA = "═" * 60
LINHA_SIMPLES = "─" * 60


def cabecalho(titulo: str):
    
    print(f"\n{LINHA}")
    print(f"   {titulo}")
    print(LINHA)


def secao(titulo: str):
    print(f"\n{LINHA_SIMPLES}")
    print(f"  {titulo}")
    print(LINHA_SIMPLES)


def sucesso(msg: str):
    print(f"\n  ✅  {msg}")


def erro(msg: str):
    print(f"\n  ❌  {msg}")


def aviso(msg: str):
    print(f"\n  ⚠️   {msg}")


def info(msg: str):
    print(f"  ℹ️   {msg}")


def ler_texto(prompt: str, obrigatorio: bool = True) -> str:
    while True:
        valor = input(f"  {prompt}: ").strip()
        if valor or not obrigatorio:
            return valor
        erro("Campo obrigatório. Tente novamente.")


def ler_inteiro(prompt: str, minimo: int = None, maximo: int = None,
                obrigatorio: bool = True) -> int | None:
    while True:
        raw = input(f"  {prompt}: ").strip()
        if not raw and not obrigatorio:
            return None
        try:
            valor = int(raw)
            if minimo is not None and valor < minimo:
                erro(f"Valor mínimo: {minimo}")
                continue
            if maximo is not None and valor > maximo:
                erro(f"Valor máximo: {maximo}")
                continue
            return valor
        except ValueError:
            erro("Digite um número inteiro válido.")


def confirmar(prompt: str = "Confirmar? (s/n)") -> bool:
    resp = input(f"\n  {prompt} ").strip().lower()
    return resp == "s"


def pausar():
    input("\n  Pressione ENTER para continuar...")


def limpar():
    print("\n" * 2)


def exibir_tabela(colunas: list[str], linhas: list, larguras: list[int] = None):
    if not larguras:
        larguras = [max(18, len(c) + 2) for c in colunas]

    header = "  " + "  ".join(str(c).ljust(w) for c, w in zip(colunas, larguras))
    sep = "  " + "  ".join("-" * w for w in larguras)

    print(f"\n{header}")
    print(sep)
    for linha in linhas:
        print("  " + "  ".join(str(v).ljust(w) for v, w in zip(linha, larguras)))
