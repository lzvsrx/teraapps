# TERA - Agente Pessoal de Serviço

Este é o aplicativo **TERA**, um agente pessoal futurista desenvolvido com Python e Flet para Android.

## 🚀 Funcionalidades
- **Autenticação Segura**: Sistema de login e cadastro com hash SHA-256.
- **Banco de Dados Local**: Armazenamento de dados persistente usando SQLite.
- **Interface Cyberpunk**: Design moderno com cores neon, fontes futuristas (Orbitron/Exo2) e efeitos de brilho.
- **Agente de Serviço**: Terminal interativo para comandos e gerenciamento de dados por profissão.
- **Multi-Profissões**: Adaptável para diversas áreas (Tecnologia, Saúde, Educação, etc).

## 🎨 Tema Visual
- **Fundo**: Preto Profundo (#05060A)
- **Cores**: Roxo Neon (#A855F7) e Azul Neon (#3B82F6)
- **Fontes**: Orbitron (Logo/Títulos) e Exo 2 (Interface)

## 🛠️ Como executar localmente
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o aplicativo:
   ```bash
   python main.py
   ```

## 📱 Como gerar o APK
Para gerar o APK para Android, você precisará do [Flutter SDK](https://docs.flutter.dev/get-started/install) instalado no seu sistema.

Execute o seguinte comando na raiz do projeto:
```bash
flet build apk --project-name tera --display-name "TERA" --description "Agente Pessoal de Serviço"
```

O ícone será gerado automaticamente a partir do arquivo `assets/logo.png`. Certifique-se de colocar a logo desejada nessa pasta com o nome `logo.png`.

## 📁 Estrutura do Projeto
- `main.py`: Ponto de entrada e lógica da interface.
- `database/db_manager.py`: Gerenciamento do banco de dados SQLite e segurança.
- `assets/`: Pasta para imagens e fontes.
- `requirements.txt`: Dependências do projeto.
