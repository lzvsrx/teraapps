import flet as ft
from database.db_manager import DatabaseManager

# Theme Constants
BG_COLOR = "#05060A"
PRIMARY_PURPLE = "#A855F7"
SECONDARY_PURPLE = "#C084FC"
PRIMARY_BLUE = "#3B82F6"
SECONDARY_BLUE = "#22D3EE"
SILVER = "#E5E7EB"
WHITE = "#FFFFFF"

# Fonts
FONTS = {
    "Orbitron": "https://github.com/google/fonts/raw/main/ofl/orbitron/static/Orbitron-Bold.ttf",
    "Exo2": "https://github.com/google/fonts/raw/main/ofl/exo2/static/Exo2-Regular.ttf",
}

class TeraApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = DatabaseManager()
        self.user = None
        
        self.setup_page()
        self.show_login()

    def setup_page(self):
        self.page.title = "TERA - Personal Agent"
        self.page.bgcolor = BG_COLOR
        self.page.fonts = FONTS
        self.page.theme = ft.Theme(
            font_family="Exo2",
            color_scheme=ft.ColorScheme(
                primary=PRIMARY_PURPLE,
                secondary=PRIMARY_BLUE,
                surface=BG_COLOR,
            )
        )
        self.page.padding = 0
        self.page.window_width = 400
        self.page.window_height = 800
        self.page.update()

    def get_logo(self, size=150):
        try:
            return ft.Image(
                src="logo.png",
                width=size,
                height=size,
                fit=ft.ImageFit.CONTAIN,
            )
        except:
            return ft.Text(
                "T",
                size=size,
                font_family="Orbitron",
                weight="bold",
                color=WHITE,
            )

    def show_login(self):
        self.page.views.clear()
        
        logo = self.get_logo(200)
        
        username_field = ft.TextField(
            label="Usuário",
            color=WHITE,
            border_color=PRIMARY_BLUE,
            focused_border_color=PRIMARY_PURPLE,
            text_style=ft.TextStyle(font_family="Exo2"),
            prefix_icon=ft.icons.PERSON_OUTLINE,
        )
        
        password_field = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            color=WHITE,
            border_color=PRIMARY_BLUE,
            focused_border_color=PRIMARY_PURPLE,
            text_style=ft.TextStyle(font_family="Exo2"),
            prefix_icon=ft.icons.LOCK_OUTLINE,
        )

        def login_click(e):
            if not username_field.value or not password_field.value:
                self.page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"), bgcolor="orange")
                self.page.snack_bar.open = True
                self.page.update()
                return

            user = self.db.authenticate_user(username_field.value, password_field.value)
            if user:
                self.user = {"id": user[0], "username": user[1], "profession": user[2]}
                self.show_dashboard()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Login inválido!"), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()

        login_view = ft.View(
            "/login",
            [
                ft.Container(
                    expand=True,
                    padding=40,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=[BG_COLOR, "#0A0F1F"],
                    ),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            logo,
                            ft.Text(
                                "TERA",
                                size=50,
                                font_family="Orbitron",
                                weight="bold",
                                color=WHITE,
                                shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=PRIMARY_PURPLE)
                            ),
                            ft.Text(
                                "AGENTE PESSOAL DE SERVIÇO",
                                size=12,
                                color=SILVER,
                                font_family="Exo2",
                                letter_spacing=3
                            ),
                            ft.Divider(height=40, color="transparent"),
                            username_field,
                            password_field,
                            ft.ElevatedButton(
                                "INICIAR SISTEMA",
                                color=WHITE,
                                bgcolor=PRIMARY_PURPLE,
                                width=300,
                                height=55,
                                on_click=login_click,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                )
                            ),
                            ft.TextButton(
                                "CRIAR NOVA IDENTIDADE",
                                font_family="Exo2",
                                on_click=lambda _: self.show_register(),
                                style=ft.ButtonStyle(color=SECONDARY_BLUE)
                            )
                        ]
                    )
                )
            ],
            bgcolor=BG_COLOR
        )
        
        self.page.views.append(login_view)
        self.page.update()

    def show_register(self):
        self.page.views.clear()
        
        username_field = ft.TextField(label="Usuário", color=WHITE, border_color=PRIMARY_BLUE)
        password_field = ft.TextField(label="Senha", password=True, color=WHITE, border_color=PRIMARY_BLUE)
        profession_field = ft.Dropdown(
            label="Área de Atuação",
            options=[
                ft.dropdown.Option("Tecnologia"),
                ft.dropdown.Option("Saúde"),
                ft.dropdown.Option("Educação"),
                ft.dropdown.Option("Design"),
                ft.dropdown.Option("Engenharia"),
                ft.dropdown.Option("Outros"),
            ],
            color=WHITE,
            border_color=PRIMARY_BLUE
        )

        def register_click(e):
            if self.db.create_user(username_field.value, password_field.value, profession_field.value):
                self.page.snack_bar = ft.SnackBar(ft.Text("Conta criada com sucesso!"), bgcolor="green")
                self.page.snack_bar.open = True
                self.show_login()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Erro: Usuário já existe!"), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()

        register_view = ft.View(
            "/register",
            [
                ft.Container(
                    expand=True,
                    padding=40,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("CADASTRO", size=30, font_family="Orbitron", color=WHITE),
                            ft.Divider(height=20, color="transparent"),
                            username_field,
                            password_field,
                            profession_field,
                            ft.ElevatedButton(
                                "CADASTRAR",
                                color=WHITE,
                                bgcolor=PRIMARY_BLUE,
                                width=300,
                                height=50,
                                on_click=register_click
                            ),
                            ft.TextButton("Voltar para Login", on_click=lambda _: self.show_login())
                        ]
                    )
                )
            ],
            bgcolor=BG_COLOR
        )
        self.page.views.append(register_view)
        self.page.update()

    def show_dashboard(self):
        self.page.views.clear()
        
        profession = self.user["profession"]
        logo = self.get_logo(40)
        
        def save_note(e):
            title = title_input.value
            content = content_input.value
            if title and content:
                self.db.save_profession_data(self.user["id"], title, content, profession)
                title_input.value = ""
                content_input.value = ""
                load_data()
                self.page.update()

        title_input = ft.TextField(
            label="Título da Atividade", 
            color=WHITE, 
            border_color=PRIMARY_PURPLE,
            focused_border_color=SECONDARY_PURPLE,
        )
        content_input = ft.TextField(
            label="Descrição/Dados", 
            multiline=True, 
            color=WHITE, 
            border_color=PRIMARY_BLUE,
            focused_border_color=SECONDARY_BLUE,
        )
        data_list = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=10)

        def load_data():
            data_list.controls.clear()
            items = self.db.get_profession_data(self.user["id"])
            for item in items:
                data_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.icons.DATA_OBJECT, color=SECONDARY_BLUE, size=16),
                                ft.Text(item[1], weight="bold", color=SECONDARY_BLUE, font_family="Orbitron", size=14),
                            ], alignment=ft.MainAxisAlignment.START),
                            ft.Text(item[2], color=WHITE, size=13),
                            ft.Text(f"Sincronizado: {item[4]}", size=9, color=SILVER),
                        ], spacing=5),
                        padding=15,
                        border_radius=12,
                        bgcolor="#0D1117",
                        border=ft.border.all(1, "#1F2937"),
                        animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
                    )
                )

        load_data()

        # Agent Interface Section
        agent_chat = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
        agent_input = ft.TextField(
            hint_text="Comando para o Agente TERA...",
            expand=True,
            border_color=PRIMARY_PURPLE,
            color=WHITE,
        )

        def agent_command(e):
            if agent_input.value:
                cmd = agent_input.value.lower()
                agent_chat.controls.append(ft.Text(f"> {agent_input.value}", color=SILVER, italic=True))
                
                # Simple logic for "agent" behavior
                response = "Comando processado com sucesso. Dados arquivados."
                if "ajuda" in cmd:
                    response = f"Como seu agente de {profession}, posso arquivar relatórios, organizar tarefas e gerenciar seus dados seguros."
                elif "status" in cmd:
                    response = "Sistemas TERA operacionais. Conexão criptografada ativa."
                
                agent_chat.controls.append(
                    ft.Container(
                        content=ft.Text(response, color=SECONDARY_BLUE, weight="bold"),
                        padding=10,
                        bgcolor="#1A1F2B",
                        border_radius=10,
                    )
                )
                agent_input.value = ""
                self.page.update()

        dashboard_view = ft.View(
            "/dashboard",
            [
                ft.AppBar(
                    leading=logo,
                    title=ft.Text("TERA CORE", font_family="Orbitron", color=WHITE),
                    bgcolor="#05060A",
                    center_title=True,
                    actions=[
                        ft.IconButton(ft.icons.LOGOUT_ROUNDED, icon_color=PRIMARY_PURPLE, on_click=lambda _: self.show_login())
                    ]
                ),
                ft.Tabs(
                    selected_index=0,
                    animation_duration=300,
                    tabs=[
                        ft.Tab(
                            text="DADOS",
                            icon=ft.icons.STORAGE,
                            content=ft.Container(
                                padding=20,
                                content=ft.Column([
                                    ft.Text(f"SETOR: {profession.upper()}", color=PRIMARY_PURPLE, font_family="Orbitron", size=12, letter_spacing=2),
                                    ft.Divider(color="#1F2937"),
                                    title_input,
                                    content_input,
                                    ft.ElevatedButton(
                                        "ARQUIVAR NO BANCO", 
                                        on_click=save_note, 
                                        bgcolor=PRIMARY_PURPLE, 
                                        color=WHITE,
                                        width=400,
                                        height=45
                                    ),
                                    ft.Divider(color="#1F2937"),
                                    ft.Text("REGISTROS ENCRIPTADOS", color=SECONDARY_BLUE, size=12, font_family="Orbitron"),
                                    data_list
                                ])
                            )
                        ),
                        ft.Tab(
                            text="AGENTE",
                            icon=ft.icons.SMART_TOY,
                            content=ft.Container(
                                padding=20,
                                content=ft.Column([
                                    ft.Text("TERMINAL DO AGENTE", color=PRIMARY_PURPLE, font_family="Orbitron", size=12, letter_spacing=2),
                                    ft.Divider(color="#1F2937"),
                                    ft.Container(
                                        content=agent_chat,
                                        expand=True,
                                        bgcolor="#05060A",
                                        padding=10,
                                        border=ft.border.all(1, "#1F2937"),
                                        border_radius=10,
                                    ),
                                    ft.Row([
                                        agent_input,
                                        ft.IconButton(ft.icons.SEND_ROUNDED, icon_color=PRIMARY_PURPLE, on_click=agent_command)
                                    ])
                                ])
                            )
                        )
                    ],
                    expand=True,
                )
            ],
            bgcolor=BG_COLOR
        )
        self.page.views.append(dashboard_view)
        self.page.update()

def main(page: ft.Page):
    TeraApp(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
