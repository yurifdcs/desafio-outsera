"""
Configuração compartilhada da suíte de testes.

A URL base não fica neste arquivo. O fixture `api` aponta para
API_BASE_URL e o `api_crud` para CRUD_API_BASE_URL (variável de ambiente
ou `.env` local). Ver `.env.example`.
"""

import pytest
from playwright.sync_api import Playwright

from config import url_obrigatoria


@pytest.fixture(scope="session")
def api(playwright: Playwright):
    """Contexto HTTP da API de consulta, reutilizado na sessão."""
    contexto = playwright.request.new_context(base_url=url_obrigatoria("API_BASE_URL"))
    yield contexto
    contexto.dispose()


@pytest.fixture(scope="session")
def api_crud(playwright: Playwright):
    """Contexto HTTP da API que persiste recurso (criação, atualização, remoção)."""
    contexto = playwright.request.new_context(base_url=url_obrigatoria("CRUD_API_BASE_URL"))
    yield contexto
    contexto.dispose()
