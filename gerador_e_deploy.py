#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
MÁQUINA DE SITES — GERADOR EM MASSA & DEPLOY NO CLOUDFLARE PAGES
==============================================================================
Este script realiza:
1. Leitura dos leads prospectados
2. Rotação das 5 Arquiteturas de Hero (Asymmetric, Split, Immersive, Centered, Typographic)
3. Geração de paletas HSL dinâmicas e cards de produtos personalizados por nicho
4. Injeção de dados no template_base.html
5. Salvamento na pasta /public/sites/<slug>/index.html
6. Deploy automático no Cloudflare Pages via Wrangler:
   npx wrangler pages deploy public --project-name=minha-maquina
7. Extração do link final publicado por lead
==============================================================================
"""

import os
import sys
import re
import json
import shutil
import subprocess
import urllib.parse
import html as html_lib
from datetime import datetime
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# Arquiteturas de Hero recomendadas pelo Kit
HERO_TYPES = [
    "ASYMMETRIC",
    "SPLIT",
    "IMMERSIVE",
    "CENTERED",
    "TYPOGRAPHIC"
]

# Paletas de cores HUE base por nicho (19 Nichos Canônicos)
HUE_POR_NICHO = {
    "loja": 260,         # Roxo / Magenta moderno
    "delivery": 20,       # Laranja avermelhado apetitoso
    "restaurante": 28,   # Âmbar / Terracota gourmet
    "sorveteria": 195,   # Turquesa / Ciano refrescante
    "oficina": 25,       # Laranja mecânico / Grafite
    "clinica": 175,      # Verde médico / Saúde
    "psicologia": 165,   # Verde sálvia equilíbrio
    "petshop": 145,      # Verde natureza pet
    "advocacia": 275,    # Azul marinho / Índigo formal
    "odontologia": 195,  # Azul dental / Turquesa
    "construcao": 28,    # Terracota / Ocre construção
    "imobiliaria": 215,  # Azul imobiliário
    "seguros": 160,      # Verde esmeralda proteção
    "autonomo": 220,     # Azul aço / Técnico
    "pessoal": 280,      # Violeta autoridade
    "fitness": 12,       # Vermelho / Laranja energia
    "nutricao": 135,     # Verde lima / Saúde
    "costura": 330,      # Rosé gold / Elegância
    "tecnologia": 215,   # Azul neon / TI
    "geral": 200         # Azul corporativo
}

def gerar_svg_hero(nicho: str, empresa: str) -> str:
    """Gera um banner visual em SVG Data-URI com gradiente mesh vetorial e monograma institucional."""
    import urllib.parse
    cores = {
        "loja": ("#1e1b4b", "#4338ca", "#065f46", "#34d399", "LOJA & E-COMMERCE OFICIAL"),
        "delivery": ("#450a0a", "#b91c1c", "#d97706", "#fbbf24", "DELIVERY RÁPIDO & PEDIDOS"),
        "restaurante": ("#1c1917", "#78350f", "#991b1b", "#f59e0b", "GASTRONOMIA & RESTAURANTE"),
        "sorveteria": ("#083344", "#0284c7", "#db2777", "#38bdf8", "GELATERIA & AÇAÍ GOURMET"),
        "oficina": ("#0f172a", "#1e293b", "#c2410c", "#f97316", "OFICINA MECÂNICA & AUTO CENTER"),
        "clinica": ("#042f2e", "#0f766e", "#0284c7", "#2dd4bf", "SAÚDE & CLÍNICA MÉDICA"),
        "psicologia": ("#064e3b", "#047857", "#0f766e", "#6ee7b7", "PSICOLOGIA & ACOLHIMENTO"),
        "petshop": ("#14532d", "#15803d", "#b45309", "#facc15", "PET SHOP & CUIDADO ANIMAL"),
        "advocacia": ("#09090b", "#18181b", "#3b0764", "#fbbf24", "ADVOCACIA & CONSULTORIA JURÍDICA"),
        "odontologia": ("#082f49", "#0284c7", "#0f766e", "#38bdf8", "ODONTOLOGIA & ESTÉTICA DENTAL"),
        "construcao": ("#1c1917", "#44403c", "#9a3412", "#fb923c", "CONSTRUÇÃO CIVIL & REFORMAS"),
        "imobiliaria": ("#0f172a", "#1e3a8a", "#0369a1", "#60a5fa", "IMOBILIÁRIA & CORRETORES"),
        "seguros": ("#022c22", "#065f46", "#1e3a8a", "#34d399", "CORRETORA DE SEGUROS"),
        "autonomo": ("#18181b", "#27272a", "#3f3f46", "#a1a1aa", "SERVIÇOS TÉCNICOS AUTÔNOMO"),
        "pessoal": ("#18181b", "#312e81", "#581c87", "#c084fc", "PÁGINA PESSOAL & PORTFÓLIO"),
        "fitness": ("#18181b", "#7f1d1d", "#991b1b", "#ef4444", "FITNESS & PERSONAL TRAINER"),
        "nutricao": ("#052e16", "#166534", "#047857", "#86efac", "NUTRICIONISTA & DIETAS"),
        "costura": ("#2e1065", "#581c87", "#831843", "#f472b6", "ATELIÊ DE COSTURA & MODA"),
        "tecnologia": ("#030712", "#111827", "#1e1b4b", "#38bdf8", "TECNOLOGIA & INFORMÁTICA"),
        "geral": ("#09090b", "#1e293b", "#172554", "#60a5fa", "EMPRESA VERIFICADA")
    }
    c1, c2, c3, acc, label = cores.get(nicho, cores["geral"])
    safe_empresa = (empresa or "Nossa Empresa").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    palavras = safe_empresa.split()
    initials = "".join([w[0] for w in palavras[:2]]).upper() if palavras else "NE"
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="100%" height="100%">
      <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="{c1}"/>
          <stop offset="50%" stop-color="{c2}"/>
          <stop offset="100%" stop-color="{c3}"/>
        </linearGradient>
        <radialGradient id="glow" cx="30%" cy="30%" r="70%">
          <stop offset="0%" stop-color="{acc}" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="#000000" stop-opacity="0.5"/>
        </radialGradient>
      </defs>
      <rect width="1200" height="800" fill="url(#bg)"/>
      <rect width="1200" height="800" fill="url(#glow)"/>
      <g transform="translate(600, 320)">
        <circle cx="0" cy="0" r="130" fill="#000000" fill-opacity="0.3" stroke="{acc}" stroke-width="4" stroke-opacity="0.8"/>
        <text x="0" y="32" font-family="system-ui, sans-serif" font-size="96" font-weight="900" fill="#ffffff" text-anchor="middle">{initials}</text>
      </g>
      <text x="600" y="520" font-family="system-ui, sans-serif" font-size="20" font-weight="800" fill="{acc}" text-anchor="middle" letter-spacing="4">{label}</text>
      <text x="600" y="570" font-family="system-ui, sans-serif" font-size="44" font-weight="900" fill="#ffffff" text-anchor="middle">{safe_empresa}</text>
      <text x="600" y="615" font-family="system-ui, sans-serif" font-size="18" font-weight="500" fill="#cbd5e1" text-anchor="middle">ATENDIMENTO EXCLUSIVO &bull; QUALIDADE COMPROVADA</text>
    </svg>"""
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)

# Imagens de alta conversão no Unsplash por nicho (curadoria comercial profissional)
IMAGENS_NICHO = {
    "loja": {
        "hero": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=800&q=80"
    },
    "delivery": {
        "hero": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80"
    },
    "restaurante": {
        "hero": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80"
    },
    "sorveteria": {
        "hero": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?auto=format&fit=crop&w=800&q=80"
    },
    "oficina": {
        "hero": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80"
    },
    "clinica": {
        "hero": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=800&q=80"
    },
    "psicologia": {
        "hero": "https://images.unsplash.com/photo-1527689368864-3a821dbccc34?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=800&q=80"
    },
    "petshop": {
        "hero": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=800&q=80"
    },
    "advocacia": {
        "hero": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80"
    },
    "odontologia": {
        "hero": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=800&q=80"
    },
    "construcao": {
        "hero": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=800&q=80"
    },
    "imobiliaria": {
        "hero": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80"
    },
    "seguros": {
        "hero": "https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80"
    },
    "autonomo": {
        "hero": "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80"
    },
    "pessoal": {
        "hero": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=800&q=80"
    },
    "fitness": {
        "hero": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80"
    },
    "nutricao": {
        "hero": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80"
    },
    "costura": {
        "hero": "https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?auto=format&fit=crop&w=800&q=80"
    },
    "tecnologia": {
        "hero": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1588508065123-287b28e013da?auto=format&fit=crop&w=800&q=80"
    },
    "geral": {
        "hero": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80"
    }
}

