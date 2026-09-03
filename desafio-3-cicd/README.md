# Desafio 3 - Integração e CI/CD

Configuração de um pipeline de CI/CD usando **GitHub Actions** que executa
os testes automatizados do repositório a cada `push` ou `pull request`,
gerando o relatório de resultados como artefato da execução.

## Onde fica a configuração

O workflow está em [`.github/workflows/ci.yml`](../.github/workflows/ci.yml),
na raiz do repositório (é onde o GitHub Actions espera encontrar os
workflows, independente de qual desafio ele testa).

## O que o pipeline faz

Dois jobs rodam em paralelo a cada push/PR em qualquer branch, de forma
independente (se um falhar, não impede o outro de terminar):

### `testes-api` (Desafio 1)

1. Faz o checkout do repositório;
2. Configura o Python 3.12 (com cache de pip pra não reinstalar tudo do
   zero em toda execução);
3. Instala as dependências do `desafio-1-teste-api/requirements.txt`;
4. Executa `pytest` contra a BrasilAPI (os 42 testes descritos no
   [Desafio 1](../desafio-1-teste-api/README.md));
5. Gera o relatório HTML (`pytest-html`) e sobe ele como **artefato** da
   execução (`relatorio-testes-api`), mesmo se algum teste falhar.

### `testes-e2e` (Desafio 2)

1. Faz o checkout do repositório;
2. Configura o Python 3.12;
3. Instala as dependências do `desafio-2-teste-e2e/requirements.txt`;
4. Executa `pytest` contra o site de prática automationpratice.com.br
   (os testes de navegação, login e checkout descritos no
   [Desafio 2](../desafio-2-teste-e2e/README.md)), usando o Google Chrome
   que já vem instalado nos runners do GitHub Actions;
5. Gera o relatório HTML e sobe ele como artefato (`relatorio-testes-e2e`).

Em ambos os casos, o relatório sobe como artefato mesmo se algum teste
falhar - assim dá pra abrir o HTML e investigar o motivo sem precisar
rodar nada localmente.

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
   `relatorio-testes-api` e o `relatorio-testes-e2e` pra baixar e abrir o
   HTML com o resultado detalhado de cada teste.

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

O relatório completo (HTML, com todos os 42 testes e headers/corpo de cada
resposta) ficou disponível como artefato `relatorio-testes-api` dessa
execução, baixável direto na página do run no GitHub Actions.
