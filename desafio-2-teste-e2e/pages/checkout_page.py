"""
Page Object da tela de checkout (/checkout-one).

O carrinho desse site já vem pré-carregado com uns produtos de exemplo
(assim que você abre o site, sem precisar adicionar nada), então dá pra
chegar direto no checkout sem precisar montar carrinho na mão.

O fluxo de finalizar pedido tem uma pegadinha: não basta preencher os dados
e clicar em "Place Order" direto. Descobri isso testando manualmente - o
formulário de cobrança precisa ser salvo primeiro (botão "Save"), só depois
disso o "Place Order" realmente completa a compra. Se pular o "Save", o
site mostra sempre a mensagem "Preencha os dados de pagamento!", mesmo com
tudo preenchido certinho.
"""

from playwright.sync_api import Page, expect


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

        # dados de cobrança
        self.primeiro_nome = page.locator("#fname")
        self.ultimo_nome = page.locator("#lname")
        self.nome_empresa = page.locator("#cname")
        self.email = page.locator("#email")
        self.pais = page.locator("#country")
        self.estado_cidade = page.locator("#city")
        self.cep = page.locator("#zip")
        self.endereco_completo = page.locator("#faddress")
        self.observacoes = page.locator("#messages")

        self.botao_salvar = page.get_by_role("button", name="Save")
        self.botao_finalizar_pedido = page.get_by_role("button", name="Place Order")

        self.mensagem_dados_salvos = page.get_by_text(
            "Billings Information registred with success!"
        )
        self.mensagem_erro_pagamento = page.get_by_text(
            "Preencha os dados de pagamento!"
        )

    def abrir(self):
        self.page.goto("/checkout-one", wait_until="domcontentloaded")
        expect(self.primeiro_nome).to_be_visible()
        return self

    def preencher_dados_de_cobranca(
        self,
        primeiro_nome: str,
        ultimo_nome: str,
        empresa: str,
        email: str,
        cep: str,
        endereco: str,
        observacoes: str = "",
    ):
        self.primeiro_nome.fill(primeiro_nome)
        self.ultimo_nome.fill(ultimo_nome)
        self.nome_empresa.fill(empresa)
        self.email.fill(email)
        # o site só tem duas opções "reais" de país e de estado/cidade,
        # o resto é conteúdo de exemplo do template (Afghanistan etc.)
        self.pais.select_option("usa")
        self.estado_cidade.select_option("Aland Islands")
        self.cep.fill(cep)
        self.endereco_completo.fill(endereco)
        if observacoes:
            self.observacoes.fill(observacoes)
        return self

    def salvar_dados_de_cobranca(self):
        self.botao_salvar.click()
        expect(self.mensagem_dados_salvos).to_be_visible()
        return self

    def finalizar_pedido(self):
        self.botao_finalizar_pedido.click()
        return self

    def confirmar_modal_pedido_realizado(self):
        expect(self.page.get_by_text("Order success!")).to_be_visible()
