# AutoWall

Gerenciador de regras de Firewall para Windows com interface gráfica, focado em liberar portas TCP/UDP de forma rápida e segura.

## Funcionalidades

- Cria automaticamente 4 regras no Windows Firewall:
  - TCP Entrada
  - TCP Saída
  - UDP Entrada
  - UDP Saída
- Aceita portas em formato:
  - Porta única: `8080`
  - Intervalo: `3030-3040`
  - Múltiplas entradas por vírgula: `8080,8443,3030-3040`
- Valida nome da regra e exibe caracteres inválidos com código Unicode.
- Bloqueia criação quando há erros de validação.
- Executável configurado para solicitar privilégios de administrador (UAC).

## Requisitos

- Windows 10/11
- PowerShell disponível no sistema
- Permissão de administrador para criar regras de firewall

## Como usar (executável)

1. Acesse a aba **Releases** deste repositório.
2. Baixe o arquivo `AutoWall.exe`.
3. Execute o arquivo e aceite o prompt de administrador (UAC).
4. Preencha:
   - **Nome base da regra**
   - **Porta(s)** (ex.: `8080,8443,3030-3040`)
5. Clique em **Criar regras no Firewall**.

> Não é necessário ter Python instalado para usar o executável.

## Como executar pelo código-fonte

```bash
# Criar/ativar ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install customtkinter pyinstaller

# Executar aplicação
python autowall.py
```

## Build do executável (reproduzível)

O projeto mantém o arquivo `.spec` para facilitar builds consistentes.

### Build rápido por comando

```bash
venv\Scripts\pyinstaller.exe --noconfirm --clean --onefile --windowed --name AutoWall --uac-admin autowall.py
```

Saída gerada em:

- `dist/AutoWall.exe`

## Observações

- O aplicativo cria regras de firewall com perfil `Domain,Private,Public`.
- Se houver erro no formato das portas ou caracteres inválidos no nome, a criação é interrompida e uma mensagem de correção é exibida.
- Em alguns ambientes, o Windows SmartScreen pode exibir aviso para executáveis não assinados digitalmente.

## Estrutura do projeto

- `autowall.py` - código principal da aplicação
- `AutoWall.spec` - configuração de build (PyInstaller)
- `.gitignore` - arquivos/pastas ignorados no Git

## Licença

Defina a licença desejada para o projeto (ex.: MIT).