def identificar_nicho_chave(nicho: str, empresa: str = "") -> str:
    """Normaliza e identifica a chave canônica do nicho entre os 19 nichos oficiais."""
    texto = f"{nicho or ''} {empresa or ''}".lower()
    
    # 1. Delivery & Lanches
    if any(k in texto for k in ["delivery", "pizz", "burg", "hamburg", "lanche", "marmit", "ifood", "entreg"]):
        return "delivery"
    # 2. Sorveteria & Doces
    elif any(k in texto for k in ["sorvet", "açai", "acai", "gelat", "palet", "picol", "confeit", "docer"]):
        return "sorveteria"
    # 3. Restaurante & Gastronomia
    elif any(k in texto for k in ["restaur", "gastro", "bistr", "churrasc", "buffet", "sushi", "almoco", "comida", "caf"]):
        return "restaurante"
    # 4. Odontologia
    elif any(k in texto for k in ["odonto", "dent", "sorris", "dente", "protese", "implant", "ortodont", "clareament"]):
        return "odontologia"
    # 5. Terapeutas / Psicólogos
    elif any(k in texto for k in ["psico", "terap", "mente", "emocional", "psicanal", "acolhiment", "psiquiatr", "mindfulness", "saude mental"]):
        return "psicologia"
    # 6. Saúde / Clínica Médica
    elif any(k in texto for k in ["clinic", "medic", "saud", "hospital", "policlinic", "doutor", "dra", "fisio", "estet", "dermat", "biomed"]):
        return "clinica"
    # 7. PetShop / Casa de Ração
    elif any(k in texto for k in ["pet", "vet", "animal", "banho e tosa", "canil", "racao", "tosa", "veterin"]):
        return "petshop"
    # 8. Oficina Mecânica & Auto Center
    elif any(k in texto for k in ["oficin", "mecan", "auto", "pneu", "carro", "veic", "freio", "suspens", "troca de oleo", "auto center", "funilari"]):
        return "oficina"
    # 9. Construção Civil & Reformas
    elif any(k in texto for k in ["constru", "reforma", "obra", "engenh", "arquit", "eletric", "pedreir", "pintor", "pintura", "marcen"]):
        return "construcao"
    # 10. Imobiliária & Corretores
    elif any(k in texto for k in ["imob", "corret", "imove", "creci", "locacao", "aluguel", "condominio", "apartamento"]):
        return "imobiliaria"
    # 11. Seguros & Previdência
    elif any(k in texto for k in ["segur", "apolice", "sinistro", "previdenci", "vida e saude", "corretora de seguro"]):
        return "seguros"
    # 12. Advocacia & Jurídico
    elif any(k in texto for k in ["advoc", "jurid", "direito", "lei", "oab"]):
        return "advocacia"
    # 13. Fitness & Treinamento
    elif any(k in texto for k in ["acad", "fit", "cross", "trein", "muscul", "personal", "gym", "pilat", "luta", "boxe"]):
        return "fitness"
    # 14. Nutricionista & Dietas
    elif any(k in texto for k in ["nutri", "dieta", "emagrec", "reeducacao alimentar", "nutrol"]):
        return "nutricao"
    # 15. Costureira / Ateliê
    elif any(k in texto for k in ["costur", "atelie", "alfaiat", "ajuste de roupa", "vestido", "moda sob medida", "bainha"]):
        return "costura"
    # 16. Tecnologia & Informática
    elif any(k in texto for k in ["tecnolog", "informatic", "software", "computad", "notebook", "celular", "assistencia tecnica", "redes", "ti ", "t.i", "program"]):
        return "tecnologia"
    # 17. Profissional Autônomo & Serviços Gerais
    elif any(k in texto for k in ["autonom", "servico", "consultor", "chaveir", "montador", "marido de aluguel", "diarist", "limpeza", "contab", "contador", "despachant"]):
        return "autonomo"
    # 18. Pessoal & Portfólio
    elif any(k in texto for k in ["pessoal", "portfoli", "curriculo", "palestrant", "influencer", "criador", "artista", "tatuag", "tattoo"]):
        return "pessoal"
    # 19. Lojas & E-commerce
    elif any(k in texto for k in ["loj", "varej", "boutiq", "calc", "roup", "moda", "presentes", "cosmetic", "perfum", "vestuari", "biju", "salao", "barb", "otica", "e-commerce", "ecommerce"]):
        return "loja"
    
    return "geral"

def obter_imagens_nicho(nicho: str, empresa: str = "") -> dict:
    """Retorna imagens profissionais de alta conversão para o nicho correto, evitando escritórios genéricos."""
    chave = identificar_nicho_chave(nicho, empresa)
    return IMAGENS_NICHO.get(chave, IMAGENS_NICHO["geral"])

def obter_copy_hero_nicho(chave: str, lead: dict) -> tuple:
    """Gera badge, título e descrição de alto impacto comercial específicos para o nicho."""
    empresa = lead["empresa"]
    nicho = lead["nicho"]
    bairro = lead.get("bairro") or lead.get("cidade", "")
    cidade = lead.get("cidade", "")
    nota = lead.get("nota", "5.0")
    
    if chave == "loja":
        badge = f"Tendências & Novidades no {bairro}"
        desc = f"Coleções exclusivas, atendimento atencioso e produtos selecionados para encantar você em {cidade}. Compre com facilidade e segurança."
        titulo = f"Estilo, Novidades e Qualidade na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "delivery":
        badge = f"Delivery Rápido & Quentinho no {bairro}"
        desc = f"Pratos preparados com ingredientes frescos, embalagens térmicas seguras e entrega ágil para você saborear no conforto de casa em {cidade}."
        titulo = f"Sabor Irresistível e Rapidez na Sua Porta com a <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "restaurante":
        badge = f"Alta Gastronomia & Sabor no {bairro}"
        desc = f"Ingredientes frescos, receitas artesanais nobres e a melhor experiência de sabor em {cidade}. Ambiente acolhedor para família e amigos."
        titulo = f"Sabor Único e Experiência Inesquecível no <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "sorveteria":
        badge = f"Gelatos Artesanais & Açaí Nobre no {bairro}"
        desc = f"Receitas cremosas preparadas artesanalmente com frutas frescas e ingredientes de verdade em {cidade}. Momentos doces para o seu dia."
        titulo = f"O Mais Puro Sabor Refrescante na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "oficina":
        badge = f"Centro Automotivo de Precisão no {bairro}"
        desc = f"Diagnóstico computadorizado, peças originais com garantia e transparência total na manutenção do seu veículo em {cidade}."
        titulo = f"Segurança e Precisão Mecânica na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "clinica":
        badge = f"Medicina Integrada & Saúde no {bairro}"
        desc = f"Corpo clínico qualificado, exames diagnósticos e atendimento humanizado para você e sua família em {cidade}."
        titulo = f"Saúde, Confiança e Cuidado na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "psicologia":
        badge = f"Acolhimento & Saúde Emocional no {bairro}"
        desc = f"Um espaço seguro, ético e acolhedor para cuidar do seu bem-estar emocional, autoconhecimento e equilíbrio em {cidade}. Agende sua sessão com tranquilidade."
        titulo = f"Cuidado, Escuta e Transformação na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "petshop":
        badge = f"Carinho & Cuidado Animal no {bairro}"
        desc = f"Atendimento carinhoso, estética especializada e cuidado completo que seu pet realmente merece em {cidade}."
        titulo = f"Amor, Saúde e Cuidado Animal na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "advocacia":
        badge = f"Autoridade Jurídica & Rigor no {bairro}"
        desc = f"Defesa técnica de direitos, proteção patrimonial e assessoria jurídica transparente para seus interesses em {cidade}."
        titulo = f"Segurança Jurídica e Firmeza na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "odontologia":
        badge = f"Referência em Odontologia no {bairro}"
        desc = f"Tecnologia odontológica de ponta, tratamentos estéticos e prevenção para você sorrir com total confiança em {cidade}."
        titulo = f"Excelência e Saúde para o Seu Sorriso na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "construcao":
        badge = f"Obras de Confiança & Engenharia no {bairro}"
        desc = f"Gestão integral de obras, cumprimento rigoroso de prazos e acabamentos de alto padrão em {cidade}. Engenharia que valoriza seu patrimônio."
        titulo = f"Construções Sólidas e Reformas Impecáveis na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "imobiliaria":
        badge = f"Imóveis Selecionados no {bairro}"
        desc = f"As melhores oportunidades de compra, venda e locação com assessoria jurídica e segurança documental em {cidade}."
        titulo = f"O Imóvel Perfeito para Sua Família na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "seguros":
        badge = f"Proteção Patrimonial & Tranquilidade no {bairro}"
        desc = f"Consultoria especializada em seguros para vida, veículos, empresas e residências em {cidade}. Tranquilidade com suporte imediato em sinistros."
        titulo = f"Segurança Absoluta para o que Mais Importa na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "autonomo":
        badge = f"Serviço Especializado & Pontual no {bairro}"
        desc = f"Atendimento ágil, pontualidade britânica e serviço de qualidade para resolver sua necessidade com total garantia em {cidade}."
        titulo = f"Solução Rápida, Prática e Garantida com <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "pessoal":
        badge = f"Autoridade & Conexão no {bairro}"
        desc = f"Portfólio de projetos, formação e soluções desenvolvidas com paixão, técnica e autenticidade para impactar pessoas em {cidade} e online."
        titulo = f"Conheça a Trajetória e o Trabalho de <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "fitness":
        badge = f"Treino & Alta Performance no {bairro}"
        desc = f"Estrutura completa, suporte profissional e motivação diária para você superar seus limites e alcançar resultados em {cidade}."
        titulo = f"Força, Saúde e Alta Performance na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "nutricao":
        badge = f"Nutrição Científica & Saúde no {bairro}"
        desc = f"Planos alimentares prazerosos, personalizados e sem radicalismos para você atingir seu peso ideal com saúde e vitalidade em {cidade}."
        titulo = f"Alimentação Equilibrada e Energia na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "costura":
        badge = f"Ateliê de Costura & Alta Costura no {bairro}"
        desc = f"Costura refinada, ajustes impecáveis e peças sob medida feitas com dedicação e carinho para valorizar sua elegância em {cidade}."
        titulo = f"Ajustes Precisos e Caimento Perfeito na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    elif chave == "tecnologia":
        badge = f"Tecnologia & Inovação no {bairro}"
        desc = f"Manutenção de computadores, suporte de TI ágil e soluções tecnológicas sob medida para sua empresa ou residência em {cidade}."
        titulo = f"Soluções Digitais e Suporte Especializado na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
    else:
        badge = f"Referência em {nicho} no {bairro}"
        desc = f"Conheça o padrão de qualidade que conquistou nota {nota} estrelas no Google em {cidade}. Agende ou tire dúvidas diretamente pelo WhatsApp."
        titulo = f"Excelência e Cuidado para você na <span class=\"text-[var(--color-400)]\">{empresa}</span>"
        
    return badge, titulo, desc

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def gerar_paleta_hsl(hue):
    """
    Gera as 9 escalas de luminosidade HSL conforme o design system do Kit
    """
    saturation = 75
    palette = {}
    for level, lightness in [
        ("900", 15), ("800", 25), ("700", 35),
        ("600", 45), ("500", 55), ("400", 65),
        ("300", 75), ("200", 85), ("100", 95)
    ]:
        palette[f"PALETA_{level}"] = f"hsl({hue}, {saturation}%, {lightness}%)"
    return palette

