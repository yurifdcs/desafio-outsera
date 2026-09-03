"""
Testes do endpoint de bancos: GET /api/banks/v1 e GET /api/banks/v1/{code}

O primeiro retorna a lista completa de instituições cadastradas no Bacen,
o segundo busca uma instituição específica pelo código COMPE.
"""


class TestBancosPositivo:
    def test_lista_completa_de_bancos(self, api):
        resposta = api.get("/api/banks/v1")
        bancos = resposta.json()

        assert resposta.status == 200
        assert "application/json" in resposta.headers["content-type"]
        assert isinstance(bancos, list)
        # hoje a base tem mais de 400 instituições, então um número bem
        # menor já é suficiente pra garantir que a lista veio populada
        assert len(bancos) > 100

    def test_banco_do_brasil_pelo_codigo_1(self, api):
        resposta = api.get("/api/banks/v1/1")
        banco = resposta.json()

        assert resposta.status == 200
        assert banco["code"] == 1
        assert banco["ispb"] == "00000000"
        assert "Brasil" in banco["fullName"]


class TestBancosNegativo:
    def test_codigo_de_banco_que_nao_existe_retorna_404(self, api):
        resposta = api.get("/api/banks/v1/99999")

        assert resposta.status == 404
        assert resposta.json()["type"] == "BANK_CODE_NOT_FOUND"

    def test_codigo_de_banco_com_letras_tambem_retorna_404(self, api):
        resposta = api.get("/api/banks/v1/abc")

        assert resposta.status == 404
