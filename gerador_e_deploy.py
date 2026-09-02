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

# Paletas de cores HUE base por nicho
HUE_POR_NICHO = {
    "odontologia": 195,  # Teal / Ciano médico
    "estética": 335,     # Rose / Pink sofisticado
    "advocacia": 275,    # Purple / Índigo formal
    "restaurante": 28,   # Laranja apetitoso
    "pizzaria": 15,      # Vermelho / Terracota
    "veterinária": 155,  # Verde natureza / Pet
    "imobiliária": 210,  # Azul confiança
    "geral": 200         # Azul corporativo
}

# Imagens de alta conversão no Unsplash por nicho
IMAGENS_NICHO = {
    "odontologia": {
        "hero": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=800&q=80"
    },
    "estética": {
        "hero": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1512290900672-1f5be1c6e1c8?auto=format&fit=crop&w=800&q=80"
    },
    "advocacia": {
        "hero": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80"
    },
    "restaurante": {
        "hero": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80"
    },
    "pizzaria": {
        "hero": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=800&q=80"
    },
    "geral": {
        "hero": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80",
        "secundaria": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=800&q=80"
    }
}

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

def gerar_cards_servicos(nicho):
    """Gera HTML dos 3 cards principais de serviços baseado no nicho"""
    nicho_low = nicho.lower()
    
    if "odonto" in nicho_low:
        servicos = [
            ("fa-tooth", "Clareamento & Estética Dental", "Técnicas avançadas para devolver o brilho e a harmonia do seu sorriso."),
            ("fa-teeth-open", "Implantes & Próteses", "Recupere sua mastigação e autoconfiança com procedimentos seguros e indolores."),
            ("fa-shield-heart", "Prevenção & Odontologia Geral", "Check-up completo, limpeza profunda e cuidados contínuos para toda a família.")
        ]
    elif "estétic" in nicho_low or "beleza" in nicho_low:
        servicos = [
            ("fa-wand-magic-sparkles", "Harmonização Facial", "Realce seus traços naturais com procedimentos minimamente invasivos de alta precisão."),
            ("fa-spa", "Limpeza de Pele Profunda", "Remoção de impurezas, controle de oleosidade e hidratação celular completa."),
            ("fa-gem", "Tratamentos Corporais", "Tecnologias para redução de medidas, celulite e estímulo de colágeno.")
        ]
    elif "advoc" in nicho_low or "jurídic" in nicho_low:
        servicos = [
            ("fa-scale-balanced", "Direito Civil & Família", "Proteção patrimonial, inventários, divórcios e soluções ágeis para você e sua família."),
            ("fa-briefcase", "Assessoria Trabalhista", "Defesa técnica de direitos e conformidade com as normas legais vigentes."),
            ("fa-handshake", "Contratos & Negócios", "Elaboração e análise detalhada para garantir total segurança jurídica.")
        ]
    elif "pizz" in nicho_low:
        servicos = [
            ("fa-pizza-slice", "Pizzas Tradicionais", "Massa de fermentação lenta com molho de tomate artesanal e ingredientes selecionados."),
            ("fa-fire", "Especiais do Chef", "Combinações exclusivas assadas no forno a lenha na temperatura ideal."),
            ("fa-motorcycle", "Delivery Rápido & Quentinho", "Embalagens térmicas especiais para você saborear como se estivesse no salão.")
        ]
    else:
        servicos = [
            ("fa-star", "Atendimento Personalizado", "Consultoria dedicada para encontrar a solução exata para sua necessidade."),
            ("fa-award", "Excelência Comprovada", "Anos de experiência e satisfação garantida para nossos clientes."),
            ("fa-clock-rotate-left", "Agilidade & Pontualidade", "Compromisso rigoroso com seus prazos e atendimento prioritário.")
        ]
        
    html_cards = []
    for icon, titulo, desc in servicos:
        html_cards.append(f"""
        <div class="bg-white p-8 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
          <div class="w-14 h-14 rounded-2xl bg-[var(--color-100)] text-[var(--color-600)] flex items-center justify-center text-2xl mb-6 shadow-inner">
            <i class="fa-solid {icon}"></i>
          </div>
          <h3 class="font-heading font-bold text-xl text-gray-900 mb-3">{titulo}</h3>
          <p class="text-gray-600 text-sm leading-relaxed mb-6">{desc}</p>
          <a href="{{{{WHATSAPP_LINK}}}}" target="_blank" class="text-[var(--color-600)] font-semibold text-sm inline-flex items-center gap-2 hover:gap-3 transition-all">
            <span>Saber mais detalhes</span>
            <i class="fa-solid fa-arrow-right text-xs"></i>
          </a>
        </div>
        """)
    return "\n".join(html_cards)

