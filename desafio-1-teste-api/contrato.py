"""Validação de contrato (JSON Schema) em cima do corpo da resposta.

Os testes de endpoint continuam checando status, headers e campos
pontuais. Aqui entra a checagem estrutural: tipos, campos obrigatórios
e formato. Campo extra na resposta não reprova (`additionalProperties`
fica liberado) — o contrato protege o que o cliente precisa ler, sem
quebrar quando a API acrescenta um atributo novo.
"""

import json
from pathlib import Path

from jsonschema import Draft202012Validator

_CONTRATOS = Path(__file__).resolve().parent / "contratos"


def validar_contrato(instancia, nome_schema: str) -> None:
    caminho = _CONTRATOS / nome_schema
    schema = json.loads(caminho.read_text(encoding="utf-8"))
    erros = sorted(
        Draft202012Validator(schema).iter_errors(instancia),
        key=lambda erro: list(erro.absolute_path),
    )
    if not erros:
        return

    linhas = [f"Resposta fora do contrato {nome_schema}:"]
    for erro in erros:
        caminho_erro = "/".join(str(parte) for parte in erro.absolute_path) or "(raiz)"
        linhas.append(f"- {caminho_erro}: {erro.message}")
    raise AssertionError("\n".join(linhas))
