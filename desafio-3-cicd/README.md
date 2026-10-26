# Desafio 3 - Integração e CI/CD

Configuração de um pipeline de CI/CD usando **GitHub Actions** que executa
os testes automatizados do repositório a cada `push` ou `pull request`,
gerando o relatório de resultados como artefato da execução.

## Onde fica a configuração

O workflow está em [`.github/workflows/ci.yml`](../.github/workflows/ci.yml),
na raiz do repositório (é onde o GitHub Actions espera encontrar os
workflows, independente de qual desafio ele testa).

## O que o pipeline faz

Quatro jobs rodam em paralelo a cada push/PR. O quinto espera os quatro e
publica o resumo. Se um job de teste falha, os outros continuam, e o
quality gate ainda roda.

As URLs não estão nos testes. O workflow define `API_BASE_URL`,
`CRUD_API_BASE_URL` e `E2E_BASE_URL`. Numa execução manual
(`workflow_dispatch`) dá para trocar esses três valores no formulário.

`E2E_RERUNS` fica em `0`. Não há retry global no E2E.

### `qualidade-codigo`

Roda `ruff check` e `ruff format --check` na suíte de API, na suíte E2E
e no script de resumo.

### `testes-api` (Desafio 1)

1. Faz o checkout do repositório;
2. Configura o Python 3.12 (com cache de pip);
3. Instala as dependências do `desafio-1-teste-api/requirements.txt`;
4. Executa `pytest` contra a API de consulta e o fluxo de CRUD;
5. Gera o HTML (`pytest-html`) e o `junit.xml`;
6. Sobe os dois como artefato `resultado-api`, mesmo se algum teste falhar.

### `testes-e2e` (Desafio 2)

1. Faz o checkout do repositório;
2. Configura o Python 3.12;
3. Instala as dependências do `desafio-2-teste-e2e/requirements.txt`;
4. Executa os testes funcionais (`-m "not acessibilidade"`) no Chrome
   que já vem no runner;
5. Sobe HTML, JUnit, `reexecucoes.json` e, se algum cenário falhou,
   screenshot e `trace.zip` em `relatorios/evidencias/` como artefato
   `resultado-e2e`.

### `testes-acessibilidade`

Roda só os três cenários de axe (home, login e checkout). Violação
critical ou serious reprova o job. Screenshot e trace da falha sobem no
artefato `resultado-acessibilidade`.

Esse job fica vermelho com o site de prática no estado atual: há
violação séria nas três jornadas (e critical no login, campo sem label).
Os testes funcionais de navegação, login e checkout não entram aqui e
seguem no job `testes-e2e`.

### `resumo` (quality gate)

Junta os JUnit e o relatório de reexecução e grava um markdown com:

- total, aprovados, reprovados, ignorados e duração;
- status de cada módulo (CEP, login, acessibilidade, …);
- status de cada job;
- quais testes precisaram ser reexecutados.

O job sai com erro se algum teste reprovou, se algum job não passou, ou
se um teste só ficou verde depois de retry. O markdown também vai para
o resumo da execução no GitHub Actions e para o artefato `resumo-execucao`.

Em todos os casos, relatório e evidência sobem mesmo se o teste falhar.

## Por que o job mobile ainda não roda de fato

O desafio pede uma pipeline que rode testes de API, E2E e mobile. Neste
repositório, os desafios 1 (API) e 2 (E2E) já estão implementados, mas o
**Desafio 5 (mobile)** ainda não.

Em vez de fingir que esse teste existe, o workflow já deixa o job
`testes-mobile` descrito no arquivo, desligado com `if: false` e com um
comentário explicando que ele entra quando o desafio correspondente for
implementado. Isso cobre a parte do enunciado que permite "descrever ou
configurar" o pipeline - a estrutura pros três tipos de teste já está
montada.

## Como ver o resultado das execuções

Depois que o repositório está no GitHub, dá pra acompanhar cada execução
na aba **Actions** do repositório:

1. Abra a aba `Actions` no GitHub;
2. Clique na execução mais recente do workflow `CI - Testes Automatizados`;
3. O status de cada step aparece ali (verde = passou, vermelho = falhou);
4. Em **Artifacts**, no final da página da execução, tem o
   `resultado-api`, o `resultado-e2e`, o `resultado-acessibilidade` e o
   `resumo-execucao`. O resumo também aparece no bloco **Summary** da
   execução.

## Resultado da última execução

> Esta seção é atualizada manualmente depois de cada publicação, com o
> link e o resultado real da execução no GitHub Actions.

| Execução | Branch | Resultado | Duração | Link |
|---|---|---|---|---|
| #33803180026 (primeira publicação) | `master` | ✅ 42 testes passaram | 12,12s | [ver execução](https://github.com/yurifdcs/desafio-outsera/actions/runs/33803180026) |

Saída do step "Rodar os testes e gerar o relatório" nessa execução:

```
============================= test session starts ==============================
tests/test_bancos.py::TestBancosPositivo::test_lista_completa_de_bancos PASSED
tests/test_bancos.py::TestBancosPositivo::test_banco_do_brasil_pelo_codigo_1 PASSED
tests/test_cambio.py::TestCambioPositivo::test_lista_de_moedas_disponiveis_inclui_dolar_e_euro PASSED
tests/test_cep.py::TestCepPositivo::test_busca_por_cep_valido_retorna_200_e_json PASSED
tests/test_ddd.py::TestDddPositivo::test_ddd_11_retorna_estado_sp_e_lista_de_cidades PASSED
tests/test_feriados.py::TestFeriadosPositivo::test_feriados_de_2025_vem_completos PASSED
tests/test_metodos_http.py::TestMetodosNaoSuportados::test_post_nao_e_suportado[...] PASSED
... (42 testes no total, cobrindo os 5 endpoints e os cenários positivos/negativos)
============================= 42 passed in 12.12s ==============================
```

O relatório completo (HTML) ficou disponível como artefato dessa
execução. A partir da rodada seguinte, o artefato passa a se chamar
`resultado-api` e o resumo consolidado sai no job `resumo`.
