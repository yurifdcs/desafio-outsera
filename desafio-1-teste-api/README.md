# Desafio 1 - Testes Automatizados de API (BrasilAPI)

Suíte de testes de API em Python + Playwright contra os endpoints públicos da
[BrasilAPI](https://brasilapi.com.br/), cobrindo cenários positivos, negativos
e métodos HTTP.

Escolhi a BrasilAPI por ser pública, sem token e fácil de validar. Como ela é
só de consulta (GET), POST/PUT/DELETE já servem de cenário negativo pronto.

Usei o cliente HTTP embutido do Playwright (`APIRequestContext`), que faz as
requisições e valida status, headers e corpo da resposta sem abrir navegador.

## Endpoints cobertos

| Endpoint | Métodos | O que valida |
|---|---|---|
| `/api/cep/v1/{cep}` | GET (+ POST/PUT/DELETE negativos) | Endereço por CEP |
| `/api/banks/v1` e `/api/banks/v1/{code}` | GET (+ negativos) | Lista de bancos e busca por código |
| `/api/ddd/v1/{ddd}` | GET (+ negativos) | Estado e cidades de um DDD |
| `/api/feriados/v1/{ano}` | GET (+ negativos) | Feriados nacionais do ano |
| `/api/cambio/v1/moedas` e `/cotacao/{moeda}/{data}` | GET | Cotação de moedas |

## Estrutura
desafio-1-teste-api/
├── conftest.py # fixture "api" (contexto HTTP do Playwright)
├── pytest.ini # config do pytest e markers positivo/negativo
├── requirements.txt
├── tests/ # um arquivo por endpoint + test_metodos_http.py
└── relatorios/ # relatório da última execução


Cada arquivo tem uma classe `*Positivo` e uma `*Negativo`. O
`test_metodos_http.py` cobre os quatro verbos, payload malformado e parâmetro
ausente.

## Como rodar

```bash
cd desafio-1-teste-api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

pytest -v

# com relatório HTML
pytest --html=relatorios/relatorio.html --self-contained-html
```

Não precisa de `playwright install` - a suíte não abre navegador.

## Observações

- **CEP**: formato inválido devolve `400`; CEP válido mas inexistente devolve
  `404`. Testei os dois separados.
- **Métodos não suportados**: POST/PUT/DELETE devolvem `404` (rota não
  encontrada), já que os endpoints são só de consulta.
- **Payload malformado**: no Playwright o `data` precisa ir como `bytes`, senão
  ele serializa a string como JSON válido e o cenário de erro se perde.
- **`/api/feriados/v1/abc`**: ano não numérico estoura `500` em vez de `400`.
  Preferi documentar no teste em vez de ignorar.
