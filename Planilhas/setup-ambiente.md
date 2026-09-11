# Setup do Ambiente — Pré-Requisitos e Instalação

Antes de começar a criar sites, você precisa verificar se tem as ferramentas instaladas no seu computador.

---

## ✅ Verificar Se Tem Instalado

Execute estes comandos no terminal/prompt para ver se as ferramentas já estão na sua máquina.

### 1️⃣ Verificar Git

```bash
git --version
```

**Esperado:** Algo como `git version 2.34.0` ou superior

Se retornar erro ou comando não encontrado → [Baixar Git](#baixar-git)

---

### 2️⃣ Verificar Node.js

```bash
node --version
npm --version
```

**Esperado:**
- `v16.0.0` ou superior (preferencialmente v18+)
- npm `v7.0.0` ou superior

Se retornar erro ou comando não encontrado → [Baixar Node.js](#baixar-nodejs)

---

## 📥 Baixar e Instalar

### Baixar Git

🔗 **Link oficial:** https://git-scm.com/

1. Acesse o site acima
2. Clique em "Downloads"
3. Escolha seu sistema operacional (Windows, Mac, Linux)
4. Baixe e execute o instalador
5. Siga os passos padrão (pode aceitar tudo com "Next")
6. Após instalar, abra um novo terminal e execute:
   ```bash
   git --version
   ```

---

### Baixar Node.js

🔗 **Link oficial:** https://nodejs.org/

1. Acesse o site acima
2. Você verá duas versões:
   - **LTS** (Recomendado) — mais estável
   - **Current** — mais recente mas pode ter bugs
3. Clique em **LTS**
4. Baixe para seu sistema operacional
5. Execute o instalador e siga os passos
6. Após instalar, abra um novo terminal e execute:
   ```bash
   node --version
   npm --version
   ```

---

## 🎯 Instalar Claude Code no VS Code

Claude Code é uma extensão que você usa dentro do VS Code para gerar e editar código com IA.

### Passo 1: Ter VS Code Instalado

Se não tem VS Code, baixe em: https://code.visualstudio.com/

### Passo 2: Instalar a Extensão

**Opção A — Pelo marketplace (mais fácil):**

1. Abra VS Code
2. Clique no ícone de extensões (quadradinho à esquerda)
3. Na barra de busca, digite: `claude code`
4. Procure por "Claude" (oficial da Anthropic)
5. Clique em "Install"

**Opção B — Pelo terminal:**

```bash
code --install-extension Anthropic.claude
```

### Passo 3: Fazer Login

1. Após instalar, clique no ícone do Claude (à esquerda do VS Code)
2. Clique em "Sign In"
3. Authorize na página que abrir
4. Pronto! Você pode começar a usar

---

## 🧪 Testar Se Tudo Funciona

Execute os 3 comandos abaixo. Se todos retornarem números de versão, você está pronto!

```bash
git --version
node --version
npm --version
```

Se algum retornar erro, volte à seção "Baixar e Instalar" acima.

---

## 🚀 Próximos Passos

Depois que verificar tudo:

1. Abra o terminal na pasta onde quer trabalhar
2. Execute:
   ```bash
   git init
   ```
3. Use Claude Code para gerar os sites (arquivo `gen.py`)
4. Suba para GitHub Pages (arquivo `enviar_real.py`)

---

## ❓ Dúvidas Frequentes

**P: Instalei mas o terminal ainda não reconhece?**  
R: Feche e abra um novo terminal. Às vezes precisa reiniciar.

**P: Qual versão de Node.js devo instalar?**  
R: A LTS (Long Term Support) é a mais segura. Atualmente é v20.x

**P: Posso usar outro editor ao invés de VS Code?**  
R: Sim, mas Claude Code só funciona em VS Code. Você pode usar outro editor, mas vai perder a IA.

**P: O que é npm?**  
R: É o gerenciador de pacotes do Node. Vem junto quando você instala Node.js.

---

**Pronto?** Abra o arquivo `README.md` e comece! 🎓
