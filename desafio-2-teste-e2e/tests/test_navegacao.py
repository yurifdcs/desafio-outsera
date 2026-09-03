"""
Testes de navegação simples pelo site.

A ideia aqui não é testar regra de negócio, é só garantir que o caminho
"normal" de navegação de um cliente funciona: abrir a home, entrar num
produto, ir pro carrinho e chegar até a tela de checkout. Sem clicar em
"finalizar pedido" ainda - isso fica pros testes de checkout.
"""

import re

import pytest
from playwright.sync_api import expect


@pytest.mark.positivo
def test_home_carrega_com_titulo_correto(page, home_page):
    home_page.abrir()

    expect(page).to_have_title("QAZANDO Shop E-Commerce")
    # os links do topo do site precisam estar visíveis pra navegação funcionar
    expect(page.get_by_role("link", name="Login").first).to_be_visible()
    expect(page.get_by_role("link", name="Cadastro").first).to_be_visible()


@pytest.mark.positivo
def test_navegar_da_home_ate_o_produto(page, home_page, product_page):
    # uso um produto que só aparece na grade principal (não repete no
    # mini-carrinho/wishlist do cabeçalho), pra evitar clicar num link
    # que está escondido fora da tela nesses widgets
    home_page.abrir().abrir_produto("Movie Projector HD Outdoor")

    expect(page).to_have_url(re.compile("product-details"))
    product_page.esperar_carregar("Movie Projector HD Outdoor")


@pytest.mark.positivo
def test_navegar_ate_o_carrinho(page, cart_page):
    # o carrinho desse site de prática já vem com alguns itens de exemplo
    # pré-carregados, então dá pra verificar a listagem sem precisar
    # adicionar nada antes
    cart_page.abrir()

    expect(page).to_have_url(re.compile(r"/cart$"))
    expect(cart_page.tem_produto("Fit-Flare Dress")).to_be_visible()
    expect(cart_page.tem_produto("Midi Dress")).to_be_visible()
    expect(cart_page.tem_produto("Tulip Dress")).to_be_visible()


@pytest.mark.positivo
def test_ir_do_carrinho_para_o_checkout(page, cart_page, checkout_page):
    cart_page.abrir().ir_para_checkout()

    expect(page).to_have_url(re.compile("checkout-one"))
    expect(page.get_by_role("heading", name="Billings Information")).to_be_visible()
    expect(page.get_by_role("heading", name="Your Orders")).to_be_visible()
    expect(page.get_by_role("heading", name="Payment")).to_be_visible()
