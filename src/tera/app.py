import toga
from toga.style import Pack
from toga.style.constants import COLUMN, ROW, CENTER, BOLD, ITALIC
from tera.database.db_manager import DatabaseManager

# Theme Constants (Approximated for Toga)
BG_COLOR = "#05060A"
PRIMARY_PURPLE = "#A855F7"
PRIMARY_BLUE = "#3B82F6"
SECONDARY_BLUE = "#22D3EE"
SILVER = "#E5E7EB"
WHITE = "#FFFFFF"

class TERA(toga.App):
    def startup(self):
        self.db = DatabaseManager(self)
        self.user = None
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.show_login()
        self.main_window.show()

    def show_login(self, widget=None):
        self.username_input = toga.TextInput(placeholder="Usuário", style=Pack(width=300, padding=10))
        self.password_input = toga.PasswordInput(placeholder="Senha", style=Pack(width=300, padding=10))
        
        login_button = toga.Button(
            "INICIAR SISTEMA",
            on_press=self.handle_login,
            style=Pack(width=300, padding=10, background_color=PRIMARY_PURPLE, color=WHITE)
        )
        
        register_link = toga.Button(
            "CRIAR NOVA IDENTIDADE",
            on_press=self.show_register,
            style=Pack(padding=10, color=SECONDARY_BLUE)
        )

        title_label = toga.Label(
            "TERA",
            style=Pack(font_size=50, font_weight=BOLD, color=WHITE, padding_bottom=10)
        )
        subtitle_label = toga.Label(
            "AGENTE PESSOAL DE SERVIÇO",
            style=Pack(font_size=12, color=SILVER, padding_bottom=40)
        )

        login_box = toga.Box(
            children=[
                title_label,
                subtitle_label,
                self.username_input,
                self.password_input,
                login_button,
                register_link
            ],
            style=Pack(direction=COLUMN, alignment=CENTER, padding=50, background_color=BG_COLOR)
        )
        
        self.main_window.content = login_box

    def handle_login(self, widget):
        username = self.username_input.value
        password = self.password_input.value
        
        if not username or not password:
            self.main_window.info_dialog("Erro", "Preencha todos os campos!")
            return

        user = self.db.authenticate_user(username, password)
        if user:
            self.user = {"id": user[0], "username": user[1], "profession": user[2]}
            self.show_dashboard()
        else:
            self.main_window.error_dialog("Erro", "Login inválido!")

    def show_register(self, widget=None):
        self.reg_username = toga.TextInput(placeholder="Usuário", style=Pack(width=300, padding=10))
        self.reg_password = toga.PasswordInput(placeholder="Senha", style=Pack(width=300, padding=10))
        self.reg_profession = toga.Selection(
            items=["Tecnologia", "Saúde", "Educação", "Design", "Engenharia", "Outros"],
            style=Pack(width=300, padding=10)
        )
        
        register_button = toga.Button(
            "CADASTRAR",
            on_press=self.handle_register,
            style=Pack(width=300, padding=10, background_color=PRIMARY_BLUE, color=WHITE)
        )
        
        back_button = toga.Button(
            "Voltar para Login",
            on_press=self.show_login,
            style=Pack(padding=10)
        )

        register_box = toga.Box(
            children=[
                toga.Label("CADASTRO", style=Pack(font_size=30, font_weight=BOLD, color=WHITE, padding_bottom=20)),
                self.reg_username,
                self.reg_password,
                self.reg_profession,
                register_button,
                back_button
            ],
            style=Pack(direction=COLUMN, alignment=CENTER, padding=50, background_color=BG_COLOR)
        )
        
        self.main_window.content = register_box

    def handle_register(self, widget):
        username = self.reg_username.value
        password = self.reg_password.value
        profession = self.reg_profession.value
        
        if self.db.create_user(username, password, profession):
            self.main_window.info_dialog("Sucesso", "Conta criada com sucesso!")
            self.show_login()
        else:
            self.main_window.error_dialog("Erro", "Usuário já existe!")

    def show_dashboard(self):
        profession = self.user["profession"]
        
        # Tab 1: Data
        self.title_input = toga.TextInput(placeholder="Título da Atividade", style=Pack(flex=1, padding=5))
        self.content_input = toga.MultilineTextInput(placeholder="Descrição/Dados", style=Pack(flex=1, padding=5, height=100))
        
        save_button = toga.Button(
            "ARQUIVAR NO BANCO",
            on_press=self.handle_save_data,
            style=Pack(padding=10, background_color=PRIMARY_PURPLE, color=WHITE)
        )
        
        self.data_list_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.refresh_data()

        data_scroll = toga.ScrollContainer(content=self.data_list_box, style=Pack(flex=1))

        data_tab_box = toga.Box(
            children=[
                toga.Label(f"SETOR: {profession.upper()}", style=Pack(color=PRIMARY_PURPLE, font_weight=BOLD)),
                self.title_input,
                self.content_input,
                save_button,
                toga.Label("REGISTROS ENCRIPTADOS", style=Pack(color=PRIMARY_BLUE, font_weight=BOLD, padding_top=10)),
                data_scroll
            ],
            style=Pack(direction=COLUMN, padding=20, background_color=BG_COLOR)
        )

        # Tab 2: Agent
        self.agent_chat_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.agent_input = toga.TextInput(placeholder="Comando para o Agente TERA...", style=Pack(flex=1))
        
        agent_send_button = toga.Button(
            "Enviar",
            on_press=self.handle_agent_command,
            style=Pack(padding=5, background_color=PRIMARY_PURPLE, color=WHITE)
        )

        agent_scroll = toga.ScrollContainer(content=self.agent_chat_box, style=Pack(flex=1))

        agent_tab_box = toga.Box(
            children=[
                toga.Label("TERMINAL DO AGENTE", style=Pack(color=PRIMARY_PURPLE, font_weight=BOLD)),
                agent_scroll,
                toga.Box(children=[self.agent_input, agent_send_button], style=Pack(direction=ROW, padding=10))
            ],
            style=Pack(direction=COLUMN, padding=20, background_color=BG_COLOR)
        )

        container = toga.OptionContainer(
            content=[
                toga.OptionItem("DADOS", data_tab_box),
                toga.OptionItem("AGENTE", agent_tab_box)
            ],
            style=Pack(flex=1)
        )
        
        # Dashboard Toolbar/Menu
        logout_cmd = toga.Command(
            self.show_login,
            text="Sair",
            tooltip="Logout",
            icon=toga.Icon.TOGA_ICON
        )
        self.main_window.toolbar.add(logout_cmd)
        
        self.main_window.content = container

    def refresh_data(self):
        self.data_list_box.clear()
        items = self.db.get_profession_data(self.user["id"])
        for item in items:
            item_box = toga.Box(
                children=[
                    toga.Label(item[1], style=Pack(font_weight=BOLD, color=PRIMARY_BLUE)),
                    toga.Label(item[2], style=Pack(color=WHITE, font_size=10)),
                    toga.Label(f"Sincronizado: {item[4]}", style=Pack(color=SILVER, font_size=8))
                ],
                style=Pack(direction=COLUMN, padding=10, background_color="#0D1117")
            )
            self.data_list_box.add(item_box)

    def handle_save_data(self, widget):
        title = self.title_input.value
        content = self.content_input.value
        if title and content:
            self.db.save_profession_data(self.user["id"], title, content, self.user["profession"])
            self.title_input.value = ""
            self.content_input.value = ""
            self.refresh_data()

    def handle_agent_command(self, widget):
        cmd_text = self.agent_input.value
        if cmd_text:
            cmd = cmd_text.lower()
            self.agent_chat_box.add(toga.Label(f"> {cmd_text}", style=Pack(color=SILVER, font_style=ITALIC)))
            
            response = "Comando processado com sucesso. Dados arquivados."
            if "ajuda" in cmd:
                response = f"Como seu agente de {self.user['profession']}, posso arquivar relatórios e gerenciar dados."
            elif "status" in cmd:
                response = "Sistemas TERA operacionais. Conexão ativa."
            
            self.agent_chat_box.add(
                toga.Box(
                    children=[toga.Label(response, style=Pack(color=PRIMARY_BLUE, font_weight=BOLD))],
                    style=Pack(padding=5, background_color="#1A1F2B")
                )
            )
            self.agent_input.value = ""

def main():
    return TERA("TERA", "com.lzvsrx.tera")
