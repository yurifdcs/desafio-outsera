# Desafio 2 - Testes E2E

Suíte de testes E2E em Python + Playwright + Pytest contra o
[automationpratice.com.br](https://automationpratice.com.br/), um e-commerce
fake feito pra treinar automação.

Cobri os fluxos principais (navegação, login e checkout) com caminho feliz e
alguns testes negativos. Não era o objetivo cobrir o site inteiro.

## O que é testado

**Navegação** - home carrega, home → produto, home → carrinho, carrinho →
checkout.

**Login** - e-mail válido + senha qualquer redireciona pra `/my-account`.
Negativos: e-mail vazio ou sem "@" e senha vazia.
Obs.: o site não valida a senha de verdade, então não existe cenário de
"senha errada".

**Checkout** - preencher os dados, clicar em "Save" e depois em "Place Order"
→ modal "Order success!". Negativos: finalizar sem salvar os dados antes, ou
com o formulário vazio.

## Estrutura

desafio-2-teste-e2e/
├── conftest.py # fixtures dos Page Objects
├── pytest.ini # config do pytest
├── requirements.txt
├── pages/ # Page Objects (um por tela)
├── tests/ # testes de navegação, login e checkout
└── relatorios/ # relatório da última execução


## Como rodar

```bash
cd desafio-2-teste-e2e
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

pytest -v --html=relatorios/relatorio.html --self-contained-html
```

Usa o Chrome instalado no sistema (`--browser-channel chrome` no
`pytest.ini`). Pra usar o Chromium do Playwright, rode
`playwright install chromium` e tire essa flag.

Pra filtrar por tipo de teste:

```bash
pytest -m positivo
pytest -m negativo
```
