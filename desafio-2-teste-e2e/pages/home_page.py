"""Page Object da página inicial (/)."""

from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.link_login = page.get_by_role("link", name="Login").first
        self.link_cadastro = page.get_by_role("link", name="Cadastro").first

    def abrir(self):
        # a home tem muita imagem de produto pra carregar, então o evento
        # "load" (padrão do Playwright) as vezes passa dos 30s. Espero só o
        # HTML estar pronto (domcontentloaded) e confio nas asserções de
        # elemento visível depois pra saber se a página realmente carregou
        self.page.goto("/", wait_until="domcontentloaded")
        expect(self.page).to_have_title("QAZANDO Shop E-Commerce")
        return self

    def abrir_produto(self, nome_produto: str):
        """Clica no link de um produto listado na home (pelo nome exibido)."""
        self.page.get_by_role("link", name=nome_produto, exact=True).first.click()
        return self

    def ir_para_login(self):
        self.link_login.click()
        return self
