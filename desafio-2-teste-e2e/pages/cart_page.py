"""Page Object da tela de carrinho (/cart)."""

from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.link_finalizar_compra = page.get_by_role(
            "link", name="Proceed to Checkout"
        )
        self.botao_limpar_carrinho = page.get_by_role("button", name="Clear cart")

    def abrir(self):
        self.page.goto("/cart", wait_until="domcontentloaded")
        expect(self.botao_limpar_carrinho).to_be_visible()
        return self

    def ir_para_checkout(self):
        self.link_finalizar_compra.click()
        return self

    def tem_produto(self, nome_produto: str):
        # o nome do produto também aparece no mini-carrinho (offcanvas) do
        # cabeçalho, então preciso restringir a busca à tabela de itens do
        # carrinho pra não pegar duas ocorrências (strict mode do Playwright
        # não deixa passar um locator ambíguo)
        return self.page.locator("table").get_by_role(
            "link", name=nome_produto, exact=True
        )
