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

**Acessibilidade** - axe-core na home, no login e no checkout. Violação
critical ou serious reprova.

O site de prática, hoje, não passa nessa barra. A home tem contraste
baixo, link sem nome e elemento escondido que ainda recebe foco. O login
deixa `#user` e `#password` sem label (impacto critical). O checkout
repete contraste e link sem nome. Esses três testes reprovam de propósito:
a violação relevante é falha da suíte. Navegação, login e checkout
funcionais continuam verdes no outro job.

## Estrutura

desafio-2-teste-e2e/
├── conftest.py # fixtures, screenshot na falha e política de retry
├── config.py # E2E_BASE_URL e E2E_RERUNS
├── acessibilidade.py # axe-core, corte por impacto
├── pytest.ini # browser, screenshot e trace (sem URL e sem rerun global)
├── requirements.txt
├── pages/ # Page Objects (um por tela)
├── tests/ # navegação, login, checkout e acessibilidade
└── relatorios/ # relatório, e evidências quando algo falha


## Como rodar

A URL do site não fica no `pytest.ini`. Exporte `E2E_BASE_URL` ou copie o exemplo:

```bash
cd desafio-2-teste-e2e
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# ou: export E2E_BASE_URL=https://automationpratice.com.br

pytest -v --html=relatorios/relatorio.html --self-contained-html
```

Usa o Chrome instalado no sistema (`--browser-channel chrome` no
`pytest.ini`). Pra usar o Chromium do Playwright, rode
`playwright install chromium` e tire essa flag.

Pra filtrar por tipo de teste:

```bash
pytest -m positivo
pytest -m negativo
pytest -m "not acessibilidade"
pytest -m acessibilidade
```

## Acessibilidade

`tests/test_acessibilidade.py` abre home, login e checkout e roda o
axe-core na página. Violação de impacto `critical` ou `serious` reprova
o teste. Moderate e minor aparecem no texto da falha só como contexto.

O motor é o axe empacotado em `axe-playwright-python` (não baixa o script
de um CDN na hora do teste).

## Evidência quando um cenário falha

O `pytest.ini` liga `--screenshot=only-on-failure` e
`--tracing=retain-on-failure`. Os arquivos vão para
`relatorios/evidencias/<cenário>/` (`test-failed-1.png` e `trace.zip`).
O relatório HTML também embute o screenshot.

Pra abrir o trace:

```bash
playwright show-trace relatorios/evidencias/<cenário>/trace.zip
```

Na pipeline esses arquivos sobem como artefato mesmo se o job falhar.

## Retry

Não existe `--reruns` global. O padrão é `E2E_RERUNS=0`: falhou, falhou.
Se a variável for maior que zero, o pytest-rerunfailures repete o teste,
o log ganha uma seção "Estratégia de retry" listando quem foi
reexecutado, e um teste que só passa na retentativa reprova a sessão.
O arquivo `relatorios/reexecucoes.json` leva essa lista para o resumo da
pipeline. A ideia é não deixar uma instabilidade passar verde.