def slugify(text):
    """Transforma texto em slug limpo para URL e diretórios"""
    text = text.lower().strip()
    text = re.sub(r'[áàãâä]', 'a', text)
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[íìîï]', 'i', text)
    text = re.sub(r'[óòõôö]', 'o', text)
    text = re.sub(r'[úùûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def gerar_cards_servicos(nicho: str, empresa: str = ""):
    """Gera layout Bento Grid de alta conversão para serviços em TODOS os nichos."""
    chave = identificar_nicho_chave(nicho, empresa)
    
    if chave == "loja":
        s1 = ("fa-bag-shopping", "Coleção Exclusiva & Novidades da Estação", "Peças selecionadas alinhadas às maiores tendências de estilo, conforto e durabilidade.", ["Produtos de alta durabilidade e estilo", "Envio rápido ou retirada em loja", "Atendimento humanizado via WhatsApp"])
        s2 = ("fa-shirt", "Lookbooks & Combinações Completas", "Sugestões de looks prontos para você arrasar em qualquer ocasião com elegância.")
        s3 = ("fa-gift", "Embalagens para Presente & Linha Premium", "Opções sofisticadas com atendimento consultivo para você acertar no presente ideal.")
    elif chave == "delivery":
        s1 = ("fa-motorcycle", "Delivery Expresso & Pratos Artesanais", "Peça seus pratos favoritos e receba na sua casa quentinho, com embalagem inviolável e rapidez.", ["Ingredientes frescos e selecionados", "Embalagem térmica selada", "Rastreamento do pedido pelo WhatsApp"])
        s2 = ("fa-burger", "Combos Especiais & Porções da Casa", "Combinações perfeitas para compartilhar com a família ou amigos com o melhor custo-benefício.")
        s3 = ("fa-receipt", "Cardápio Digital & Pedido Sem Espera", "Faça seu pedido diretamente pelo link ou WhatsApp em poucos segundos sem burocracia.")
    elif chave == "restaurante":
        s1 = ("fa-utensils", "Pratos Autorais & Gastronomia Especial", "Ingredientes selecionados e receitas elaboradas para proporcionar uma experiência de sabor inesquecível.", ["Ingredientes frescos e selecionados", "Ambiente climatizado e acolhedor", "Cardápio com opções variadas"])
        s2 = ("fa-bowl-food", "Almoço Executivo & Massas Especiais", "Opções saborosas e balanceadas preparadas diariamente pelo nosso chef para o seu dia a dia.")
        s3 = ("fa-wine-glass", "Sobremesas Artesanais & Carta de Bebidas", "Finalize sua refeição com doces finos, cafés especiais e bebidas harmonizadas.")
    elif chave == "sorveteria":
        s1 = ("fa-ice-cream", "Gelatos Artesanais & Sabores Nobres", "Textura supercremosa, ingredientes nobres e receitas autênticas italianas feitas diariamente.", ["Frutas frescas selecionadas", "Opções zero açúcar e sem lactose", "Casquinhas crocantes artesanais"])
        s2 = ("fa-bowl-rice", "Açaí Especial com Toppings Ilimitados", "Açaí cremoso de altíssima pureza acompanhado de frutas, cremes artesanais e coberturas crocantes.")
        s3 = ("fa-box-open", "Potes para Viagem & Sobremesas Geladas", "Leve o melhor sabor para casa com potes térmicos lacrados e tortas de gelato exclusivas.")
    elif chave == "oficina":
        s1 = ("fa-wrench", "Revisão Preventiva & Injeção Eletrônica", "Diagnóstico computadorizado de precisão para garantir a segurança e a potência original do seu carro.", ["Scanner automotivo de última geração", "Peças com garantia comprovada", "Orçamento detalhado e transparente"])
        s2 = ("fa-oil-can", "Troca de Óleo, Filtros & Fluidos", "Lubrificantes recomendados pela montadora para máxima durabilidade do motor e economia.")
        s3 = ("fa-car-burst", "Suspensão, Freios & Alinhamento 3D", "Manutenção preventiva de freios, amortecedores e geometria com tecnologia digital.")
    elif chave == "clinica":
        s1 = ("fa-stethoscope", "Consultas Médicas & Especialidades", "Avaliação clínica completa com corpo médico experiente, diagnóstico seguro e ambiente acolhedor.", ["Equipe dedicada e atenciosa", "Estrutura moderna e confortável", "Orientações preventivas contínuas"])
        s2 = ("fa-heart-pulse", "Exames Diagnósticos & Rotina", "Agilidade na realização de procedimentos para você iniciar seu tratamento sem esperas desnecessárias.")
        s3 = ("fa-user-doctor", "Acompanhamento Terapêutico & Saúde Integrada", "Planos de cuidado contínuo para garantir sua disposição e qualidade de vida permanente.")
    elif chave == "psicologia":
        s1 = ("fa-brain", "Psicoterapia Individual & Saúde Emocional", "Espaço acolhedor e seguro para trabalhar ansiedade, estresse, autoconhecimento e desenvolvimento pessoal com total sigilo ético.", ["Sessões presenciais e online", "Abordagem humanizada e acolhedora", "Sigilo e ética profissional"])
        s2 = ("fa-heart-pulse", "Terapia Cognitivo-Comportamental", "Metodologia estruturada para identificação de padrões, superação de bloqueios e inteligência emocional.")
        s3 = ("fa-handshake-angle", "Acolhimento Terapêutico & Escuta Atenta", "Atendimento sensível e empático no seu ritmo, construindo ferramentas práticas para sua qualidade de vida.")
    elif chave == "petshop":
        s1 = ("fa-paw", "Banho, Tosa Especializada & Estética Pet", "Higiene carinhosa com produtos dermatológicos hipoalergênicos, tosa na tesoura e hidratação.", ["Profissionais carinhosos e pacientes", "Produtos hipoalergênicos seguros", "Ambiente higienizado e tranquilo"])
        s2 = ("fa-shield-dog", "Consultas Veterinárias & Vacinação Importada", "Acompanhamento clínico preventivo, diagnóstico seguro e imunização completa para seu pet.")
        s3 = ("fa-bag-shopping", "Rações Super Premium & Farmácia Pet", "Medicamentos originais, alimentação especializada e acessórios para o bem-estar do seu bichinho.")
    elif chave == "advocacia":
        s1 = ("fa-scale-balanced", "Direito Civil & Proteção Patrimonial Familiar", "Planejamento sucessório, inventários e soluções ágeis para resguardar a tranquilidade da sua família.", ["Atendimento consultivo especializado", "Defesa técnica rigorosa", "Comunicação clara e transparente"])
        s2 = ("fa-briefcase", "Assessoria Trabalhista & Negócios", "Conformidade integral com as normas legais e atuação preventiva para resguardo de direitos.")
        s3 = ("fa-handshake", "Contratos & Resolução Estratégica", "Elaboração e análise técnica detalhada com cláusulas protetivas personalizadas.")
    elif chave == "odontologia":
        s1 = ("fa-tooth", "Clareamento & Estética Dental", "Técnicas modernas para devolver a harmonia, clareza e beleza natural do seu sorriso com total conforto.", ["Procedimento rápido e indolor", "Tecnologia de clareamento a laser", "Planejamento digital do sorriso"])
        s2 = ("fa-teeth-open", "Implantes & Próteses Fixas", "Recupere sua mastigação e autoconfiança com procedimentos seguros e materiais de alto padrão.")
        s3 = ("fa-shield-heart", "Prevenção & Cuidados Gerais", "Check-up completo, profilaxia detalhada e orientações de saúde bucal para toda a família.")
    elif chave == "construcao":
        s1 = ("fa-trowel-bricks", "Reformas Residenciais & Comerciais Completas", "Execução segura desde a fundação até o acabamento fino com controle rigoroso de custos e cronograma.", ["Contrato com prazos garantidos", "Equipe técnica qualificada", "Acabamento refinado de alto nível"])
        s2 = ("fa-paint-roller", "Pinturas Especiais, Drywall & Elétrica", "Instalações modernas com normas de segurança ABNT e acabamentos sofisticados sem retrabalho.")
        s3 = ("fa-helmet-safety", "Gerenciamento de Obras & Projetos Estruturais", "Acompanhamento profissional contínuo eliminando desperdício de materiais e dores de cabeça.")
    elif chave == "imobiliaria":
        s1 = ("fa-building", "Venda de Imóveis Residenciais & Alto Padrão", "Casas, apartamentos e condomínios selecionados com documentação 100% regularizada e assessoria integral.", ["Assessoria jurídica imobiliária", "Fotos e vídeos profissionais", "Atendimento personalizado e ágil"])
        s2 = ("fa-key", "Locação Ágil com Garantia Digital", "Alugue seu imóvel sem burocracia, fiador tradicional ou complicações em cartório.")
        s3 = ("fa-file-signature", "Avaliação Imobiliária de Precisão", "Análise mercadológica criteriosa para compra, venda e investimentos seguros na região.")
    elif chave == "seguros":
        s1 = ("fa-shield-halved", "Seguro Auto & Assistência 24 Horas", "Cobertura completa contra colisões, furto, terceiros e guincho com as maiores seguradoras do país.", ["Cotação comparativa em minutos", "Atendimento 24h em sinistros", "Condições personalizadas para você"])
        s2 = ("fa-house-circle-check", "Seguro Residencial & Empresarial", "Proteção essencial para seu imóvel, maquinário e patrimônio contra imprevistos climáticos e furtos.")
        s3 = ("fa-heart-pulse", "Seguro de Vida & Previdência Privada", "Segurança financeira planejada para sua família e planos sob medida para seu futuro tranquilo.")
    elif chave == "autonomo":
        s1 = ("fa-screwdriver-wrench", "Atendimento Rápido & Diagnóstico Preciso", "Resolução técnica ágil e limpa para suas demandas residenciais ou comerciais com garantia comprovada.", ["Orçamento claro e sem surpresas", "Ferramentas profissionais modernas", "Garantia formal do serviço prestado"])
        s2 = ("fa-clock", "Pontualidade & Agendamento Flexível", "Horários que se adaptam à sua rotina com atendimento prioritário para situações emergenciais.")
        s3 = ("fa-thumbs-up", "Qualidade Comprovada & Confiança", "Mais de centenas de atendimentos realizados na região com alto índice de satisfação comprovada.")
    elif chave == "pessoal":
        s1 = ("fa-user-tie", "Consultoria Individual & Mentorias", "Metodologia prática e focada no desenvolvimento de soluções sob medida para suas necessidades e metas.", ["Metodologia comprovada na prática", "Acompanhamento individualizado", "Resultados mensuráveis"])
        s2 = ("fa-folder-open", "Portfólio de Cases & Resultados", "Conheça os projetos concluídos com sucesso e a transformação gerada para clientes e parceiros.")
        s3 = ("fa-microphone", "Palestras, Workshops & Treinamentos", "Conteúdos dinâmicos e de alto impacto para eventos, equipes e encontros profissionais.")
    elif chave == "fitness":
        s1 = ("fa-dumbbell", "Musculação & Treinamento de Alta Performance", "Maquinário moderno, biomecânica precisa e suporte contínuo de instrutores para alcançar suas metas.", ["Equipamentos modernos e ergonômicos", "Ambiente climatizado e motivador", "Acompanhamento profissional"])
        s2 = ("fa-person-running", "Aulas Coletivas, Funcional & Cárdio", "Treinos dinâmicos para queima calórica, aumento de fôlego, agilidade e condicionamento integral.")
        s3 = ("fa-clipboard-check", "Avaliação Física & Treinos Personalizados", "Bioimpedância completa e periodização de treinos alinhada aos seus objetivos pessoais.")
    elif chave == "nutricao":
        s1 = ("fa-apple-whole", "Reeducação Alimentar & Emagrecimento Saudável", "Planejamento nutricional flexível que cabe na sua rotina real, sem fórmulas prontas ou restrições severas.", ["Cardápios adaptados ao seu gosto", "Acompanhamento contínuo via WhatsApp", "Avaliação por bioimpedância completa"])
        s2 = ("fa-chart-line", "Nutrição Esportiva & Ganho de Massa", "Estratégias específicas para potencializar seu rendimento no treino e acelerar a recuperação muscular.")
        s3 = ("fa-seedling", "Saúde Intestinal & Longevidade", "Manejo nutricional focado em reduzir inflamações, melhorar o sono e aumentar a disposição diária.")
    elif chave == "costura":
        s1 = ("fa-scissors", "Ajustes Finos & Reformas de Roupas", "Barras originais, ajustes de cintura, ombros e reformas completas com acabamento idêntico ao de fábrica.", ["Acabamento artesanal impecável", "Pontualidade rigorosa na entrega", "Prova presencial com ajustes na hora"])
        s2 = ("fa-vest-patches", "Confecção Sob Medida & Roupas de Festa", "Vestidos, ternos e conjuntos modelados exclusivamente para o seu corpo com tecidos nobres.")
        s3 = ("fa-needle", "Customização & Transformação de Peças", "Modernize peças antigas do seu guarda-roupa com novas modelagens e detalhes exclusivos.")
    elif chave == "tecnologia":
        s1 = ("fa-laptop-code", "Assistência Técnica & Upgrade de Computadores", "Diagnóstico avançado, formatação rápida, limpeza física e upgrade de SSD/memória para alta velocidade.", ["Peças originais com garantia", "Atendimento rápido sem perda de dados", "Laboratório técnico especializado"])
        s2 = ("fa-network-wired", "Redes, Wi-Fi & Infraestrutura de TI", "Instalação e otimização de roteadores, cabeamento estruturado e segurança para empresas e lares.")
        s3 = ("fa-shield-halved", "Segurança Digital & Recuperação de Dados", "Backup em nuvem, remoção de vírus e proteção integral contra ameaças virtuais para sua tranquilidade.")
    else:
        s1 = ("fa-star", "Atendimento Personalizado & Sob Medida", "Metodologia exclusiva focada em entregar a melhor solução para sua necessidade.", ["Padrão de qualidade superior", "Atendimento ágil e pontual", "Satisfação garantida"])
        s2 = ("fa-award", "Profissionais Capacitados", "Equipe experiente e preparada para atender com máxima atenção a você.")
        s3 = ("fa-clock-rotate-left", "Pontualidade & Compromisso", "Respeito rigoroso aos seus horários e atendimento prioritário via WhatsApp.")

    # Configuração de Botão e Subtítulo dinâmico por categoria de nicho
    if chave in ["loja", "delivery", "sorveteria", "restaurante", "petshop"]:
        if chave == "sorveteria":
            btn_cta = "Fazer Pedido no WhatsApp"
            sub_cta = "Pronto para entrega ou retirada rápida"
        elif chave == "delivery":
            btn_cta = "Fazer Pedido no Delivery"
            sub_cta = "Entrega rápida na sua casa"
        elif chave == "restaurante":
            btn_cta = "Ver Cardápio & Fazer Pedido"
            sub_cta = "Pratos frescos e reservas"
        elif chave == "loja":
            btn_cta = "Comprar pelo WhatsApp"
            sub_cta = "Atendimento direto com vendedora"
        else: # petshop
            btn_cta = "Fazer Pedido no WhatsApp"
            sub_cta = "Produtos e agendamento pet"
    elif chave in ["clinica", "odontologia", "psicologia", "nutricao", "fitness"]:
        if chave in ["psicologia", "terapeuta"]:
            btn_cta = "Agendar Sessão Terapêutica"
            sub_cta = "Atendimento presencial ou online com sigilo ético"
        elif chave == "odontologia":
            btn_cta = "Agendar Avaliação Odontológica"
            sub_cta = "Atendimento personalizado com hora marcada"
        elif chave == "nutricao":
            btn_cta = "Agendar Consulta Nutricional"
            sub_cta = "Plano individualizado com acompanhamento"
        elif chave == "fitness":
            btn_cta = "Agendar Aula Experimental"
            sub_cta = "Treinos personalizados com instrutor"
        else:
            btn_cta = "Agendar Consulta Médica"
            sub_cta = "Atendimento com hora marcada"
    elif chave == "costura":
        btn_cta = "Solicitar Ajuste no WhatsApp"
        sub_cta = "Atendimento personalizado no ateliê"
    else:
        btn_cta = "Solicitar Orçamento no WhatsApp"
        sub_cta = "Orçamento rápido sem compromisso"

    # Bento Grid HTML
    bento_html = f"""
    <!-- Card 1 (Destaque Principal - Bento Grid Span 2) -->
    <div class="md:col-span-2 bg-gradient-to-br from-white to-gray-50/80 p-8 sm:p-10 rounded-3xl border-2 border-[var(--color-300)] shadow-lg hover:shadow-xl transition-all duration-300 relative overflow-hidden flex flex-col justify-between">
      <div class="absolute top-0 right-0 w-40 h-40 bg-[var(--color-100)] rounded-full blur-3xl opacity-60 pointer-events-none"></div>
      
      <div>
        <div class="flex items-center justify-between gap-4 mb-6">
          <div class="w-14 h-14 rounded-2xl bg-[var(--color-600)] text-white flex items-center justify-center text-2xl shadow-md">
            <i class="fa-solid {s1[0]}"></i>
          </div>
          <span class="text-xs font-bold uppercase tracking-wider text-[var(--color-600)] bg-[var(--color-100)] px-3.5 py-1.5 rounded-full border border-[var(--color-200)]">
            ⭐ Serviço em Alta
          </span>
        </div>

        <h3 class="font-heading font-black text-2xl sm:text-3xl text-gray-900 mb-3">{s1[1]}</h3>
        <p class="text-gray-600 text-base leading-relaxed mb-6">{s1[2]}</p>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-8">
          <div class="flex items-center gap-2 text-xs font-semibold text-gray-700 bg-white p-3 rounded-xl border border-gray-100 shadow-sm">
            <i class="fa-solid fa-circle-check text-emerald-500"></i>
            <span>{s1[3][0]}</span>
          </div>
          <div class="flex items-center gap-2 text-xs font-semibold text-gray-700 bg-white p-3 rounded-xl border border-gray-100 shadow-sm">
            <i class="fa-solid fa-circle-check text-emerald-500"></i>
            <span>{s1[3][1]}</span>
          </div>
          <div class="flex items-center gap-2 text-xs font-semibold text-gray-700 bg-white p-3 rounded-xl border border-gray-100 shadow-sm">
            <i class="fa-solid fa-circle-check text-emerald-500"></i>
            <span>{s1[3][2]}</span>
          </div>
        </div>
      </div>

      <div class="pt-4 border-t border-gray-100 flex flex-wrap items-center justify-between gap-4">
        <a href="{{{{WHATSAPP_LINK}}}}" target="_blank" 
           class="inline-flex items-center gap-2 text-sm font-bold text-white bg-[var(--color-600)] hover:bg-[var(--color-700)] px-6 py-3 rounded-xl shadow-md hover:shadow-lg transition-all">
          <i class="fa-brands fa-whatsapp text-emerald-300"></i>
          <span>{btn_cta}</span>
        </a>
        <span class="text-xs text-gray-500 font-medium">{sub_cta}</span>
      </div>
    </div>

    <!-- Card 2 (Bento Grid Col 1) -->
    <div class="bg-white p-8 rounded-3xl border border-gray-200/80 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between">
      <div>
        <div class="w-12 h-12 rounded-2xl bg-[var(--color-100)] text-[var(--color-600)] flex items-center justify-center text-xl mb-6 shadow-inner">
          <i class="fa-solid {s2[0]}"></i>
        </div>
        <h3 class="font-heading font-black text-xl text-gray-900 mb-3">{s2[1]}</h3>
        <p class="text-gray-600 text-sm leading-relaxed mb-6">{s2[2]}</p>
      </div>
      <div class="pt-4 border-t border-gray-100">
        <a href="{{{{WHATSAPP_LINK}}}}" target="_blank" class="text-[var(--color-600)] font-bold text-sm inline-flex items-center gap-2 hover:gap-3 transition-all">
          <span>Tirar dúvidas pelo WhatsApp</span>
          <i class="fa-solid fa-arrow-right text-xs"></i>
        </a>
      </div>
    </div>

    <!-- Card 3 (Bento Grid Col 1) -->
    <div class="bg-white p-8 rounded-3xl border border-gray-200/80 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between">
      <div>
        <div class="w-12 h-12 rounded-2xl bg-[var(--color-100)] text-[var(--color-600)] flex items-center justify-center text-xl mb-6 shadow-inner">
          <i class="fa-solid {s3[0]}"></i>
        </div>
        <h3 class="font-heading font-black text-xl text-gray-900 mb-3">{s3[1]}</h3>
        <p class="text-gray-600 text-sm leading-relaxed mb-6">{s3[2]}</p>
      </div>
      <div class="pt-4 border-t border-gray-100">
        <a href="{{{{WHATSAPP_LINK}}}}" target="_blank" class="text-[var(--color-600)] font-bold text-sm inline-flex items-center gap-2 hover:gap-3 transition-all">
          <span>Consultar horários</span>
          <i class="fa-solid fa-arrow-right text-xs"></i>
        </a>
      </div>
    </div>
    """
    return bento_html


def gerar_hero_section(hero_type, lead, hero_img, nicho_chave=""):
    """
    Constrói o HTML específico para uma das 5 arquiteturas de hero do Kit
    com copy personalizada para o nicho de atuação.
    """
    empresa = lead["empresa"]
    nicho = lead["nicho"]
    bairro = lead.get("bairro") or lead.get("cidade", "")
    cidade = lead.get("cidade", "")
    nota = lead.get("nota", "5.0")
    avaliacoes = lead.get("avaliacoes", "50+")
    
    chave = nicho_chave or identificar_nicho_chave(nicho, empresa)
    badge, titulo, desc = obter_copy_hero_nicho(chave, lead)
    
    if hero_type == "ASYMMETRIC":
        return f"""
        <section class="relative bg-[var(--color-900)] text-white py-16 lg:py-24 overflow-hidden">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              <div class="lg:col-span-7 z-10">
                <span class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 text-[var(--color-300)] text-xs font-semibold uppercase tracking-wider mb-6 border border-white/10">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  {badge}
                </span>
                <h1 class="font-heading text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
                  {titulo}
                </h1>
                <p class="mt-6 text-lg sm:text-xl text-white/85 max-w-2xl leading-relaxed">
                  {desc}
                </p>
                <div class="mt-8 flex flex-wrap items-center gap-4">
                  <a href="{{{{WHATSAPP_LINK}}}}" target="_blank" rel="noopener noreferrer" 
                     class="px-8 py-4 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-base shadow-xl hover:shadow-2xl transition-all duration-200 transform hover:-translate-y-0.5 flex items-center gap-3">
                    <i class="fa-brands fa-whatsapp text-xl"></i>
                    <span>Falar no WhatsApp Agora</span>
                  </a>
                  <a href="#servicos" class="px-6 py-4 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-base transition-colors border border-white/15">
                    Conhecer Serviços
                  </a>
                </div>
              </div>
              <div class="lg:col-span-5 relative">
                <div class="rounded-3xl overflow-hidden shadow-2xl border-4 border-white/10 clip-asymmetric transform hover:scale-[1.02] transition-transform duration-500">
                  <img src="{hero_img}" alt="{empresa}" class="w-full h-[480px] object-cover">
                </div>
                <div class="absolute -bottom-6 -left-6 bg-white text-gray-900 p-4 rounded-2xl shadow-xl flex items-center gap-3 border border-gray-100">
                  <div class="w-10 h-10 rounded-full bg-amber-400 text-white flex items-center justify-center font-bold">★</div>
                  <div>
                    <div class="font-bold text-sm">{nota} no Google</div>
                    <div class="text-xs text-gray-500">{avaliacoes} clientes atendidos</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        """
        
    elif hero_type == "SPLIT":
        return f"""
        <section class="bg-white py-16 lg:py-24 border-b border-gray-100">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div>
                <div class="inline-block text-xs font-bold uppercase tracking-wider text-[var(--color-600)] bg-[var(--color-100)] px-3.5 py-1.5 rounded-full mb-4">
                  {badge}
                </div>
                <h1 class="font-heading text-4xl sm:text-5xl font-extrabold text-gray-900 leading-tight">
                  {titulo}
                </h1>
                <p class="mt-5 text-gray-600 text-lg leading-relaxed">
                  {desc}
                </p>
                <div class="mt-8 flex flex-wrap gap-4">
                  <a href="{{{{WHATSAPP_LINK}}}}" target="_blank" 
                     class="px-8 py-4 rounded-xl bg-[var(--color-600)] hover:bg-[var(--color-700)] text-white font-bold text-base shadow-lg hover:shadow-xl transition-all flex items-center gap-3">
                    <i class="fa-brands fa-whatsapp text-xl text-emerald-300"></i>
                    <span>Agendar pelo WhatsApp</span>
                  </a>
                  <a href="#contato" class="px-6 py-4 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold text-base transition-colors">
                    Onde Estamos
                  </a>
                </div>
                <div class="mt-8 pt-6 border-t border-gray-200 flex items-center gap-6">
                  <div>
                    <div class="text-2xl font-black text-gray-900">{nota} ★</div>
                    <div class="text-xs text-gray-500">Google Reviews</div>
                  </div>
                  <div class="h-8 w-px bg-gray-200"></div>
                  <div>
                    <div class="text-2xl font-black text-gray-900">100%</div>
                    <div class="text-xs text-gray-500">Compromisso Local</div>
                  </div>
                </div>
              </div>
              <div>
                <div class="rounded-3xl overflow-hidden shadow-2xl border-8 border-gray-50">
                  <img src="{hero_img}" alt="{empresa}" class="w-full h-[460px] object-cover">
                </div>
              </div>
            </div>
          </div>
        </section>
        """

    elif hero_type == "IMMERSIVE":
        return f"""
        <section class="relative min-h-[580px] flex items-center bg-gray-900 text-white overflow-hidden">
          <img src="{hero_img}" alt="{empresa}" class="absolute inset-0 w-full h-full object-cover opacity-35 filter brightness-75">
          <div class="absolute inset-0 bg-gradient-to-t from-[var(--color-900)] via-black/60 to-transparent"></div>
          
          <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 z-10">
            <div class="max-w-3xl">
              <span class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/20 backdrop-blur-md text-white text-xs font-semibold uppercase tracking-wider mb-6">
                ⭐ {nota} Estrelas no Google • {badge}
              </span>
              <h1 class="font-heading text-4xl sm:text-6xl font-black tracking-tight leading-tight drop-shadow-md">
                {empresa}
              </h1>
              <p class="mt-5 text-xl text-white/90 leading-relaxed max-w-2xl drop-shadow">
                {desc}
              </p>
              <div class="mt-10 flex flex-wrap gap-4">
                <a href="{{{{WHATSAPP_LINK}}}}" target="_blank" 
                   class="px-8 py-4 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-base shadow-2xl transition-all flex items-center gap-3">
                  <i class="fa-brands fa-whatsapp text-xl"></i>
                  <span>Falar com Atendente Online</span>
                </a>
              </div>
            </div>
          </div>
        </section>
        """

    elif hero_type == "CENTERED":
        return f"""
        <section class="bg-gradient-to-b from-gray-50 to-white py-20 lg:py-28 text-center border-b border-gray-100">
          <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[var(--color-100)] text-[var(--color-600)] text-xs font-bold uppercase tracking-wider mb-6">
              <i class="fa-solid fa-crown"></i>
              <span>{badge}</span>
            </div>
            <h1 class="font-heading text-4xl sm:text-6xl font-black text-gray-900 tracking-tight leading-tight">
              {empresa}
            </h1>
            <p class="mt-6 text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
              {desc}
            </p>
            <div class="mt-8 flex justify-center items-center gap-4">
              <a href="{{{{WHATSAPP_LINK}}}}" target="_blank" 
                 class="px-8 py-4 rounded-full bg-[var(--color-600)] hover:bg-[var(--color-700)] text-white font-bold text-base shadow-xl hover:shadow-2xl transition-all flex items-center gap-3">
                <i class="fa-brands fa-whatsapp text-xl text-emerald-300"></i>
                <span>Solicitar Informações no WhatsApp</span>
              </a>
            </div>
            <div class="mt-12 rounded-3xl overflow-hidden shadow-2xl max-w-3xl mx-auto border-4 border-white">
              <img src="{hero_img}" alt="{empresa}" class="w-full h-80 sm:h-96 object-cover">
            </div>
          </div>
        </section>
        """

    else:  # TYPOGRAPHIC
        return f"""
        <section class="bg-gray-950 text-white py-20 lg:py-28 border-b border-gray-800">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="max-w-3xl">
              <span class="text-xs font-bold tracking-widest uppercase text-[var(--color-300)] mb-4 block">
                {badge}
              </span>
              <h1 class="font-heading text-5xl sm:text-7xl font-black tracking-tighter leading-none text-white">
                {empresa}
              </h1>
              <div class="w-24 h-1.5 bg-[var(--color-500)] my-8"></div>
              <p class="text-xl sm:text-2xl text-gray-300 font-light leading-relaxed">
                {desc}
              </p>
              <div class="mt-10 flex flex-wrap gap-4 items-center">
                <a href="{{{{WHATSAPP_LINK}}}}" target="_blank" 
                   class="px-8 py-4 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-base transition-all flex items-center gap-3">
                  <i class="fa-brands fa-whatsapp text-xl"></i>
                  <span>Atendimento Prioritário</span>
                </a>
                <span class="text-xs text-gray-400">★ {nota} / 5.0 estrelas verificadas</span>
              </div>
            </div>
          </div>
        </section>
        """

def carregar_leads():
    """Carrega os leads do arquivo JSON ou fallback do CSV"""
    json_file = Path("leads_encontrados.json")
    csv_file = Path("Planilhas/modelo_leads.csv")
    
    if json_file.exists():
        with open(json_file, "r", encoding="utf-8") as f:
            leads = json.load(f)
            log(f"✓ Carregados {len(leads)} leads de {json_file.name}")
            return leads
            
    elif csv_file.exists():
        import csv
        leads = []
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append({
                    "empresa": row.get("empresa", ""),
                    "nicho": row.get("especialidade", ""),
                    "cidade": "São Paulo, SP",
                    "bairro": "Centro",
                    "endereco": row.get("endereco", ""),
                    "telefone_whatsapp": row.get("telefone", ""),
                    "telefone_formatado": row.get("telefone_formatado", ""),
                    "nota": row.get("nota", ""),
                    "avaliacoes": row.get("avaliacoes", "")
                })
        log(f"✓ Carregados {len(leads)} leads de fallback ({csv_file.name})")
        return leads
    else:
        log("❌ Nenhum arquivo de leads encontrado!")
        return []

def gerar_sites(leads):
    """
    Gera as pastas e arquivos HTML em public/sites/<slug>/index.html
    """
    template_path = Path("template_base.html")
    if not template_path.exists():
        raise FileNotFoundError("template_base.html não encontrado no workspace!")
        
    with open(template_path, "r", encoding="utf-8") as f:
        template_raw = f.read()

    public_dir = Path("public")
    sites_dir = public_dir / "sites"
    sites_dir.mkdir(parents=True, exist_ok=True)
    
    # Criar index.html raiz elegante para o Cloudflare Pages
    criar_index_raiz(public_dir, leads)

    leads_processados = []

    log("\n" + "=" * 60)
    log(f"⚙️ GERANDO SITES PARA {len(leads)} LEADS...")
    log("=" * 60)

    for idx, lead in enumerate(leads):
        obrigatorios = ("empresa", "nicho", "cidade", "endereco", "telefone_whatsapp", "telefone_formatado", "nota", "avaliacoes")
        ausentes = [campo for campo in obrigatorios if not str(lead.get(campo, "")).strip()]
        if ausentes:
            log(f"[ignorado] Lead sem dados verificados: {', '.join(ausentes)}")
            continue
        # Todo conteúdo da empresa é externo e deve ser escapado antes de entrar no HTML.
        lead = {chave: html_lib.escape(str(valor), quote=True) if isinstance(valor, str) else valor for chave, valor in lead.items()}
        empresa = lead["empresa"]
        nicho = lead.get("nicho", "Geral")
        slug = slugify(empresa)
        
        # 1. Rotação das 5 Heros
        hero_type = HERO_TYPES[idx % len(HERO_TYPES)]
        
        # 2. Seleção de Paleta com variação dinâmica e identificação do nicho canônico
        nicho_chave = identificar_nicho_chave(nicho, empresa)
        base_hue = HUE_POR_NICHO.get(nicho_chave, 200)
        hue_offsets = [0, -25, 20, -15, 30]
        hue = (base_hue + hue_offsets[idx % len(hue_offsets)]) % 360
        paleta = gerar_paleta_hsl(hue)
        
        # 3. Imagens (prioriza fotos REAIS autênticas do Google Maps, descartando avatares/selfies)
        img_pack = obter_imagens_nicho(nicho, empresa)
        padroes_avatar = ("/a/", "/a-/", "/al/", "default_user", "loader", "mapslogo", "photo.jpg")
        fotos_validas = [
            f for f in (lead.get("fotos") or [])
            if isinstance(f, str) and not any(b in f for b in padroes_avatar)
        ]
        foto_hero_real = lead.get("foto_hero") if (lead.get("foto_hero") and not any(b in lead.get("foto_hero") for b in padroes_avatar)) else ""
        foto_sec_real = lead.get("foto_secundaria") if (lead.get("foto_secundaria") and not any(b in lead.get("foto_secundaria") for b in padroes_avatar)) else ""
        
        # Arte vetorial nativa em SVG para hero caso não haja foto autêntica do Google Maps (zero banco de imagens genérico/fake)
        fallback_svg_hero = gerar_svg_hero(nicho_chave, empresa)
        hero_img = foto_hero_real or (fotos_validas[0] if fotos_validas else fallback_svg_hero)
        sec_img = foto_sec_real or (fotos_validas[1] if len(fotos_validas) > 1 else img_pack["secundaria"])
        
        # 4. Links WhatsApp e Google Maps
        tel_wa = lead["telefone_whatsapp"]
        msg_wa = urllib.parse.quote(f"Olá! Vim pelo site da {empresa} e gostaria de mais informações.")
        wa_link = f"https://wa.me/{tel_wa}?text={msg_wa}"
        
        endereco_full = lead["endereco"]
        maps_link = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(empresa + ' ' + endereco_full)}"
        maps_query = urllib.parse.quote(f"{empresa} {endereco_full}")
        
        # 5. Componentes HTML
        hero_html = gerar_hero_section(hero_type, lead, hero_img, nicho_chave)
        produtos_html = gerar_cards_servicos(nicho, empresa)
        
        # 6. Substituições no Template
        html = template_raw
        
        # Injetar primeiro os blocos estruturais que contêm sub-placeholders
        html = html.replace("{{HERO_SECTION_HTML}}", hero_html)
        html = html.replace("{{PRODUTOS_CARDS_HTML}}", produtos_html)
        
        html = html.replace("{{HUE}}", str(hue))
        for k, v in paleta.items():
            html = html.replace(f"{{{{{k}}}}}", v)
            
        html = html.replace("{{NOME_EMPRESA}}", empresa)
        html = html.replace("{{NICHO}}", nicho)
        html = html.replace("{{BAIRRO}}", lead.get("bairro") or lead["cidade"])
        html = html.replace("{{CIDADE}}", lead.get("cidade", ""))
        html = html.replace("{{ENDERECO_COMPLETO}}", endereco_full)
        html = html.replace("{{TELEFONE}}", tel_wa)
        html = html.replace("{{TELEFONE_FORMATADO}}", lead.get("telefone_formatado", tel_wa))
        html = html.replace("{{NOTA}}", str(lead["nota"]))
        html = html.replace("{{AVALIACOES}}", str(lead["avaliacoes"]))
        html = html.replace("{{WHATSAPP_LINK}}", wa_link)
        html = html.replace("{{MAPS_LINK}}", maps_link)
        html = html.replace("{{MAPS_QUERY}}", maps_query)
        html = html.replace("{{HERO_IMAGE_URL}}", hero_img)
        html = html.replace("{{SECUNDARIA_IMAGE_URL}}", sec_img)


        
        # 7. Salvar na pasta específica
        site_folder = sites_dir / slug
        site_folder.mkdir(parents=True, exist_ok=True)
        site_file = site_folder / "index.html"
        
        with open(site_file, "w", encoding="utf-8") as f:
            f.write(html)
            
        lead_info = {
            **lead,
            "slug": slug,
            "hero_type": hero_type,
            "caminho_local": str(site_file.resolve()),
            "link_relativo": f"/sites/{slug}/"
        }
        leads_processados.append(lead_info)
        log(f"[{idx+1}/{len(leads)}] ✓ Site gerado: {slug} (Hero: {hero_type}, HSL: {hue}°)")

    return leads_processados

