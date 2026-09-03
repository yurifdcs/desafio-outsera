# Desafio Outsera - Automação de Testes

Repositório com a resolução prática da avaliação de automação de testes.
Cada desafio da avaliação vive na sua própria pasta, com README, código e
evidências próprias.

## Estrutura do repositório

```
DESAFIO_OUTSERA/
├── .github/workflows/ci.yml   # pipeline de CI/CD (Desafio 3)
├── desafio-1-teste-api/       # Desafio 1 - Testes automatizados de API
└── desafio-3-cicd/            # Desafio 3 - Integração e CI/CD
```

## Desafios resolvidos

| Desafio | Pasta | Status |
|---|---|---|
| 1 - Testes Automatizados de API | [`desafio-1-teste-api/`](desafio-1-teste-api/README.md) | ✅ Concluído |
| 2 - Testes End-to-End (E2E) | - | Não implementado ainda |
| 3 - Integração e CI/CD | [`desafio-3-cicd/`](desafio-3-cicd/README.md) | ✅ Concluído (roda o Desafio 1 no pipeline) |
| 4 - Testes de Carga (opcional) | - | Não implementado ainda |
| 5 - Testes Mobile (opcional) | - | Não implementado ainda |

## Desafio 1 - Testes Automatizados de API

Suíte de testes em **Python + Playwright** contra a
[BrasilAPI](https://brasilapi.com.br/), cobrindo cenários positivos e
negativos, múltiplos endpoints e métodos HTTP (GET/POST/PUT/DELETE), com
relatório HTML gerado via `pytest-html`.

Detalhes completos, versões, dependências e como rodar:
[`desafio-1-teste-api/README.md`](desafio-1-teste-api/README.md)

## Desafio 3 - Integração e CI/CD

Pipeline em **GitHub Actions** que roda os testes do Desafio 1 a cada
`push`/`pull request` e publica o relatório como artefato da execução.

Detalhes completos e como acompanhar as execuções:
[`desafio-3-cicd/README.md`](desafio-3-cicd/README.md)
