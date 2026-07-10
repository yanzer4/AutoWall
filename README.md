# 🔥 AutoWall

Gerenciador de regras de Firewall para Windows com interface gráfica, focado em **liberar portas TCP/UDP de forma rápida, padronizada e segura**.

Criar regras manualmente no Windows Firewall pode ser repetitivo e propenso a erros. O **AutoWall automatiza esse processo**, criando todas as regras necessárias com apenas alguns cliques.

---

## 🚀 Funcionalidades

* Criação automática de **4 regras no Windows Firewall**:

  * TCP Entrada
  * TCP Saída
  * UDP Entrada
  * UDP Saída

* Suporte a múltiplos formatos de portas:

  * Porta única: `8080`
  * Intervalo: `3030-3040`
  * Múltiplas entradas: `8080,8443,3030-3040`

* **Atalho de 1 clique** para a faixa padrão da empresa:

  * Botão **"⚡ Liberar PORTAS PLAYLIST (3030-3040)"** cria as regras
    automaticamente, sem precisar digitar nome ou portas
  * O preset (nome e faixa) é configurável nas constantes
    `COMPANY_PRESET_NAME` e `COMPANY_PRESET_PORTS` do `autowall.py`

* Validação de entrada:

  * Verifica formato das portas
  * Identifica caracteres inválidos no nome da regra (com código Unicode)

* Segurança:

  * Bloqueia criação em caso de erro
  * Executa com privilégios de administrador (UAC)

---

## 🧠 Como funciona

O AutoWall utiliza comandos do PowerShell (`New-NetFirewallRule`) para criar automaticamente regras de entrada e saída no Windows Firewall.

As 4 regras são criadas em uma única execução silenciosa do PowerShell, sem abrir janelas adicionais no sistema.

As regras são criadas com os seguintes perfis:

* Domain
* Private
* Public

O processo garante padronização e evita erros comuns na criação manual de regras.

---

## 📌 Exemplo de uso

**Entrada:**

* Nome da regra: `WebServer`
* Portas: `8080,8443`

**Regras criadas:**

* `WebServer_TCP_IN`
* `WebServer_TCP_OUT`
* `WebServer_UDP_IN`
* `WebServer_UDP_OUT`

---

## 💻 Requisitos

* Windows 8 / 8.1, Windows 10 ou Windows 11
* Windows Server 2012 ou superior
* PowerShell disponível no sistema
* Permissão de administrador

---

## ▶️ Como usar (executável)

1. Acesse a aba **Releases** do repositório
2. Baixe o arquivo `AutoWall.exe`
3. Execute o arquivo e aceite o prompt de administrador (UAC)
4. Escolha uma das opções:

   **Manual:**
   * Preencha o **Nome base da regra** e a(s) **Porta(s)** (ex: `8080,8443,3030-3040`)
   * Clique em **Criar regras no Firewall**

   **Atalho da empresa:**
   * Clique em **"⚡ Liberar PORTAS PLAYLIST (3030-3040)"** — as regras são
     criadas na hora, com nome e faixa padrão, sem preencher nada

> ⚠️ Não é necessário ter Python instalado para usar o executável.

---

## 🧪 Como executar pelo código-fonte

```bash
# Criar/ativar ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install customtkinter pyinstaller

# Executar aplicação
python autowall.py
```

---

## 🏗️ Build do executável

O projeto inclui arquivo `.spec` para builds reproduzíveis.

### Build com o .spec (recomendado):

```bash
pyinstaller AutoWall.spec --noconfirm
```

### Build rápido:

```bash
venv\Scripts\pyinstaller.exe --noconfirm --clean --onefile --windowed --name AutoWall --uac-admin autowall.py
```

**Saída:**

```
dist/AutoWall.exe
```

---

## 📦 Instalador

O projeto inclui um script **Inno Setup** (`installer.iss`) para gerar um instalador Windows completo.

### Pré-requisitos

* [Inno Setup 6](https://jrsoftware.org/isdl.php)

### Gerar o instalador

```bash
# 1. Gere o executável primeiro
pyinstaller AutoWall.spec --noconfirm

# 2. Compile o instalador
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

**Saída:**

```
installer_output/AutoWall_Setup_v1.0.0.exe
```

O instalador:

* Instala em `C:\PlaylistTools\AutoWall` por padrão
* Cria atalho no Menu Iniciar
* Cria atalho na Área de Trabalho (opcional)
* Registra o desinstalador no Painel de Controle
* Suporte a português (BR) e inglês

---

## ⚠️ Observações

* O aplicativo cria regras para todos os perfis de rede (Domain, Private e Public)
* A criação é interrompida automaticamente em caso de erro de validação
* O Windows SmartScreen pode exibir aviso para executáveis não assinados digitalmente

---

## 📁 Estrutura do projeto

```
autowall.py        # Código principal
AutoWall.spec      # Configuração de build (PyInstaller)
installer.iss      # Script do instalador (Inno Setup)
autowall.ico       # Ícone do aplicativo (janela, .exe e instalador)
autowall_logo.png  # Logo oficial (fonte do ícone)
make_icon.py       # Gera o autowall.ico a partir do logo
LICENSE.txt        # Licença
.gitignore         # Arquivos ignorados
```

> Para regenerar o ícone após trocar o logo: substitua `autowall_logo.png`
> e rode `python make_icon.py` (requer Pillow: `pip install pillow`).

---

## 🔐 Considerações de segurança

* O AutoWall **não remove regras existentes**
* As regras são criadas com base no nome informado, evitando conflitos diretos
* Nenhuma configuração global do firewall é alterada

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

---

## 📬 Contribuição

Contribuições são bem-vindas!
Sinta-se à vontade para abrir issues ou pull requests.
