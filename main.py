from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.text import LabelBase
from database import Database

# Configurações de Janela para teste (simulando mobile)
Window.size = (360, 640)
Window.clearcolor = (0.02, 0.024, 0.04, 1)

# Registro de Fontes Futuristas
try:
    LabelBase.register(name='Orbitron', fn_regular='assets/Orbitron-Regular.ttf')
    LabelBase.register(name='Exo2', fn_regular='assets/Exo2-Regular.otf')
except Exception as e:
    print(f"Erro ao registrar fontes: {e}")

# Inicializa Banco de Dados
db = Database()

class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def do_login(self):
        user = db.login_user(self.username.text, self.password.text)
        if user:
            app = App.get_running_app()
            app.current_user = user
            self.manager.current = 'dashboard'
        else:
            print("Login falhou")

class RegisterScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    profession = ObjectProperty(None)

    def do_register(self):
        if db.register_user(self.username.text, self.password.text, self.profession.text):
            self.manager.current = 'login'
        else:
            print("Erro no registro")

class DashboardScreen(Screen):
    user_info = StringProperty("")

    def on_enter(self):
        user = App.get_running_app().current_user
        if user:
            prof = user[2].upper()
            self.user_info = (
                f"AGENTE: {user[1].upper()}\n"
                f"SETOR: {prof}\n"
                f"STATUS: OPERACIONAL\n"
                f"--------------------------\n"
                f"Bem-vindo ao centro de comando Tera. Suas ferramentas de {prof} estão prontas."
            )

    def save_report(self):
        user = App.get_running_app().current_user
        if user:
            # Exemplo de salvamento de relatório automático baseado na profissão
            title = f"Relatório Diário - {user[2]}"
            content = f"Atividades registradas para o agente {user[1]} na área de {user[2]}."
            db.save_user_data(user[0], title, content, user[2])
            print(f"Relatório de {user[2]} salvo com sucesso!")

class WindowManager(ScreenManager):
    pass

class TeraApp(App):
    current_user = None

    def build(self):
        return Builder.load_file('tera.kv')

if __name__ == '__main__':
    TeraApp().run()
