"""
Tarefa 2 - cobertura de múltiplos endpoints usando diferentes métodos HTTP.

Um detalhe importante da BrasilAPI: ela é uma API só de consulta, então
nenhum dos endpoints abaixo aceita POST, PUT ou DELETE de verdade. Em vez de
isso ser um problema pros testes, a gente usa exatamente esse comportamento
como cenário negativo - o esperado é que a API rejeite esses métodos, e é
isso que validamos aqui, junto com payload malformado e requisição sem os
dados obrigatórios.
"""

import pytest

ENDPOINTS = [
    "/api/cep/v1/01310930",
    "/api/banks/v1/1",
    "/api/ddd/v1/11",
    "/api/feriados/v1/2025",
]


class TestMetodoGet:
    """O único verbo que esses endpoints realmente suportam."""

    @pytest.mark.parametrize("endpoint", ENDPOINTS)
    def test_get_responde_200_com_json_em_todos_os_endpoints(self, api, endpoint):
        resposta = api.get(endpoint)

        assert resposta.status == 200
        assert "application/json" in resposta.headers["content-type"]
        assert resposta.json()  # corpo não pode vir vazio


class TestMetodosNaoSuportados:
    """POST, PUT e DELETE não existem pra esses recursos - tem que dar erro."""

    @pytest.mark.parametrize("endpoint", ENDPOINTS)
    def test_post_nao_e_suportado(self, api, endpoint):
        resposta = api.post(endpoint)
        assert resposta.status == 404

    @pytest.mark.parametrize("endpoint", ENDPOINTS)
    def test_put_nao_e_suportado(self, api, endpoint):
        resposta = api.put(endpoint)
        assert resposta.status == 404

    @pytest.mark.parametrize("endpoint", ENDPOINTS)
    def test_delete_nao_e_suportado(self, api, endpoint):
        resposta = api.delete(endpoint)
        assert resposta.status == 404


class TestPayloadMalformadoEDadosAusentes:
    def test_post_com_json_quebrado_no_corpo_retorna_400(self, api):
        # atenção: o "data" precisa ir em bytes aqui. Se mandar como string
        # comum o Playwright entende que é um valor de texto e serializa
        # como um JSON válido (colocando aspas em volta), o que estragaria
        # o propósito do teste - a ideia é mandar um corpo realmente quebrado
        resposta = api.post(
            "/api/banks/v1",
            headers={"Content-Type": "application/json"},
            data=b"{isso aqui nao fecha certinho",
        )

        assert resposta.status == 400

    def test_get_sem_o_parametro_obrigatorio_nao_retorna_sucesso(self, api):
        # tira o CEP da URL e sobra só a rota base - não tem como funcionar
        resposta = api.get("/api/cep/v1/", max_redirects=0)

        assert resposta.status != 200
