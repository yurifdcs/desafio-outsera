"""Page Object da página de detalhes de um produto (/product-details-*)."""

from playwright.sync_api import Page, expect


class ProductPage:
    def __init__(self, page: Page):
        self.page = page
        self.botao_adicionar_ao_carrinho = page.get_by_role(
            "link", name="Add To Cart"
        )

    def titulo_do_produto(self, nome_produto: str):
        # o site tem duas variações de template pra página de produto
        # (product-details-one e product-details-two) e o nível do heading
        # do título muda entre elas, então não fixo o "level" aqui
        return self.page.get_by_role("heading", name=nome_produto)

    def esperar_carregar(self, nome_produto: str):
        expect(self.titulo_do_produto(nome_produto)).to_be_visible()
        expect(self.botao_adicionar_ao_carrinho).to_be_visible()
        return self
