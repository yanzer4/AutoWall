Segue uma versão **reescrita, mais profissional e pronta para GitHub**, mantendo sua ideia original, mas com melhor estrutura, clareza e credibilidade:

---

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

* Validação de entrada:

  * Verifica formato das portas
  * Identifica caracteres inválidos no nome da regra (com código Unicode)

* Segurança:

  * Bloqueia criação em caso de erro
  * Executa com privilégios de administrador (UAC)

---

## 🧠 Como funciona

O AutoWall utiliza comandos do PowerShell (`New-NetFirewallRule`) para criar automaticamente regras de entrada e saída no Windows Firewall.

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

* Windows 10 ou Windows 11
* PowerShell disponível no sistema
* Permissão de administrador

---

## ▶️ Como usar (executável)

1. Acesse a aba **Releases** do repositório
2. Baixe o arquivo `AutoWall.exe`
3. Execute o arquivo e aceite o prompt de administrador (UAC)
4. Preencha:

   * Nome base da regra
   * Porta(s) (ex: `8080,8443,3030-3040`)
5. Clique em **Criar regras no Firewall**

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

### Build rápido:

```bash
venv\Scripts\pyinstaller.exe --noconfirm --clean --onefile --windowed --name AutoWall --uac-admin autowall.py
```

**Saída:**

```
dist/AutoWall.exe
```

---

## ⚠️ Observações

* O aplicativo cria regras para todos os perfis de rede (Domain, Private e Public)
* A criação é interrompida automaticamente em caso de erro de validação
* O Windows SmartScreen pode exibir aviso para executáveis não assinados digitalmente

---

## 📁 Estrutura do projeto

```
autowall.py        # Código principal
AutoWall.spec      # Configuração de build
.gitignore         # Arquivos ignorados
```

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

---

Se quiser, posso dar um próximo passo contigo:
👉 melhorar ainda mais (nível open source forte, com badges, screenshots e UX polish)
👉 ou revisar o código do `autowall.py` pra alinhar com esse nível de README
