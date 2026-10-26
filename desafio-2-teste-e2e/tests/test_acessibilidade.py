"""
Acessibilidade das jornadas críticas da loja, com axe-core.

Home, login e checkout. Violação de impacto critical ou serious reprova
o teste. O critério está em `acessibilidade.py`.

O site de prática, hoje, falha nessa barra (contraste, link sem nome,
campo de login sem label). A reprovação é o resultado da auditoria.
"""

import pytest
from playwright.sync_api import expect

from acessibilidade import auditar

pytestmark = pytest.mark.acessibilidade


def test_home_sem_violacoes_relevantes(page, home_page):
    home_page.abrir()
    auditar(page, "home")


def test_login_sem_violacoes_relevantes(page, login_page):
    login_page.abrir()
    auditar(page, "login")


def test_checkout_sem_violacoes_relevantes(page, cart_page):
    cart_page.abrir().ir_para_checkout()
    expect(page.get_by_role("heading", name="Billings Information")).to_be_visible()
    auditar(page, "checkout")
