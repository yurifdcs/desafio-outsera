"""
Testes do endpoint de CEP: GET /api/cep/v1/{cep}

A BrasilAPI consulta, nos bastidores, vários provedores de CEP (Correios,
ViaCEP, Widenet...) e devolve o primeiro que responder com sucesso. Aqui a
gente valida o caminho feliz (CEP existente) e alguns erros comuns: CEP fora
do padrão de 8 dígitos e CEP que não existe em nenhuma base.
"""

import pytest

CEP_VALIDO = "01310930"  # Av. Paulista, Bela Vista - São Paulo/SP


class TestCepPositivo:
    def test_busca_por_cep_valido_retorna_200_e_json(self, api):
        resposta = api.get(f"/api/cep/v1/{CEP_VALIDO}")

        assert resposta.status == 200
        assert "application/json" in resposta.headers["content-type"]

    def test_corpo_da_resposta_tem_os_dados_do_endereco(self, api):
        resposta = api.get(f"/api/cep/v1/{CEP_VALIDO}")
        endereco = resposta.json()

        assert endereco["cep"] == CEP_VALIDO
        assert endereco["state"] == "SP"
        assert endereco["city"] == "São Paulo"
        assert endereco["street"] == "Avenida Paulista"
        # esse campo indica qual dos provedores (correios, viacep etc.)
        # respondeu a consulta - não tem um valor fixo, só precisa existir
        assert endereco["service"]


class TestCepNegativo:
    @pytest.mark.parametrize(
        "cep_invalido",
        [
            "123",  # menos de 8 dígitos
            "1234567890",  # mais de 8 dígitos
            "abcdefgh",  # letras no lugar de números
            "0131093a",  # mistura número com letra
        ],
    )
    def test_cep_fora_do_padrao_retorna_400(self, api, cep_invalido):
        resposta = api.get(f"/api/cep/v1/{cep_invalido}")

        assert resposta.status == 400
        corpo = resposta.json()
        assert corpo["name"] == "CepPromiseError"

    def test_cep_valido_no_formato_mas_inexistente_retorna_404(self, api):
        # 8 dígitos, formato correto, só que esse CEP não existe de verdade
        resposta = api.get("/api/cep/v1/00000000")

        assert resposta.status == 404
        assert "message" in resposta.json()

    def test_chamada_sem_informar_o_cep_nao_retorna_sucesso(self, api):
        resposta = api.get("/api/cep/v1/", max_redirects=0)

        # sem o parâmetro a rota nem existe de fato, a aplicação só redireciona
        assert resposta.status != 200
