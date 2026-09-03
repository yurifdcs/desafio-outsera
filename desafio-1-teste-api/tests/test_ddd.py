"""Testes do endpoint de DDD: GET /api/ddd/v1/{ddd}"""

import pytest


class TestDddPositivo:
    def test_ddd_11_retorna_estado_sp_e_lista_de_cidades(self, api):
        resposta = api.get("/api/ddd/v1/11")
        corpo = resposta.json()

        assert resposta.status == 200
        assert corpo["state"] == "SP"
        assert isinstance(corpo["cities"], list)
        assert "SÃO PAULO" in corpo["cities"]


class TestDddNegativo:
    @pytest.mark.parametrize(
        "ddd_invalido",
        [
            "00",  # não existe DDD 00
            "1",  # falta um dígito
            "999",  # dígito a mais
            "ab",  # não é numérico
        ],
    )
    def test_ddd_invalido_retorna_400(self, api, ddd_invalido):
        resposta = api.get(f"/api/ddd/v1/{ddd_invalido}")

        assert resposta.status == 400
        assert resposta.json()["name"] == "DDD_INVALID"
