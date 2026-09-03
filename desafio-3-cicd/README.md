# Desafio 3 - Integração e CI/CD

Configuração de um pipeline de CI/CD usando **GitHub Actions** que executa
os testes automatizados do repositório a cada `push` ou `pull request`,
gerando o relatório de resultados como artefato da execução.

## Onde fica a configuração

O workflow está em [`.github/workflows/ci.yml`](../.github/workflows/ci.yml),
na raiz do repositório (é onde o GitHub Actions espera encontrar os
workflows, independente de qual desafio ele testa).

## O que o pipeline faz

O job `testes-api` roda a cada push/PR em qualquer branch:

1. Faz o checkout do repositório;
2. Configura o Python 3.12 (com cache de pip pra não reinstalar tudo do
   zero em toda execução);
3. Instala as dependências do `desafio-1-teste-api/requirements.txt`;
4. Executa `pytest` contra a BrasilAPI (os 42 testes descritos no
   [Desafio 1](../desafio-1-teste-api/README.md));
5. Gera o relatório HTML (`pytest-html`) e sobe ele como **artefato** da
   execução (`relatorio-testes-api`), mesmo se algum teste falhar - assim
   dá pra abrir o HTML e investigar o motivo sem precisar rodar nada
   localmente.

## Por que só o job de API está rodando de fato

O desafio pede uma pipeline que rode testes de API, E2E e mobile. Neste
repositório, até agora, só o **Desafio 1 (testes de API)** foi
implementado - os desafios 2 (E2E) e 5 (mobile) ainda não existem aqui.

Em vez de fingir que esses testes existem, o workflow já deixa os jobs
`testes-e2e` e `testes-mobile` descritos no arquivo, desligados com
`if: false` e com um comentário explicando que entram quando os desafios
correspondentes forem implementados. Isso cobre a parte do enunciado que
permite "descrever ou configurar" o pipeline - a estrutura para os três
tipos de teste já está montada, rodando em paralelo e de forma
independente (falha de um job não impede o outro de rodar).

## Como ver o resultado das execuções

Depois que o repositório está no GitHub, dá pra acompanhar cada execução
na aba **Actions** do repositório:

1. Abra a aba `Actions` no GitHub;
2. Clique na execução mais recente do workflow `CI - Testes Automatizados`;
3. O status de cada step aparece ali (verde = passou, vermelho = falhou);
4. Em **Artifacts**, no final da página da execução, tem o
   `relatorio-testes-api` pra baixar e abrir o HTML com o resultado
   detalhado de cada teste.

## Resultado da última execução

> Esta seção é atualizada manualmente depois de cada publicação, com o
> link e o resultado real da execução no GitHub Actions.

| Execução | Branch | Resultado | Link |
|---|---|---|---|
| _(preenchido após a primeira publicação no GitHub)_ | `master` | - | - |
