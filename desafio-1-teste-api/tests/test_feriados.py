"""Testes do endpoint de feriados nacionais: GET /api/feriados/v1/{ano}"""


class TestFeriadosPositivo:
    def test_feriados_de_2025_vem_completos(self, api):
        resposta = api.get("/api/feriados/v1/2025")
        feriados = resposta.json()

        assert resposta.status == 200
        assert isinstance(feriados, list)
        # 2025 tem 14 feriados nacionais (fixos + móveis, tipo Carnaval e Páscoa)
        assert len(feriados) == 14

        ano_novo = feriados[0]
        assert ano_novo["date"] == "2025-01-01"
        assert ano_novo["name"] == "Confraternização mundial"
        assert ano_novo["type"] == "national"


class TestFeriadosNegativo:
    def test_ano_fora_do_intervalo_suportado_retorna_404(self, api):
        # a API só sabe calcular feriados entre 1900 e 2199
        resposta = api.get("/api/feriados/v1/999999")

        assert resposta.status == 404
        assert resposta.json()["type"] == "feriados_range_error"

    def test_ano_nao_numerico_estoura_erro_interno(self, api):
        # comportamento meio estranho da API: ela não valida o parâmetro
        # antes de tentar calcular os feriados, então "abc" quebra com 500
        # em vez de devolver um 400 arrumadinho. Deixando documentado aqui
        # pra não pegar ninguém de surpresa se um dia mudarem isso.
        resposta = api.get("/api/feriados/v1/abc")

        assert resposta.status == 500
