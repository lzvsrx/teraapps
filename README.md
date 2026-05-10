# TERA - Agente Pessoal de Serviço (BeeWare Version)

Este é o aplicativo **TERA**, um agente pessoal futurista desenvolvido com **Python** e **BeeWare (Toga)** para Android e Desktop.

## 🚀 Funcionalidades
- **Autenticação Segura**: Sistema de login e cadastro com hash SHA-256.
- **Banco de Dados Nativo**: Armazenamento de dados persistente usando SQLite (diretório de dados padrão do sistema).
- **Interface Nativa**: Utiliza widgets nativos do sistema operacional para melhor performance.
- **Agente de Serviço**: Terminal interativo para comandos e gerenciamento de dados por profissão.

## 🛠️ Como executar localmente
1. Instale as dependências:
   ```bash
   pip install briefcase toga
   ```
2. Execute o aplicativo em modo de desenvolvimento:
   ```bash
   briefcase dev
   ```

## 📱 Como gerar o APK (Android)
Para gerar o APK utilizando o BeeWare:

1. Crie o projeto Android:
   ```bash
   briefcase create android
   ```
2. Compile o projeto:
   ```bash
   briefcase build android
   ```
3. Execute no emulador ou dispositivo:
   ```bash
   briefcase run android
   ```
4. Gere o pacote de distribuição:
   ```bash
   briefcase package android
   ```

## 📁 Estrutura do Projeto
- `src/tera/app.py`: Lógica principal da interface Toga.
- `src/tera/database/db_manager.py`: Gerenciamento do banco de dados SQLite.
- `pyproject.toml`: Configurações do BeeWare/Briefcase.
