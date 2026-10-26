"""
Contrato das respostas, em JSON Schema.

Estes cenários não substituem os asserts de conteúdo dos outros arquivos
(CEP da Paulista, Banco do Brasil, DDD 11, feriados de 2025). Eles
repetem o mínimo de status e Content-Type e, em seguida, conferem se o
corpo obedece ao schema em `contratos/`.
"""

import pytest

from contrato import validar_contrato

pytestmark = pytest.mark.contrato

CEP_VALIDO = "01310930"


class TestContratoCep:
    def test_cep_valido_obedece_o_schema(self, api):
        resposta = api.get(f"/api/cep/v1/{CEP_VALIDO}")

        assert resposta.status == 200
        assert "application/json" in resposta.headers["content-type"]
        validar_contrato(resposta.json(), "cep.json")

    def test_cep_fora_do_padrao_obedece_o_schema_de_erro(self, api):
        resposta = api.get("/api/cep/v1/123")

        assert resposta.status == 400
        assert "application/json" in resposta.headers["content-type"]
        validar_contrato(resposta.json(), "erro_cep.json")


class TestContratoBancoDddEFeriados:
    def test_banco_do_brasil_obedece_o_schema(self, api):
        resposta = api.get("/api/banks/v1/1")

        assert resposta.status == 200
        assert "application/json" in resposta.headers["content-type"]
        validar_contrato(resposta.json(), "banco.json")

    def test_ddd_11_obedece_o_schema(self, api):
        resposta = api.get("/api/ddd/v1/11")

        assert resposta.status == 200
        assert "application/json" in resposta.headers["content-type"]
        validar_contrato(resposta.json(), "ddd.json")

    def test_feriados_de_2025_obedecem_o_schema(self, api):
        resposta = api.get("/api/feriados/v1/2025")

        assert resposta.status == 200
        assert "application/json" in resposta.headers["content-type"]
        validar_contrato(resposta.json(), "feriados.json")
