"""
Testes do fluxo de login.

Caminho feliz: e-mail em formato válido + senha qualquer -> loga e vai
pra /my-account.

Negativos (só o básico, que é o que esse site de prática realmente
valida no client-side):
  - e-mail vazio/sem "@"  -> "E-mail inválido."
  - senha vazia            -> "Senha inválida."

Reforçando: eu testei manualmente e esse mock de login NÃO confere se a
senha está correta - ele só exige que o campo não esteja vazio. Por isso
não existe aqui um teste de "senha errada", já que pra esse app isso não
é um cenário real de erro.
"""

import re

import pytest
from playwright.sync_api import expect


@pytest.mark.positivo
def test_login_com_credenciais_validas_redireciona_para_minha_conta(
    page, login_page
):
    login_page.abrir().logar("teste@teste.com", "teste123")
    login_page.confirmar_modal_de_sucesso()

    expect(page).to_have_url(re.compile("my-account"))


@pytest.mark.negativo
def test_login_sem_preencher_email_mostra_mensagem_de_invalido(page, login_page):
    login_page.abrir().logar("", "qualquersenha")

    expect(login_page.mensagem_invalida).to_have_text("E-mail inválido.")
    # não deve ter saído da tela de login
    expect(page).to_have_url(re.compile(r"/login$"))


@pytest.mark.negativo
def test_login_com_email_sem_arroba_mostra_mensagem_de_invalido(page, login_page):
    login_page.abrir().logar("emailsemarroba", "qualquersenha")

    expect(login_page.mensagem_invalida).to_have_text("E-mail inválido.")
    expect(page).to_have_url(re.compile(r"/login$"))


@pytest.mark.negativo
def test_login_sem_preencher_senha_mostra_mensagem_de_invalido(page, login_page):
    login_page.abrir().logar("alguem@teste.com", "")

    expect(login_page.mensagem_invalida).to_have_text("Senha inválida.")
    expect(page).to_have_url(re.compile(r"/login$"))
