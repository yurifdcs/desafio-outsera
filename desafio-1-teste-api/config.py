"""URLs dos ambientes sob teste.

Nenhuma URL fica escrita nos testes nem no pytest.ini. Quem escolhe o
ambiente é a variável (exportada no shell, no CI ou num `.env` local,
que não entra no git).
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
