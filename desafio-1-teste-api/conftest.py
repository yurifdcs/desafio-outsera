"""
Configuração compartilhada da suíte de testes.

A ideia aqui é simples: em vez de usar o Playwright para controlar um
navegador (que é o uso mais comum da ferramenta), usamos o recurso de
"API testing" dele, o `request.new_context()`, que permite fazer chamadas
HTTP puras (GET, POST, PUT, DELETE...) sem precisar abrir nenhuma página.

Isso deixa os testes bem mais rápidos do que se a gente subisse um browser
só pra bater numa API.
"""

import pytest

BASE_URL = "https://brasilapi.com.br"


@pytest.fixture(scope="session")
def api(playwright):
    """Contexto de requisição HTTP reutilizado em toda a sessão de testes.

    O fixture `playwright` já é fornecido pelo plugin pytest-playwright.
    """
    contexto = playwright.request.new_context(base_url=BASE_URL)

    yield contexto

    contexto.dispose()
