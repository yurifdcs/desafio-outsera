"""
Configuração compartilhada da suíte de testes E2E.

Aqui só ficam fixtures que "montam" os Page Objects em cima da fixture
`page` que o plugin pytest-playwright já fornece (ele cuida de abrir e
fechar o browser/contexto pra cada teste). A URL base do site já está
configurada no pytest.ini (--base-url), então dentro dos Page Objects a
gente só usa caminhos relativos, tipo page.goto("/login").
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


# o site é uma SPA em React e às vezes demora um pouco mais que o padrão
# do Playwright (5s) pra carregar o "chunk" JS de uma rota nova depois de
# um clique (ex: carrinho -> checkout). Aumento a margem pra não pegar
# falso negativo por lentidão de carregamento, sem exagerar no tempo.
expect.set_options(timeout=10_000)


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
