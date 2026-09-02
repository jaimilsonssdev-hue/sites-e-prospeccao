# 🚀 Kit do Aluno — Automação de Criação de Sites

Bem-vindo ao **Kit Completo de Treinamento**! Aqui você encontra tudo que precisa para criar e entregar sites em massa de forma automática.

## 📁 Estrutura do Kit

```
Kit do Aluno/
├── roteiro_sites.html          ← COMECE AQUI! Guia interativo passo a passo
├── README.md                   ← Este arquivo
│
├── Scripts/
│   ├── gen.py                  ← Gerador Python (template comentado)
│   └── enviar_real.py          ← Script de envio WhatsApp (template comentado)
│
├── Planilhas/
│   ├── modelo_leads.csv        ← Exemplo de planilha de leads
│   └── setup-ambiente.md       ← Pré-requisitos e instalação de ferramentas
│
├── Documentação/
│   ├── SKILL.md                ← O que é a Skill e como usar
│   ├── hero-architectures.md   ← As 5 arquiteturas de hero
│   └── design-system.md        ← Sistema de cores, tipografia e componentes
│
└── Exemplos de Sites/
    ├── Frutayce/index.html              ← Exemplo 1 (Bebidas)
    ├── Hype Drink/index.html            ← Exemplo 2 (Produto)
    ├── Advocacia Brasil/index.html      ← Exemplo 3 (Advocacia)
    ├── Nova Face Clean/index.html       ← Exemplo 4 (Estética)
    └── Carmed Cimed/index.html          ← Exemplo 5 (Campanha/Marca)
```

## ✅ Pré-Requisitos

Antes de começar, certifique-se que tem as ferramentas instaladas:

- ✅ **Git** — Para controle de versão
- ✅ **Node.js (v16+)** — Runtime para scripts
- ✅ **Python 3.9+** — Para os scripts de geração
- ✅ **VS Code** — Editor com Claude Code (IA)

**Não tem instalado?** Acesse `Planilhas/setup-ambiente.md` para:
- Verificar quais ferramentas já tem
- Baixar as que faltam
- Testar se tudo funciona

---

## 🎯 Como Usar Este Kit

### 1️⃣ **Primeira Vez? Abra o Roteiro**
```
Abra: roteiro_sites.html (duplo clique)
```
Este arquivo HTML interativo te guia através de todos os 10 passos. Ele:
- Explica cada ferramenta (Skill, MCPs, Integrações)
- Mostra como instalar tudo
- Tem um checklist para você acompanhar o progresso

### 2️⃣ **Estude a Documentação**
Leia os arquivos em `Documentação/` para entender:
- Como a Skill funciona
- Quais são as 5 arquiteturas de hero
- Qual é o design system (cores, fontes, espaçamento)

### 3️⃣ **Veja os Exemplos**
Abra os 5 sites em `Exemplos de Sites/` no navegador:
- Cada um usa uma arquitetura de hero DIFERENTE
- Estude como eles são estruturados
- Use como referência para seus próprios sites

### 4️⃣ **Prepare Sua Planilha de Leads**
Use `Planilhas/modelo_leads.csv` como base:
- Copie e adapte para seu nicho
- Preencha com dados reais do Google Maps
- Garanta que cada empresa tem mínimo 8 avaliações

### 5️⃣ **Crie Seus Scripts Python**
Use os templates em `Scripts/`:
- `gen.py` → Adapte para seu nicho específico
- `enviar_real.py` → Configure com seus dados de Z-API

### 6️⃣ **Execute o Fluxo**
Siga o roteiro interativo até completar os 10 passos:
1. Montar planilha
2. Instalar Chrome DevTools MCP
3. Estudar Skill
4. Criar gerador Python
5. Executar gerador
6. Testar com Chrome DevTools
7. Publicar no GitHub Pages
8. Conectar Z-API
9. Criar script de envio
10. Executar envios

## ⚠️ Regras Importantes

✅ **Sempre:**
- Use dados REAIS do Google Maps
- Cada site com uma hero DIFERENTE (não repetir consecutivas)
- Delay de 100-140s entre envios WhatsApp
- Screenshots de preview ANTES de publicar

❌ **Nunca:**
- Inventar depoimentos ou avaliações fictícias
- Inferir números de telefone (sempre perguntar)
- Usar em dashes (travessões) no texto
- Publicar sites via Artifact (risco de impersonação)

## 🛠️ Tecnologias Necessárias

| Ferramenta | Tipo | Status |
|---|---|---|
| Skill-sites-prospeccao | Skill | ✅ Instalada no seu Claude Code |
| Chrome DevTools MCP | MCP | 📥 Instalar via `npx @modelcontextprotocol/server-chrome-devtools` |
| Jina AI MCP | MCP | 📥 Instalar via `npx @jina-ai/mcp-server` |
| GitHub Pages | Integração | 🌐 Criar repositório público |
| Z-API WhatsApp | Integração | 🔐 Criar conta em z-api.io |
| Python 3.9+ | Runtime | 💻 Instalado no seu computador |

## 📊 Fluxo Resumido

```
Planilha de Leads
    ↓
Extração de Dados (Jina MCP)
    ↓
Geração de HTML (gen.py + Skill)
    ↓
Screenshots (Chrome DevTools MCP)
    ↓
Publicação (GitHub Pages)
    ↓
Envio de Mensagens (Z-API + enviar_real.py)
    ↓
✅ Sites entregues aos clientes!
```

## 📚 Exemplos Inclusos

Este kit vem com **5 sites de bônus** já prontos:

1. **Site 1** — Hero ASYMMETRIC (clipping diagonal, foto à direita)
2. **Site 2** — Hero SPLIT (layout lado a lado)
3. **Site 3** — Hero IMMERSIVE (full-bleed com imagem de fundo)
4. **Site 4** — Hero CENTERED (centralizado com stats)
5. **Site 5** — Hero TYPOGRAPHIC (tipografia pesada, sem foto)

Abra cada um e analise como são construídos. Use-os como base para seus próprios sites!

## 🎓 Tempo de Implementação

- **Setup inicial:** 30-45 min (instalar MCPs, criar contas)
- **Criar 10 sites:** 70 min (7 min/site)
- **Publicar + Testar:** 20 min
- **Enviar via WhatsApp:** 20 min (delays de segurança)

**Total:** ~2-3 horas para criar e entregar 10 sites.

## ❓ Dúvidas Comuns

**P: Preciso saber programar?**
R: Não! O gerador Python é um template que você só precisa adaptar. Maioria é copy-paste.

**P: Funciona com qualquer nicho?**
R: Sim! Adapte o copy, paleta e especialmente o formulário de contato para seu nicho.

**P: Posso modificar os exemplos?**
R: Sim! Use-os como base. Mude cores, textos, fotos — a estrutura HTML é reutilizável.

**P: E se um lead não quiser o site?**
R: Tudo bem! O site é um mockup de proposta. Se não quiser, você tem economia de tempo. Se quiser, já está pronto.

---

**Desenvolvido por:** Anderson Braga | SB Business  
**Última atualização:** Agosto 2026

Boa sorte! 🚀
