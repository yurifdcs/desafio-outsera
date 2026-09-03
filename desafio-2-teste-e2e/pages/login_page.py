"""
Page Object da tela de login (/login).

Fui direto no HTML da página pra pegar os ids reais dos campos (inspecionei
via devtools), porque o site não usa data-testid em nenhum lugar. Os campos
não têm "name", então uso os ids mesmo: #user e #password.

Uma coisa curiosa que descobri testando manualmente: esse site de prática
não valida a senha de verdade. Qualquer senha não-vazia passa, desde que o
e-mail tenha um formato válido (com @). Ou seja, não existe "senha errada"
de fato aqui - só "e-mail inválido" e "senha vazia". Por isso os testes
negativos de login cobrem exatamente esses dois casos.
"""

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.campo_email = page.locator("#user")
        self.campo_senha = page.locator("#password")
        self.botao_login = page.get_by_role("button", name="login")
        self.mensagem_invalida = page.locator(".invalid_input")

    def abrir(self):
        self.page.goto("/login", wait_until="domcontentloaded")
        expect(self.campo_email).to_be_visible()
        return self

    def logar(self, email: str, senha: str):
        self.campo_email.fill(email)
        self.campo_senha.fill(senha)
        self.botao_login.click()
        return self

    def confirmar_modal_de_sucesso(self):
        """Depois de um login válido aparece um modalzinho de confirmação
        (tipo SweetAlert) com um botão OK. Clico nele pra seguir o fluxo."""
        botao_ok = self.page.get_by_role("button", name="OK")
        expect(botao_ok).to_be_visible()
        botao_ok.click()
