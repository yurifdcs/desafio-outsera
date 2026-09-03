"""
Testes do fluxo de checkout.

Caminho feliz: preencher os dados de cobrança, salvar (botão "Save") e só
depois clicar em "Place Order" -> pedido concluído com sucesso.

Achei essa ordem (salvar antes de finalizar) testando manualmente: se você
clica direto em "Place Order" sem ter salvo os dados antes, o site sempre
devolve a mensagem de erro "Preencha os dados de pagamento!", mesmo com
todos os campos preenchidos corretamente. Isso é ótimo pra virar o nosso
cenário negativo, porque é 100% reproduzível.
"""

import re

import pytest
from playwright.sync_api import expect


@pytest.mark.positivo
def test_checkout_completo_com_sucesso(page, cart_page, checkout_page):
    cart_page.abrir().ir_para_checkout()

    checkout_page.preencher_dados_de_cobranca(
        primeiro_nome="Maria",
        ultimo_nome="Silva",
        empresa="Empresa Teste",
        email="maria.silva@teste.com",
        cep="12345678",
        endereco="Rua Teste, 123",
        observacoes="Entregar no período da tarde",
    )
    checkout_page.salvar_dados_de_cobranca()
    checkout_page.finalizar_pedido()

    checkout_page.confirmar_modal_pedido_realizado()


@pytest.mark.negativo
def test_finalizar_pedido_sem_salvar_dados_mostra_erro(page, cart_page, checkout_page):
    cart_page.abrir().ir_para_checkout()

    # preenche tudo certinho, mas NÃO clica em "Save" antes - de propósito
    checkout_page.preencher_dados_de_cobranca(
        primeiro_nome="Maria",
        ultimo_nome="Silva",
        empresa="Empresa Teste",
        email="maria.silva@teste.com",
        cep="12345678",
        endereco="Rua Teste, 123",
    )
    checkout_page.finalizar_pedido()

    expect(checkout_page.mensagem_erro_pagamento).to_be_visible()
    # continua na tela de checkout, o pedido não foi concluído
    expect(page).to_have_url(re.compile("checkout-one"))


@pytest.mark.negativo
def test_finalizar_pedido_com_formulario_vazio_mostra_erro(page, cart_page, checkout_page):
    cart_page.abrir().ir_para_checkout()

    # nem tenta preencher nada, vai direto no botão
    checkout_page.finalizar_pedido()

    expect(checkout_page.mensagem_erro_pagamento).to_be_visible()
