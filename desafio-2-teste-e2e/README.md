# Desafio 2 - Testes End-to-End (E2E)

Suíte de testes E2E em **Python + Playwright + Pytest** contra o site de
prática [automationpratice.com.br](https://automationpratice.com.br/), um
e-commerce fake (QAZANDO Shop) feito especificamente pra treinar automação.

O objetivo do desafio era cobrir uma navegação simples: caminho feliz +
alguns testes negativos básicos. Não fui atrás de cobrir 100% do site (não
era o pedido), só os fluxos principais: navegação, login e checkout.

## O que é testado

### Navegação (`tests/test_navegacao.py`)
- Home carrega com o título certo.
- Dá pra ir da home até a página de um produto.
- Dá pra ir até o carrinho (que já vem com uns itens de exemplo
  pré-carregados nesse site de prática).
- Dá pra ir do carrinho até a tela de checkout.

### Login (`tests/test_login.py`)
- **Caminho feliz:** e-mail em formato válido + senha qualquer → login
  funciona e redireciona pra `/my-account`.
- **Negativos:** e-mail vazio ou sem "@" → mensagem "E-mail inválido.";
  senha vazia → mensagem "Senha inválida.".

Vale registrar uma descoberta ao explorar o site: esse mock de login **não
valida a senha de verdade**. Qualquer senha não-vazia passa, desde que o
e-mail tenha formato válido. Por isso não existe teste de "senha errada" -
esse cenário simplesmente não existe nesse app.

### Checkout (`tests/test_checkout.py`)
- **Caminho feliz:** preencher os dados de cobrança, clicar em "Save"
  (que confirma "Billings Information registred with success!") e só
  depois clicar em "Place Order" → modal "Order success!".
- **Negativos:** clicar em "Place Order" sem ter salvo os dados antes
  (mesmo com tudo preenchido) ou com o formulário vazio → mensagem
  "Preencha os dados de pagamento!".

Essa ordem "salvar antes de finalizar" não é óbvia por documentação
nenhuma - só descobri testando manualmente o site no navegador antes de
escrever os testes.

## Arquivos do projeto

```
desafio-2-teste-e2e/
├── conftest.py            # fixtures dos Page Objects + timeout global do expect
├── pytest.ini             # config do pytest (browser, base-url, reruns, markers)
├── requirements.txt       # dependências Python
├── .gitignore
├── pages/                 # Page Objects (um por tela do site)
│   ├── home_page.py
│   ├── login_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_navegacao.py
│   ├── test_login.py
│   └── test_checkout.py
└── relatorios/
    └── relatorio.html     # relatório da última execução (evidência)
```

## Como rodar

```bash
cd desafio-2-teste-e2e
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# usa o Google Chrome instalado no sistema (--browser-channel chrome no
# pytest.ini), então não precisa rodar "playwright install" pra baixar
# o Chromium embutido - útil em ambientes onde esse download é bloqueado.
# Se preferir usar o Chromium do próprio Playwright, é só rodar
# "playwright install chromium" e remover a flag --browser-channel do
# pytest.ini.

pytest -v --html=relatorios/relatorio.html --self-contained-html
```

Pra rodar só os testes positivos ou só os negativos:

```bash
pytest -m positivo
pytest -m negativo
```

## Sobre a estabilidade dos testes

Isso aqui testa um site de terceiros de verdade, não um mock local - então
de vez em quando uma imagem demora a carregar ou a rede engasga por um
instante (a SPA em React carrega os "chunks" JS de cada rota sob demanda).
Pra não deixar o pipeline vermelho por uma lentidão pontual, o
`pytest.ini` usa `--reruns 2 --reruns-delay 2`, que tenta de novo
automaticamente antes de considerar o teste como falho de fato. É uma
prática comum em E2E contra ambientes que a gente não controla.
