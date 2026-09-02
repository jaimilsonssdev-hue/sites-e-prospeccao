---
name: maquina-de-sites
description: Automação completa para prospecção de leads locais com Jina AI, geração de sites de alta conversão com Tailwind CSS e publicação automática no Cloudflare Pages.
---

# Skill: Máquina de Sites Automática

Esta skill capacita o agente a criar, personalizar e publicar Landing Pages comerciais completas em massa para empresas locais que não possuem site.

## Fluxo Operacional

```
Prospecção (Jina AI) ➔ Geração dos Sites (5 Heros + Tailwind) ➔ Deploy Cloudflare Pages ➔ Planilha leads_prontos.xlsx
```

## Como Usar via Terminal

Para gerar sites automaticamente para qualquer nicho e cidade:

```bash
# Exemplo 1: Odontologia em Belo Horizonte
python painel_vendas.py --nicho "Odontologia" --cidade "Belo Horizonte, MG" --qtd 5

# Exemplo 2: Pizzaria em Curitiba
python painel_vendas.py --nicho "Pizzaria" --cidade "Curitiba, PR" --qtd 5

# Exemplo 3: Estética em São Paulo
python painel_vendas.py --nicho "Estética" --cidade "São Paulo, SP" --qtd 5
```

## Arquitetura de Heros Aplicada

A esteira alterna ciclicamente entre as 5 arquiteturas de hero do Kit para que cada proposta comercial seja única:
1. **ASYMMETRIC**: Clipping diagonal moderno com foto à direita e cards flutuantes.
2. **SPLIT**: Layout 2 colunas lado a lado balanceado e corporativo.
3. **IMMERSIVE**: Full-bleed fotográfico escurecido de alto impacto.
4. **CENTERED**: Layout centralizado com autoridade e selos de avaliação.
5. **TYPOGRAPHIC**: Tipografia marcante e minimalista.

## Arquivos e Estrutura

- `prospeccao.py`: Busca empresas locais no Google Maps e web usando Jina AI Search/Reader.
- `template_base.html`: Template responsivo com Tailwind CSS CDN e paletas HSL dinâmicas.
- `gerador_e_deploy.py`: Cria as páginas em `public/sites/<slug>/index.html` e dispara `npx wrangler pages deploy`.
- `painel_vendas.py`: Orquestrador que gera a planilha `leads_prontos.xlsx` com colunas:
  `[Nome da Empresa] | [Telefone] | [Link do Site Publicado]`.

