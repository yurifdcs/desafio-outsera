"""URL do site sob teste e política de retry.

A URL não fica no pytest.ini. E2E_RERUNS parte de zero: falha é falha.
Subir esse número repete o teste, mas um caso que só passa na
retentativa continua reprovando a suíte (veja conftest.py).
"""

import os
from pathlib import Path

_DIRETORIO = Path(__file__).resolve().parent
_DOTENV_CARREGADO = False


def _carregar_dotenv() -> None:
    global _DOTENV_CARREGADO
    if _DOTENV_CARREGADO:
        return
    _DOTENV_CARREGADO = True

    arquivo = _DIRETORIO / ".env"
    if not arquivo.is_file():
        return

    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip().strip("\"'"))


def url_obrigatoria(nome: str) -> str:
    _carregar_dotenv()
    valor = os.environ.get(nome, "").strip().rstrip("/")
    if not valor:
        raise RuntimeError(
            f"A variável de ambiente {nome} não está definida. "
            "Exporte a variável ou copie .env.example para .env antes de rodar a suíte."
        )
    if not valor.startswith(("http://", "https://")):
        raise RuntimeError(
            f"{nome} precisa incluir o protocolo (http:// ou https://). Recebi: {valor}"
        )
    return valor


def reruns_configurados() -> int:
    _carregar_dotenv()
    bruto = os.environ.get("E2E_RERUNS", "0").strip()
    try:
        valor = int(bruto)
    except ValueError as erro:
        raise RuntimeError(f"E2E_RERUNS precisa ser um inteiro. Recebi: {bruto}") from erro
    if valor < 0:
        raise RuntimeError("E2E_RERUNS não pode ser negativo.")
    return valor


def atraso_entre_reruns() -> float:
    _carregar_dotenv()
    bruto = os.environ.get("E2E_RERUNS_DELAY", "1").strip()
    try:
        valor = float(bruto)
    except ValueError as erro:
        raise RuntimeError(f"E2E_RERUNS_DELAY precisa ser um número. Recebi: {bruto}") from erro
    if valor < 0:
        raise RuntimeError("E2E_RERUNS_DELAY não pode ser negativo.")
    return valor
