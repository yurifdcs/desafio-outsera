"""
Testes do endpoint de câmbio:
    GET /api/cambio/v1/moedas
    GET /api/cambio/v1/cotacao/{moeda}/{data}
"""


class TestCambioPositivo:
    def test_lista_de_moedas_disponiveis_inclui_dolar_e_euro(self, api):
        resposta = api.get("/api/cambio/v1/moedas")
        moedas = resposta.json()

        assert resposta.status == 200
        simbolos = [moeda["simbolo"] for moeda in moedas]
        assert "USD" in simbolos
        assert "EUR" in simbolos

    def test_cotacao_do_dolar_numa_data_valida(self, api):
        resposta = api.get("/api/cambio/v1/cotacao/USD/2025-01-10")
        corpo = resposta.json()

        assert resposta.status == 200
        assert corpo["moeda"] == "USD"
        assert corpo["data"] == "2025-01-10"
        assert len(corpo["cotacoes"]) > 0


class TestCambioNegativo:
    def test_moeda_que_nao_existe_retorna_400(self, api):
        resposta = api.get("/api/cambio/v1/cotacao/XYZ/2025-01-10")

        assert resposta.status == 400
        assert resposta.json()["name"] == "INVALID_CURRENCY_VALUE"

    def test_data_fora_do_formato_yyyy_mm_dd_retorna_400(self, api):
        resposta = api.get("/api/cambio/v1/cotacao/USD/10-01-2025")

        assert resposta.status == 400
        assert resposta.json()["name"] == "DATE_FORMAT_INCORRECT_PATTERN"
