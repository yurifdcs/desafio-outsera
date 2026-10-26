"""Monta o resumo da execução e devolve o status do quality gate.

Lê os junit.xml e os reexecucoes.json encontrados na pasta recebida,
imprime um markdown com total, aprovados, reprovados, duração e status
por módulo, e sai com código 1 se algum job, algum teste ou alguma
reexecução "verde" indicar problema.

Uso:
    python desafio-3-cicd/resumo_execucao.py resultados \\
        --job "Testes de API=success"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

NOMES_DE_MODULO = {
    "test_cep.py": "API · CEP",
    "test_bancos.py": "API · Bancos",
    "test_ddd.py": "API · DDD",
    "test_feriados.py": "API · Feriados",
    "test_cambio.py": "API · Câmbio",
    "test_metodos_http.py": "API · Métodos HTTP",
    "test_contrato.py": "API · Contrato",
    "test_crud.py": "API · CRUD",
    "test_navegacao.py": "E2E · Navegação",
    "test_login.py": "E2E · Login",
    "test_checkout.py": "E2E · Checkout",
    "test_acessibilidade.py": "E2E · Acessibilidade",
}

STATUS_DE_JOB = {
    "success": "aprovado",
    "failure": "reprovado",
    "cancelled": "cancelado",
    "skipped": "ignorado",
}


def formatar_duracao(segundos: float) -> str:
    if segundos < 60:
        return f"{segundos:.2f}s"
    minutos, resto = divmod(int(segundos), 60)
    return f"{minutos}m{resto:02d}s"


def nome_do_modulo(caso: ET.Element) -> str:
    arquivo = caso.get("file")
    if arquivo:
        nome = Path(arquivo).name
    else:
        partes = (caso.get("classname") or "").split(".")
        candidato = next((parte for parte in partes if parte.startswith("test_")), "")
        nome = f"{candidato}.py" if candidato else "desconhecido"
    return NOMES_DE_MODULO.get(nome, nome)


def nodeid_do_caso(caso: ET.Element) -> str:
    arquivo = caso.get("file") or ""
    nome = caso.get("name") or ""
    partes = (caso.get("classname") or "").split(".")
    if not arquivo and len(partes) >= 2:
        arquivo = f"{partes[0]}/{partes[1]}.py"
    if len(partes) >= 3:
        return f"{arquivo}::{partes[-1]}::{nome}"
    return f"{arquivo}::{nome}"


def status_do_caso(caso: ET.Element) -> tuple[str, str]:
    falha = caso.find("failure")
    if falha is None:
        falha = caso.find("error")
    if falha is not None:
        mensagem = (falha.get("message") or falha.text or "").strip()
        return "reprovado", mensagem
    if caso.find("skipped") is not None:
        return "ignorado", ""
    return "aprovado", ""


def ler_junit(caminho: Path) -> list[dict]:
    raiz = ET.parse(caminho).getroot()
    suites = raiz.findall("testsuite") if raiz.tag == "testsuites" else [raiz]
    casos = []
    for suite in suites:
        for caso in suite.findall("testcase"):
            status, mensagem = status_do_caso(caso)
            casos.append(
                {
                    "modulo": nome_do_modulo(caso),
                    "nodeid": nodeid_do_caso(caso),
                    "nome": caso.get("name") or caso.get("classname") or "teste",
                    "status": status,
                    "duracao": float(caso.get("time") or 0),
                    "mensagem": mensagem,
                }
            )
    return casos


def ler_reexecucoes(caminhos: list[Path]) -> tuple[list[str], list[dict]]:
    politicas: list[str] = []
    testes: list[dict] = []
    for caminho in caminhos:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        politica = (dados.get("politica") or "").strip()
        if politica and politica not in politicas:
            politicas.append(politica)
        for item in dados.get("testes_reexecutados") or []:
            testes.append(item)
    return politicas, testes


def aplicar_instabilidade(casos: list[dict], reexecutados: list[dict]) -> list[dict]:
    por_nodeid = {item.get("nodeid"): item for item in reexecutados}
    instaveis = []
    for caso in casos:
        info = por_nodeid.get(caso["nodeid"])
        if not info:
            continue
        if info.get("resultado_final") == "passed" and int(info.get("reexecucoes") or 0) > 0:
            caso["status"] = "instável"
            instaveis.append(info)
    conhecidos = {caso["nodeid"] for caso in casos}
    for info in reexecutados:
        if info.get("nodeid") in conhecidos:
            continue
        if info.get("resultado_final") == "passed" and int(info.get("reexecucoes") or 0) > 0:
            instaveis.append(info)
    return instaveis


def status_do_modulo(casos: list[dict]) -> str:
    statuses = {caso["status"] for caso in casos}
    if "reprovado" in statuses:
        return "reprovado"
    if "instável" in statuses:
        return "instável"
    if casos:
        return "aprovado"
    return "sem testes"


def agrupar(casos: list[dict]) -> dict[str, list[dict]]:
    grupos: dict[str, list[dict]] = defaultdict(list)
    for caso in casos:
        grupos[caso["modulo"]].append(caso)
    return grupos


def linha_tabela(colunas: list[str], negrito: bool = False) -> str:
    celulas = [coluna.replace("|", "/") for coluna in colunas]
    if negrito:
        celulas = [f"**{celula}**" for celula in celulas]
    return "| " + " | ".join(celulas) + " |"


def resumo_de_casos(casos: list[dict]) -> tuple[int, int, int, int, float]:
    total = len(casos)
    aprovados = sum(1 for caso in casos if caso["status"] == "aprovado")
    reprovados = sum(1 for caso in casos if caso["status"] == "reprovado")
    instaveis = sum(1 for caso in casos if caso["status"] == "instável")
    ignorados = sum(1 for caso in casos if caso["status"] == "ignorado")
    duracao = sum(caso["duracao"] for caso in casos)
    return total, aprovados, reprovados + instaveis, ignorados, duracao


def montar_markdown(
    casos: list[dict],
    jobs: list[tuple[str, str]],
    politicas: list[str],
    reexecutados: list[dict],
    instaveis: list[dict],
) -> str:
    grupos = agrupar(casos)
    total, aprovados, reprovados, ignorados, duracao = resumo_de_casos(casos)
    jobs_ruins = [nome for nome, resultado in jobs if resultado != "success"]
    consolidado = "aprovado"
    if reprovados or jobs_ruins or instaveis or not casos:
        consolidado = "reprovado"

    linhas = [
        "# Resumo da execução",
        "",
        f"**Status consolidado: {consolidado.upper()}**",
        "",
        (
            f"Total: {total} · Aprovados: {aprovados} · "
            f"Reprovados: {reprovados} · Ignorados: {ignorados} · "
            f"Duração: {formatar_duracao(duracao)}"
        ),
        "",
        "A duração soma o tempo dos testes. No CI, os módulos rodam em paralelo.",
        "",
        "## Módulos",
        "",
        linha_tabela(
            ["Módulo", "Total", "Aprovados", "Reprovados", "Ignorados", "Duração", "Status"]
        ),
        linha_tabela(["---", "---:", "---:", "---:", "---:", "---:", "---"]),
    ]

    for modulo in sorted(grupos):
        itens = grupos[modulo]
        n_total, n_ok, n_falha, n_skip, n_tempo = resumo_de_casos(itens)
        linhas.append(
            linha_tabela(
                [
                    modulo,
                    str(n_total),
                    str(n_ok),
                    str(n_falha),
                    str(n_skip),
                    formatar_duracao(n_tempo),
                    status_do_modulo(itens),
                ]
            )
        )

    linhas.append(
        linha_tabela(
            [
                "Consolidado",
                str(total),
                str(aprovados),
                str(reprovados),
                str(ignorados),
                formatar_duracao(duracao),
                consolidado,
            ],
            negrito=True,
        )
    )

    if jobs:
        linhas.extend(["", "## Jobs da pipeline", "", "| Job | Resultado |", "| --- | --- |"])
        for nome, resultado in jobs:
            linhas.append(f"| {nome} | {STATUS_DE_JOB.get(resultado, resultado)} |")

    linhas.extend(["", "## Reexecuções", ""])
    if politicas:
        for politica in politicas:
            linhas.append(politica)
            linhas.append("")
    else:
        linhas.append("Nenhum relatório de reexecução foi encontrado.")
        linhas.append("")

    if reexecutados:
        linhas.append("| Teste | Reexecuções | Resultado final |")
        linhas.append("| --- | ---: | --- |")
        for item in reexecutados:
            linhas.append(
                "| {teste} | {vezes} | {resultado} |".format(
                    teste=str(item.get("nodeid", "?")).replace("|", "/"),
                    vezes=int(item.get("reexecucoes") or 0),
                    resultado=item.get("resultado_final") or "?",
                )
            )
        linhas.append("")
        if instaveis:
            linhas.append(
                "Teste que só passou depois de ser reexecutado conta como reprovado "
                "no quality gate. A instabilidade não entra como sucesso."
            )
            linhas.append("")
    else:
        linhas.append("Nenhum teste precisou ser reexecutado.")
        linhas.append("")

    falhas = [caso for caso in casos if caso["status"] == "reprovado"]
    if falhas:
        linhas.extend(["## Falhas", ""])
        for caso in falhas:
            linhas.append(f"- `{caso['nodeid']}`")
            mensagem = caso["mensagem"].strip()
            if mensagem:
                trecho = "\n".join(mensagem.splitlines()[:20])
                if len(trecho) > 1500:
                    trecho = trecho[:1500] + "…"
                linhas.append("")
                linhas.append("```")
                linhas.append(trecho)
                linhas.append("```")
                linhas.append("")

    if not casos:
        linhas.extend(
            [
                "## Falhas",
                "",
                "Nenhum junit.xml foi encontrado. O quality gate reprova sem resultado de teste.",
                "",
            ]
        )

    return "\n".join(linhas).rstrip() + "\n"


def quality_gate_reprovado(
    casos: list[dict],
    jobs: list[tuple[str, str]],
    instaveis: list[dict],
) -> bool:
    if any(resultado != "success" for _, resultado in jobs):
        return True
    if not casos:
        return True
    if any(caso["status"] in {"reprovado", "instável"} for caso in casos):
        return True
    return bool(instaveis)


def parse_jobs(valores: list[str]) -> list[tuple[str, str]]:
    jobs = []
    for valor in valores:
        if "=" not in valor:
            raise SystemExit(f"Job inválido (use NOME=RESULTADO): {valor}")
        nome, resultado = valor.split("=", 1)
        jobs.append((nome.strip(), resultado.strip()))
    return jobs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resumo da execução e quality gate.")
    parser.add_argument("diretorio", type=Path, help="Pasta com junit.xml e reexecucoes.json")
    parser.add_argument("--job", action="append", default=[], metavar="NOME=RESULTADO")
    parser.add_argument("--saida", type=Path, help="Grava o markdown neste arquivo")
    args = parser.parse_args(argv)

    diretorio = args.diretorio
    casos: list[dict] = []
    if diretorio.is_dir():
        junits = sorted(diretorio.rglob("junit.xml"))
        reexecucoes = sorted(diretorio.rglob("reexecucoes.json"))
    elif diretorio.is_file() and diretorio.name == "junit.xml":
        junits = [diretorio]
        reexecucoes = []
    else:
        junits = []
        reexecucoes = []

    for caminho in junits:
        casos.extend(ler_junit(caminho))

    politicas, reexecutados = ler_reexecucoes(reexecucoes)
    instaveis = aplicar_instabilidade(casos, reexecutados)
    jobs = parse_jobs(args.job)
    markdown = montar_markdown(casos, jobs, politicas, reexecutados, instaveis)

    print(markdown, end="")
    if args.saida:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(markdown, encoding="utf-8")

    resumo_github = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumo_github:
        with open(resumo_github, "a", encoding="utf-8") as arquivo:
            arquivo.write(markdown)

    if quality_gate_reprovado(casos, jobs, instaveis):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
