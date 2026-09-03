# Desafio 1 - Testes Automatizados de API (BrasilAPI)

Suíte de testes automatizados construída em Python + Playwright para validar
endpoints públicos da [BrasilAPI](https://brasilapi.com.br/). A ideia da
avaliação era usar Rest Assured, Cypress ou Playwright para testar uma API de
exemplo cobrindo cenários positivos e negativos, com diferentes métodos HTTP
e relatório final - foi exatamente esse o escopo seguido aqui.

## Por que a BrasilAPI

A BrasilAPI é pública, não exige autenticação/token e tem endpoints simples
de validar (CEP, bancos, DDD, feriados, câmbio), o que facilita montar
cenários de teste realistas sem depender de nenhum ambiente próprio no ar.
Um detalhe interessante: como é uma API só de consulta (GET), ela também dá
material de sobra para os cenários negativos de método HTTP não suportado
pedidos na Tarefa 2 (POST/PUT/DELETE nesses endpoints devem falhar).

## Por que Playwright para testar API

O Playwright é mais conhecido pelo lado de automação de navegador, mas ele
também tem um cliente HTTP embutido (`APIRequestContext`, acessível via
`playwright.request`) que serve exatamente para esse tipo de teste: fazer
chamadas GET/POST/PUT/DELETE direto contra uma API e validar status code,
headers e corpo da resposta, sem precisar subir nenhum navegador. É esse
recurso que a suíte usa do início ao fim.

## Endpoints cobertos

| Endpoint | Método(s) testado(s) | O que valida |
|---|---|---|
| `/api/cep/v1/{cep}` | GET (+ POST/PUT/DELETE negativos) | Consulta de endereço por CEP |
| `/api/banks/v1` e `/api/banks/v1/{code}` | GET (+ POST/PUT/DELETE negativos) | Lista de bancos e busca por código |
| `/api/ddd/v1/{ddd}` | GET (+ POST/PUT/DELETE negativos) | Estado e cidades atendidas por um DDD |
| `/api/feriados/v1/{ano}` | GET (+ POST/PUT/DELETE negativos) | Feriados nacionais de um ano |
| `/api/cambio/v1/moedas` e `/api/cambio/v1/cotacao/{moeda}/{data}` | GET | Cotação de moedas estrangeiras |

## Arquitetura / estrutura de pastas

```
desafio-1-teste-api/
├── conftest.py              # fixture "api" (contexto de requisição HTTP do Playwright)
├── pytest.ini                # configuração do pytest (paths, markers)
├── requirements.txt           # dependências do projeto
├── tests/
│   ├── test_cep.py            # Tarefa 1 - endpoint de CEP (positivo/negativo)
│   ├── test_bancos.py         # Tarefa 1 - endpoint de bancos (positivo/negativo)
│   ├── test_ddd.py            # Tarefa 1 - endpoint de DDD (positivo/negativo)
│   ├── test_feriados.py       # Tarefa 1 - endpoint de feriados (positivo/negativo)
│   ├── test_cambio.py         # Tarefa 1 - endpoint de câmbio (positivo/negativo)
│   └── test_metodos_http.py   # Tarefa 2 - GET/POST/PUT/DELETE, payload malformado e dados ausentes
└── relatorios/
    └── relatorio.html         # relatório HTML gerado na última execução (evidência)
```

Cada arquivo de teste segue o mesmo padrão: uma classe `*Positivo` com os
cenários de sucesso e uma `*Negativo` com formato inválido, recurso
inexistente, parâmetro ausente, etc. O `test_metodos_http.py` é o que cobre
especificamente a Tarefa 2, testando os mesmos endpoints com os quatro
verbos HTTP.

## O que cada arquivo faz

- **`conftest.py`** - configuração compartilhada da suíte. É aqui que fica o
  fixture `api`, que cria (uma única vez por sessão) o contexto de
  requisições HTTP do Playwright já apontando para `https://brasilapi.com.br`.
  Todo teste que recebe `api` como parâmetro reaproveita esse mesmo contexto.
- **`pytest.ini`** - configuração do pytest: onde ficam os testes
  (`tests/`), o padrão de nome de arquivo/classe/função que ele deve
  reconhecer como teste, e a declaração dos markers `positivo`/`negativo`
  (usados só como referência de organização dos cenários).
- **`requirements.txt`** - lista travada (com versão exata) de tudo que
  precisa estar instalado pra rodar o projeto: `playwright`, `pytest`,
  `pytest-playwright` (integração entre os dois) e `pytest-html` (gerador
  do relatório).
- **`.gitignore`** - evita que ambiente virtual (`venv/`), cache do pytest
  (`.pytest_cache/`) e bytecode do Python (`__pycache__/`, `*.pyc`) sejam
  versionados. Nenhum desses é código do projeto, então não faz sentido
  subir pro repositório.
- **`README.md`** - este arquivo.
- **`tests/test_cep.py`** - Tarefa 1: valida o endpoint de CEP. Cenário
  positivo com um CEP existente (status, headers e campos do endereço) e
  negativos com CEP fora do padrão de 8 dígitos, CEP inexistente e
  requisição sem informar o CEP.
- **`tests/test_bancos.py`** - Tarefa 1: valida a listagem de bancos e a
  busca por código. Positivo cobre a lista completa e a busca pelo Banco do
  Brasil (código 1); negativo cobre código inexistente e código não numérico.
- **`tests/test_ddd.py`** - Tarefa 1: valida a consulta de DDD. Positivo com
  o DDD 11 (retorna SP e a lista de cidades); negativo com DDDs em formatos
  inválidos (curto demais, longo demais, não numérico).
- **`tests/test_feriados.py`** - Tarefa 1: valida os feriados nacionais de
  um ano. Positivo confere a quantidade e os dados do feriado de Ano Novo em
  2025; negativo cobre ano fora do intervalo suportado pela API e ano não
  numérico (que gera erro 500 - comportamento documentado no próprio teste).
- **`tests/test_cambio.py`** - Tarefa 1: valida a cotação de moedas.
  Positivo confere a lista de moedas disponíveis e a cotação do dólar numa
  data válida; negativo cobre moeda inexistente e data em formato errado.
- **`tests/test_metodos_http.py`** - Tarefa 2: bate nos mesmos endpoints
  usados nos outros arquivos, mas focando nos métodos HTTP. Confirma que o
  `GET` funciona em todos eles e que `POST`, `PUT` e `DELETE` são rejeitados
  (já que a BrasilAPI só expõe consulta). Também cobre payload malformado
  (JSON quebrado no corpo de um `POST`) e requisição sem o parâmetro
  obrigatório na URL.
- **`relatorios/relatorio.html`** - relatório HTML gerado pelo `pytest-html`
  na última execução da suíte, guardado como evidência dos testes.

## Versões utilizadas

- Python 3.12.3
- playwright 1.48.0
- pytest 8.3.3
- pytest-playwright 0.5.2
- pytest-html 4.1.1

(as versões exatas de cada dependência ficam travadas no `requirements.txt`)

## Dependências - como instalar

```bash
# a partir da pasta desafio-1-teste-api

# 1. criar e ativar um ambiente virtual
python3 -m venv venv
source venv/bin/activate      # no Windows: venv\Scripts\activate

# 2. instalar as dependências do projeto
pip install -r requirements.txt
```

Não é necessário rodar `playwright install` aqui - a suíte usa somente o
cliente de requisições HTTP do Playwright, não abre navegador nenhum, então
os binários de browser não fazem falta.

## Como executar os testes

```bash
# executa a suíte inteira
pytest

# com mais detalhes no console
pytest -v

# rodando só um arquivo específico
pytest tests/test_cep.py -v
```

## Como gerar o relatório

```bash
pytest --html=relatorios/relatorio.html --self-contained-html
```

Isso gera um relatório HTML autocontido (não depende de arquivos externos)
em `relatorios/relatorio.html`, com o resultado de cada teste, tempo de
execução e o motivo de qualquer falha. Basta abrir o arquivo em qualquer
navegador para consultar. O relatório da última execução já está commitado
nessa pasta como evidência.

## Observações sobre alguns cenários

- **CEP inexistente vs. formato inválido**: a API separa bem os dois casos -
  formato errado (não tem 8 dígitos) devolve `400`, já um CEP com formato
  válido mas que não existe em nenhuma base devolve `404`. Os testes cobrem
  as duas situações separadamente.
- **Métodos não suportados**: como a BrasilAPI só expõe consulta (GET) nos
  endpoints usados aqui, POST/PUT/DELETE devolvem `404` (rota não
  encontrada). Isso é usado de propósito como cenário negativo da Tarefa 2.
- **Payload malformado**: ao montar o corpo de uma requisição malformada com
  o Playwright, é preciso passar `data` como `bytes` (não como `str`) quando
  o `Content-Type` é `application/json`. Se for passada uma string comum,
  o Playwright entende que o valor deve virar uma string JSON válida e a
  serializa colocando aspas ao redor - o que evitaria justamente o cenário
  de erro que o teste quer reproduzir. Isso está comentado no próprio código
  do teste (`test_metodos_http.py`).
- **`/api/feriados/v1/abc`**: um ano não numérico faz a API estourar um erro
  `500` em vez de um `400` mais amigável. Não é o comportamento mais
  elegante, mas é o que a API realmente faz hoje, então o teste documenta
  esse comportamento em vez de simplesmente ignorá-lo.
