"""Auditoria de acessibilidade com axe-core.

O motor vem do pacote axe-playwright-python (o axe.min.js vai junto com
a lib, sem depender de CDN no meio do teste).

Violação relevante, que reprova o teste, é a de impacto `critical` ou
`serious` — é assim que o axe classifica barreira real de acesso.
Moderate e minor entram no texto da falha só como contexto, quando já
existe violação relevante; sozinhas, não derrubam a suíte.
"""

from axe_playwright_python.sync_playwright import Axe

_AXE = Axe()
_IMPACTOS_RELEVANTES = ("critical", "serious")
_ORDEM = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}


def auditar(page, jornada: str) -> None:
    # options=None de propósito. Nesta versão do axe-playwright-python,
    # passar o dict de opções sem um contexto faz o axe receber as opções
    # no lugar do seletor. Sem o argumento, a chamada é axe.run() na
    # página inteira, e o corte por impacto fica aqui no Python.
    resultado = _AXE.run(page, options=None)
    violacoes = resultado.response.get("violations", [])

    relevantes = [item for item in violacoes if item.get("impact") in _IMPACTOS_RELEVANTES]
    if not relevantes:
        return

    outras = [item for item in violacoes if item.get("impact") not in _IMPACTOS_RELEVANTES]
    linhas = [
        f"Jornada '{jornada}' tem {len(relevantes)} violação(ões) relevante(s) "
        "(impacto critical ou serious):"
    ]
    for violacao in sorted(
        relevantes, key=lambda item: (_ORDEM.get(item.get("impact"), 9), item.get("id", ""))
    ):
        linhas.append(_descrever(violacao))

    if outras:
        linhas.append(
            f"Há também {len(outras)} violação(ões) moderate/minor. "
            "Elas não entram no critério de reprovação, mas ficam registradas:"
        )
        for violacao in sorted(
            outras, key=lambda item: (_ORDEM.get(item.get("impact"), 9), item.get("id", ""))
        ):
            linhas.append(_descrever(violacao))

    raise AssertionError("\n".join(linhas))


def _descrever(violacao: dict) -> str:
    impacto = violacao.get("impact") or "?"
    regra = violacao.get("id") or "?"
    ajuda = violacao.get("help") or ""
    quantidade = len(violacao.get("nodes") or [])
    exemplos = []
    for no in (violacao.get("nodes") or [])[:3]:
        alvo = no.get("target") or []
        if isinstance(alvo, list):
            exemplos.append(" ".join(str(parte) for parte in alvo))
        else:
            exemplos.append(str(alvo))

    linha = f"- [{impacto}] {regra}: {ajuda} ({quantidade} elemento(s))"
    if exemplos:
        linha += " | exemplos: " + "; ".join(exemplos)
    if violacao.get("helpUrl"):
        linha += f" | {violacao['helpUrl']}"
    return linha