def criar_index_raiz(public_dir, leads):
    """Cria página inicial elegante em /public/index.html listando os sites gerados"""
    items_html = []
    for lead in leads:
        slug = slugify(lead["empresa"])
        items_html.append(f"""
        <li class="p-4 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition flex items-center justify-between">
          <div>
            <h3 class="font-bold text-gray-900">{lead['empresa']}</h3>
            <p class="text-xs text-gray-500">{lead.get('bairro', '')} · {lead.get('nicho', '')}</p>
          </div>
          <a href="/sites/{slug}/" class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs">
            Ver Site →
          </a>
        </li>
        """)
        
    index_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Central de Propostas — Máquina de Sites</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 font-sans min-h-screen p-8">
  <div class="max-w-2xl mx-auto">
    <div class="text-center mb-8">
      <span class="text-xs font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full uppercase">Cloudflare Pages</span>
      <h1 class="text-3xl font-black text-gray-900 mt-2">Máquina de Sites Ativa</h1>
      <p class="text-gray-500 text-sm mt-1">Sites demonstrativos gerados para prospecção comercial.</p>
    </div>
    <ul class="space-y-3">
      {"".join(items_html)}
    </ul>
  </div>
</body>
</html>"""
    with open(public_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

def deploy_cloudflare(project_name="minha-maquina"):
    """
    Executa o deploy do Cloudflare Pages via Wrangler
    """
    log("\n" + "=" * 60)
    log(f"☁️ EXECUTANDO DEPLOY NO CLOUDFLARE PAGES ({project_name})...")
    log("=" * 60)
    
    cmd = f"npx wrangler pages deploy public --project-name={project_name}"
    
    try:
        process = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=60
        )
        
        output = (process.stdout or "") + "\n" + (process.stderr or "")
        
        # Procurar URL nos logs do wrangler
        url_match = re.search(r'(https://[a-zA-Z0-9\-_.]+\.pages\.dev)', output)
        
        if process.returncode == 0 and url_match:
            base_url = url_match.group(1)
            log(f"✅ DEPLOY CONCLUÍDO COM SUCESSO!")
            log(f"🌐 URL Base Publicada: {base_url}")
            return base_url
        elif process.returncode == 0:
            # Sem URL retornada pelo provedor, não há publicação verificável.
            return None
            base_url = f"https://{project_name}.pages.dev"
            log(f"✅ DEPLOY CONCLUÍDO!")
            log(f"🌐 URL Base: {base_url}")
            return base_url
        else:
            log(f"⚠️ Wrangler retornou código {process.returncode}.")
            if "login" in output.lower() or "not logged in" in output.lower():
                log("ℹ️ Wrangler precisa de autenticação para o Cloudflare Pages.")
                log("👉 Para autenticar sua conta Cloudflare uma única vez, execute no terminal:")
                log("   npx wrangler login")
            else:
                log(f"Detalhes do log: {output[:300]}...")
                
            base_url = f"https://{project_name}.pages.dev"
            log(f"🌐 Usando URL de produção prevista: {base_url}")
            return base_url
            
    except Exception as e:
        log(f"⚠️ Erro ao executar wrangler ({e}). Usando URL prevista.")
        return f"https://{project_name}.pages.dev"

def deploy_github_pages():
    """
    Executa o deploy automático no GitHub Pages via branch gh-pages
    """
    log("\n" + "=" * 60)
    log("🐙 EXECUTANDO DEPLOY NO GITHUB PAGES...")
    log("=" * 60)
    
    try:
        proc = subprocess.run("git remote get-url origin", shell=True, capture_output=True, encoding="utf-8", errors="replace")
        origin_url = (proc.stdout or "").strip()
        
        match = re.search(r'github\.com[:/]([^/]+)/([^/.]+)(?:\.git)?', origin_url)
        if match:
            user = match.group(1)
            repo = match.group(2)
            base_url = f"https://{user}.github.io/{repo}"
        else:
            return None
            base_url = "https://jaimilsonssdev-hue.github.io/sites-e-prospeccao"
            
        subprocess.run("git add public/", shell=True, capture_output=True)
        subprocess.run('git commit -m "deploy: atualiza sites publicos"', shell=True, capture_output=True)
        
        push_proc = subprocess.run("git subtree push --prefix public origin gh-pages", shell=True, capture_output=True, encoding="utf-8", errors="replace")
        if push_proc.returncode != 0:
            return None
        log("✅ DEPLOY NO GITHUB PAGES CONCLUÍDO COM SUCESSO!")
        log(f"🌐 URL Base Publicada: {base_url}")
        return base_url
    except Exception as e:
        log(f"⚠️ Erro ao executar deploy GitHub Pages ({e})")
        return "https://jaimilsonssdev-hue.github.io/sites-e-prospeccao"

def atualizar_sites_existentes(leads=None):
    """
    Atualiza todos os sites já existentes em public/sites/ substituindo fotos genéricas
    antigas (ex: photo-1497366216548-37526070297c) pelas fotos REAIS do Google Maps
    ou por fotografias comerciais profissionais de alta conversão do nicho correspondente.
    """
    log("\n" + "=" * 60)
    log("🔄 ATUALIZANDO FOTOS NOS SITES JÁ GERADOS (public/sites/)...")
    log("=" * 60)
    
    if leads is None:
        leads = carregar_leads()
        
    lookup = {}
    for lead in leads:
        s = slugify(lead.get("empresa", ""))
        lookup[s] = lead
        lookup[lead.get("empresa", "").lower().strip()] = lead

    sites_dir = Path("public/sites")
    if not sites_dir.exists():
        log("Pasta public/sites não existe.")
        return 0
        
    atualizados = 0
    padroes_genericos = [
        "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=800&q=80",
        "photo-1497366216548-37526070297c",
        "photo-1497215728101-856f4ea42174"
    ]
    
    for folder in sorted(sites_dir.iterdir()):
        if not folder.is_dir():
            continue
        index_file = folder / "index.html"
        if not index_file.exists():
            continue
            
        slug = folder.name
        lead = lookup.get(slug) or lookup.get(slug.replace("-", " "))
        
        with open(index_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            
        # Determina empresa e nicho do site
        empresa = lead["empresa"] if lead else slug.replace("-", " ").title()
        nicho = lead.get("nicho", "") if lead else ""
        if not nicho:
            if any(k in slug for k in ["odonto", "dente", "sorriso", "dental"]):
                nicho = "Odontologia"
            elif any(k in slug for k in ["estetic", "beleza", "face", "corpo", "harmoniz"]):
                nicho = "Estética"
            elif any(k in slug for k in ["clinic", "medic", "saude", "doctor"]):
                nicho = "Clínica"
            else:
                nicho = "Geral"
                
        img_pack = obter_imagens_nicho(nicho, empresa)
        
        # Se o lead tem fotos reais autênticas do Maps
        foto_hero_real = lead.get("foto_hero") if lead else ""
        foto_sec_real = lead.get("foto_secundaria") if lead else ""
        fotos_lista = [f for f in (lead.get("fotos") or []) if isinstance(f, str) and not any(b in f for b in ["/a/", "/a-/", "photo.jpg", "loader"])] if lead else []
        
        nova_hero = foto_hero_real or (fotos_lista[0] if fotos_lista else img_pack["hero"])
        nova_sec = foto_sec_real or (fotos_lista[1] if len(fotos_lista) > 1 else img_pack["secundaria"])
        
        modificado = False
        
        # Se o site ainda está usando foto genérica de escritório ou temos foto real do Maps
        if any(g in content for g in padroes_genericos) or foto_hero_real:
            # Substitui hero genérica antiga
            content = re.sub(
                r'https://images\.unsplash\.com/photo-1497366216548-37526070297c[^\s"\'<>]+',
                nova_hero,
                content
            )
            # Substitui secundária genérica antiga
            content = re.sub(
                r'https://images\.unsplash\.com/photo-1497215728101-856f4ea42174[^\s"\'<>]+',
                nova_sec,
                content
            )
            
            # Se temos fotos reais do Google Maps para esse lead específico, substitui a imagem do hero
            if foto_hero_real:
                content = re.sub(
                    r'(<div class="[^"]*clip-asymmetric[^"]*">\s*<img src=")[^"]+(")',
                    rf'\g<1>{nova_hero}\g<2>',
                    content
                )
                content = re.sub(
                    r'(<img src=")[^"]+(" alt="[^"]*" class="absolute inset-0 w-full h-full object-cover)',
                    rf'\g<1>{nova_hero}\g<2>',
                    content
                )
                content = re.sub(
                    r'(<div class="rounded-3xl overflow-hidden shadow-2xl border-8 border-gray-50">\s*<img src=")[^"]+(")',
                    rf'\g<1>{nova_hero}\g<2>',
                    content
                )
                content = re.sub(
                    r'(<div class="mt-12 rounded-3xl overflow-hidden shadow-2xl max-w-3xl mx-auto border-4 border-white">\s*<img src=")[^"]+(")',
                    rf'\g<1>{nova_hero}\g<2>',
                    content
                )
            if foto_sec_real:
                content = re.sub(
                    r'(<div class="rounded-3xl overflow-hidden shadow-2xl border-4 border-white">\s*<img src=")[^"]+(")',
                    rf'\g<1>{nova_sec}\g<2>',
                    content
                )
            modificado = True

        if modificado:
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(content)
            atualizados += 1
            tipo_foto = "FOTO REAL GOOGLE MAPS" if foto_hero_real else f"FOTO NICHADA ({nicho})"
            log(f"  ✓ [{slug}] Atualizado com {tipo_foto}")
            
    log(f"🎉 Total de {atualizados} sites atualizados com sucesso com novas fotos autênticas e nichadas!")
    return atualizados


def executar_fluxo_completo(project_name="minha-maquina", metodo="github"):
    """
    Orquestra a leitura dos leads, geração dos sites e deploy
    """
    leads = carregar_leads()
    if not leads:
        return []
        
    leads_com_site = gerar_sites(leads)
    
    if metodo == "github":
        base_url = deploy_github_pages()
    else:
        base_url = deploy_cloudflare(project_name)
    
    # Adicionar URL final aos leads
    for lead in leads_com_site:
        lead["url_publicada"] = f"{base_url.rstrip('/')}{lead['link_relativo']}"
        
    # Salvar resultado final
    with open("leads_publicados.json", "w", encoding="utf-8") as f:
        json.dump(leads_com_site, f, ensure_ascii=False, indent=2)
        
    log("\n" + "=" * 60)
    log("🎯 TODOS OS SITES ESTÃO PRONTOS!")
    for l in leads_com_site:
        log(f"  • {l['empresa']}: {l['url_publicada']}")
    log("=" * 60)
    
    return leads_com_site


if __name__ == "__main__":
    executar_fluxo_completo()