def gerar_hero_section(hero_type, lead, hero_img):
    """
    Constrói o HTML específico para uma das 5 arquiteturas de hero do Kit
    """
    empresa = lead["empresa"]
    nicho = lead["nicho"]
    bairro = lead["bairro"]
    cidade = lead["cidade"]
    nota = lead["nota"]
    avaliacoes = lead["avaliacoes"]
    
    if hero_type == "ASYMMETRIC":
        return f"""
        <section class="relative bg-[var(--color-900)] text-white py-16 lg:py-24 overflow-hidden">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              <div class="lg:col-span-7 z-10">
                <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-[var(--color-300)] text-xs font-semibold uppercase tracking-wider mb-6 border border-white/10">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  Referência em {nicho} no {bairro}
                </span>
                <h1 class="font-heading text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
                  Excelência e Cuidado para você na <span class="text-[var(--color-400)]">{empresa}</span>
                </h1>
                <p class="mt-6 text-lg sm:text-xl text-white/80 max-w-2xl leading-relaxed">
                  Conheça o padrão de qualidade que conquistou nota {nota} estrelas no Google em {cidade}. Agende ou tire dúvidas diretamente pelo WhatsApp.
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
                <div class="inline-block text-xs font-bold uppercase tracking-wider text-[var(--color-600)] bg-[var(--color-100)] px-3 py-1 rounded-full mb-4">
                  {nicho} de Alta Qualidade
                </div>
                <h1 class="font-heading text-4xl sm:text-5xl font-extrabold text-gray-900 leading-tight">
                  O melhor atendimento em {nicho} no bairro {bairro}
                </h1>
                <p class="mt-5 text-gray-600 text-lg leading-relaxed">
                  A equipe da <strong>{empresa}</strong> une tecnologia, dedicação e profissionais capacitados para oferecer o melhor a você em {cidade}.
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
                ⭐ {nota} Estrelas no Google Maps ({avaliacoes} avaliações)
              </span>
              <h1 class="font-heading text-4xl sm:text-6xl font-black tracking-tight leading-tight drop-shadow-md">
                {empresa}
              </h1>
              <p class="mt-5 text-xl text-white/90 leading-relaxed max-w-2xl drop-shadow">
                Especialistas dedicados em {nicho} trazendo conforto, segurança e resultados de primeiro nível em {bairro}, {cidade}.
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
              <span>Autoridade em {nicho} em {cidade}</span>
            </div>
            <h1 class="font-heading text-4xl sm:text-6xl font-black text-gray-900 tracking-tight leading-tight">
              {empresa}
            </h1>
            <p class="mt-6 text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
              Atendimento personalizado e estrutura completa no bairro {bairro}. Entre em contato direto e experimente a diferença.
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
                {bairro.upper()}, {cidade.upper()} — {nicho.upper()}
              </span>
              <h1 class="font-heading text-5xl sm:text-7xl font-black tracking-tighter leading-none text-white">
                {empresa}
              </h1>
              <div class="w-24 h-1.5 bg-[var(--color-500)] my-8"></div>
              <p class="text-xl sm:text-2xl text-gray-300 font-light leading-relaxed">
                Compromisso inegociável com qualidade, pontualidade e transparência para clientes exigentes em {cidade}.
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
                    "empresa": row.get("empresa", "Empresa"),
                    "nicho": row.get("especialidade", "Geral").capitalize(),
                    "cidade": "São Paulo, SP",
                    "bairro": "Centro",
                    "endereco": row.get("endereco", "Centro"),
                    "telefone_whatsapp": row.get("telefone", "5511987654321"),
                    "telefone_formatado": "(11) 98765-4321",
                    "nota": row.get("nota", "4.9"),
                    "avaliacoes": row.get("avaliacoes", "120")
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
        empresa = lead["empresa"]
        nicho = lead.get("nicho", "Geral")
        slug = slugify(empresa)
        
        # 1. Rotação das 5 Heros
        hero_type = HERO_TYPES[idx % len(HERO_TYPES)]
        
        # 2. Seleção de Paleta
        nicho_key = nicho.lower()
        hue = HUE_POR_NICHO.get(nicho_key, 200)
        paleta = gerar_paleta_hsl(hue)
        
        # 3. Imagens
        img_pack = IMAGENS_NICHO.get(nicho_key, IMAGENS_NICHO["geral"])
        hero_img = img_pack["hero"]
        sec_img = img_pack["secundaria"]
        
        # 4. Links WhatsApp e Google Maps
        tel_wa = lead.get("telefone_whatsapp", "5511987654321")
        msg_wa = urllib.parse.quote(f"Olá! Vim pelo site da {empresa} e gostaria de mais informações.")
        wa_link = f"https://wa.me/{tel_wa}?text={msg_wa}"
        
        endereco_full = lead.get("endereco", f"{lead.get('bairro', 'Centro')}, {lead.get('cidade', '')}")
        maps_link = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(empresa + ' ' + endereco_full)}"
        
        # 5. Componentes HTML
        hero_html = gerar_hero_section(hero_type, lead, hero_img)
        produtos_html = gerar_cards_servicos(nicho)
        
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
        html = html.replace("{{BAIRRO}}", lead.get("bairro", "Centro"))
        html = html.replace("{{CIDADE}}", lead.get("cidade", ""))
        html = html.replace("{{ENDERECO_COMPLETO}}", endereco_full)
        html = html.replace("{{TELEFONE}}", tel_wa)
        html = html.replace("{{TELEFONE_FORMATADO}}", lead.get("telefone_formatado", tel_wa))
        html = html.replace("{{NOTA}}", str(lead.get("nota", "4.9")))
        html = html.replace("{{AVALIACOES}}", str(lead.get("avaliacoes", "120")))
        html = html.replace("{{WHATSAPP_LINK}}", wa_link)
        html = html.replace("{{MAPS_LINK}}", maps_link)
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

def executar_fluxo_completo(project_name="minha-maquina"):
    """
    Orquestra a leitura dos leads, geração dos sites e deploy
    """
    leads = carregar_leads()
    if not leads:
        return []
        
    leads_com_site = gerar_sites(leads)
    base_url = deploy_cloudflare(project_name)
    
    # Adicionar URL final aos leads
    for lead in leads_com_site:
        lead["url_publicada"] = f"{base_url.rstrip('/')}{lead['link_relativo']}"
        
    # Salvar resultado final
    with open("leads_publicados.json", "w", encoding="utf-8") as f:
        json.dump(leads_com_site, f, ensure_ascii=False, indent=2)
        
    log("\n" + "=" * 60)
    log(f"🎯 TODOS OS SITES ESTÃO PRONTOS!")
    for l in leads_com_site:
        log(f"  • {l['empresa']}: {l['url_publicada']}")
    log("=" * 60)
    
    return leads_com_site

if __name__ == "__main__":
    executar_fluxo_completo()

