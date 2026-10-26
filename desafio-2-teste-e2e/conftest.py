"""
Configuração compartilhada da suíte E2E.

A URL base vem de E2E_BASE_URL. Screenshot e trace ficam a cargo das
flags do pytest.ini e só são mantidos quando o cenário falha. O retry
global saiu do pytest.ini: E2E_RERUNS=0 por padrão e, se alguém ligar
a reexecução, um teste que só passa na retentativa reprova a sessão.
"""

import base64
import json
from contextlib import suppress
from pathlib import Path

import pytest
from playwright.sync_api import expect

from config import atraso_entre_reruns, reruns_configurados, url_obrigatoria
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

try:
    from pytest_html import extras as extras_html
except ImportError:  # a suíte roda sem o relatório HTML, se o plugin não estiver instalado
    extras_html = None

# o site é uma SPA em React e às vezes demora um pouco mais que o padrão
# do Playwright (5s) pra carregar o "chunk" JS de uma rota nova depois de
# um clique (ex: carrinho -> checkout). Aumento a margem pra não pegar
# falso negativo por lentidão de carregamento, sem exagerar no tempo.
expect.set_options(timeout=10_000)

_RERUNS = 0
_ESTADO: dict[str, dict] = {}

POLITICA_DE_RETRY = (
    "Não há rerun global no pytest.ini. A reexecução só ocorre se E2E_RERUNS "
    "for maior que zero. Quando um teste só passa na retentativa, a suíte é "
    "reprovada: a instabilidade fica explícita no relatório em vez de virar sucesso."
)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    global _RERUNS
    try:
        config.option.base_url = url_obrigatoria("E2E_BASE_URL")
        _RERUNS = reruns_configurados()
        if _RERUNS > 0:
            config.option.reruns = _RERUNS
            config.option.reruns_delay = atraso_entre_reruns()
    except RuntimeError as erro:
        raise pytest.UsageError(str(erro)) from erro


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed and report.when in {"setup", "call"}:
        _anexar_screenshot(item, report)


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    info = _ESTADO.setdefault(report.nodeid, {"reexecucoes": 0, "resultado_final": report.outcome})
    if report.outcome == "rerun":
        info["reexecucoes"] += 1
    else:
        info["resultado_final"] = report.outcome


def pytest_terminal_summary(terminalreporter):
    terminalreporter.write_sep("=", "Estratégia de retry")
    terminalreporter.write_line(f"E2E_RERUNS={_RERUNS}. {POLITICA_DE_RETRY}")
    reexecutados = _testes_reexecutados()
    if not reexecutados:
        terminalreporter.write_line("Nenhum teste precisou ser reexecutado.")
        return
    for item in reexecutados:
        terminalreporter.write_line(
            f"- {item['nodeid']}: {item['reexecucoes']} reexecução(ões), "
            f"resultado final {item['resultado_final']}"
        )
    if _instaveis(reexecutados):
        terminalreporter.write_line(
            "INSTABILIDADE: teste que só passou na retentativa reprova a suíte."
        )


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    reexecutados = _testes_reexecutados()
    _gravar_reexecucoes(reexecutados)
    codigo_atual = session.exitstatus if session.exitstatus is not None else exitstatus
    if _instaveis(reexecutados) and int(codigo_atual) == 0:
        session.exitstatus = pytest.ExitCode.TESTS_FAILED


@pytest.fixture
def home_page(page):
    return HomePage(page)


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def product_page(page):
    return ProductPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


def _anexar_screenshot(item, report):
    if extras_html is None:
        return
    page = item.funcargs.get("page")
    if page is None:
        return
    # falha ao tirar o screenshot não pode esconder o erro original do teste
    png = None
    with suppress(Exception):
        if not page.is_closed():
            png = base64.b64encode(page.screenshot(full_page=True, timeout=10_000)).decode("ascii")
    if not png:
        return
    extras = list(getattr(report, "extras", []) or [])
    extras.append(extras_html.png(png, name="Screenshot da falha"))
    extras.append(
        extras_html.text(
            "Trace do Playwright (trace.zip) fica em relatorios/evidencias "
            "e é publicado como artefato da pipeline junto com este screenshot.",
            name="Evidências",
        )
    )
    report.extras = extras


def _testes_reexecutados() -> list[dict]:
    return [
        {
            "nodeid": nodeid,
            "reexecucoes": info["reexecucoes"],
            "resultado_final": info["resultado_final"],
        }
        for nodeid, info in sorted(_ESTADO.items())
        if info["reexecucoes"] > 0
    ]


def _instaveis(reexecutados: list[dict]) -> list[dict]:
    return [item for item in reexecutados if item["resultado_final"] == "passed"]


def _gravar_reexecucoes(reexecutados: list[dict]) -> None:
    destino = Path("relatorios")
    destino.mkdir(parents=True, exist_ok=True)
    conteudo = {
        "reruns_configurados": _RERUNS,
        "politica": POLITICA_DE_RETRY,
        "testes_reexecutados": reexecutados,
    }
    (destino / "reexecucoes.json").write_text(
        json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
