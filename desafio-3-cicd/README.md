# Desafio 3 - Integração e CI/CD

Pipeline no **GitHub Actions** que roda os testes automatizados do
repositório a cada `push` ou `pull request`, e sobe o relatório HTML como
artefato da execução.

O workflow fica em [`.github/workflows/ci.yml`](../.github/workflows/ci.yml),
na raiz do repo (é onde o Actions espera encontrar).

## O que roda

Dois jobs em paralelo, independentes (se um falhar, o outro segue):

- **`testes-api`** - roda os testes do
  [Desafio 1](../desafio-1-teste-api/README.md) contra a BrasilAPI.
- **`testes-e2e`** - roda os testes do
  [Desafio 2](../desafio-2-teste-e2e/README.md) contra o
  automationpratice.com.br, usando o Chrome que já vem nos runners.

Os dois usam Python 3.12 com cache de pip, e sobem o relatório HTML como
artefato (`relatorio-testes-api` e `relatorio-testes-e2e`) mesmo quando algum
teste falha - assim dá pra investigar sem rodar nada local.


## Resultado da última execução

Atualizado manualmente a cada publicação.

| Execução | Branch | Resultado | Duração | Link |
|---|---|---|---|---|
| #33803180026 | `master` | ✅ 42 testes passaram | 12,12s | [ver execução](https://github.com/yurifdcs/desafio-outsera/actions/runs/33803180026) |

O relatório completo fica como artefato na página do run, na aba **Actions**.
