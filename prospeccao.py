#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prospecção local verificável via Google Maps e Jina Reader.

O módulo nunca completa telefone, endereço, nota ou avaliações com valores
estimados. Um resultado sem os dados necessários é descartado.
"""

import csv
import json
import re
import sys
import unicodedata
import urllib.parse
from datetime import datetime
from pathlib import Path

import requests


def log(mensagem: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {mensagem}", flush=True)


def limpar_nome_busca(nome: str) -> str:
    """Remove slogans, subtítulos e repetições de cidade para encontrar a ficha direta no Maps."""
    nome_limpo = re.sub(r"\s*[-–|]\s*(?:Sua Clínica|Especializada|Matriz|Filial|Teixeira de Freitas|BA|SP|RJ|MG|DF|Brasil).*", "", nome, flags=re.I)
    return nome_limpo.strip() or nome.strip()


def extrair_fotos_estabelecimento(empresa: str, cidade: str, endereco: str = "") -> dict:
    """Extrai fotos reais do Google Maps filtrando estritamente avatares e pessoas.
    
    Prioriza fachadas reais do Google Street View e fotos comerciais do estabelecimento,
    elevando a resolução para visualização em alta definição.
    """
    termo_limpo = limpar_nome_busca(empresa)
    consulta = urllib.parse.quote(f"{termo_limpo} {cidade}")
    origem = f"https://www.google.com/maps/search/{consulta}?hl=pt-BR"
    
    try:
        resp = requests.get(
            f"https://r.jina.ai/{origem}",
            headers={"Accept-Language": "pt-BR,pt;q=0.9"},
            timeout=25
        )
        if not resp.ok:
            return {"foto_hero": "", "foto_secundaria": "", "fotos": []}
        texto = resp.text
    except requests.RequestException:
        return {"foto_hero": "", "foto_secundaria": "", "fotos": []}
        
    urls_brutas = re.findall(
        r'https?://(?:lh\d+\.googleusercontent\.com|streetviewpixels-pa\.googleapis\.com)[^\s\)"\']+',
        texto
    )
    
    padroes_bloqueados = (
        "/a/", "/a-/", "/al/", "default_user", "loader", "mapslogo", "photo.jpg",
        "contrib", "profile_photos", "result-no-thumbnail", "=s32", "=s40",
        "=s48", "=s64", "=w36", "=w48", "tactile"
    )
    
    fotos_fachada = []
    fotos_local = []
    vistos = set()
    
    for url in urls_brutas:
        if any(bad in url for bad in padroes_bloqueados):
            continue
        if "vt/pb=" in url:
            continue
            
        if "streetviewpixels-pa.googleapis.com" in url:
            url_hd = re.sub(r'&w=\d+&h=\d+', '&w=1200&h=600', url)
            if url_hd not in vistos:
                vistos.add(url_hd)
                fotos_fachada.append(url_hd)
        elif "googleusercontent.com" in url:
            url_hd = re.sub(r'=w\d+.*$', '=w1200-h800-k-no', url)
            if "=w1200" not in url_hd:
                url_hd = url_hd + "=w1200-h800-k-no"
            if url_hd not in vistos:
                vistos.add(url_hd)
                fotos_local.append(url_hd)
                
    todas = fotos_fachada + fotos_local

    # Se não encontrou na primeira busca, tenta variação simplificada do termo (ex: "Prevclin Teixeira de Freitas")
    if not todas and " " in termo_limpo:
        palavras = [p for p in termo_limpo.split() if p.lower() not in ["clínica", "clinica", "centro", "instituto", "dr.", "dra."]]
        if palavras:
            termo_alt = " ".join(palavras)
            consulta_alt = urllib.parse.quote(f"{termo_alt} {cidade}")
            try:
                resp_alt = requests.get(
                    f"https://r.jina.ai/https://www.google.com/maps/search/{consulta_alt}?hl=pt-BR",
                    headers={"Accept-Language": "pt-BR,pt;q=0.9"},
                    timeout=20
                )
                if resp_alt.ok:
                    urls_alt = re.findall(
                        r'https?://(?:lh\d+\.googleusercontent\.com|streetviewpixels-pa\.googleapis\.com)[^\s\)"\']+',
                        resp_alt.text
                    )
                    for url in urls_alt:
                        if any(bad in url for bad in padroes_bloqueados) or "vt/pb=" in url:
                            continue
                        if "streetviewpixels-pa.googleapis.com" in url:
                            url_hd = re.sub(r'&w=\d+&h=\d+', '&w=1200&h=600', url)
                            if url_hd not in vistos:
                                vistos.add(url_hd)
                                fotos_fachada.append(url_hd)
                        elif "googleusercontent.com" in url:
                            url_hd = re.sub(r'=w\d+.*$', '=w1200-h800-k-no', url)
                            if "=w1200" not in url_hd:
                                url_hd = url_hd + "=w1200-h800-k-no"
                            if url_hd not in vistos:
                                vistos.add(url_hd)
                                fotos_local.append(url_hd)
                    todas = fotos_fachada + fotos_local
            except requests.RequestException:
                pass

    hero = fotos_fachada[0] if fotos_fachada else (fotos_local[0] if fotos_local else "")
    sec = fotos_local[0] if fotos_fachada and fotos_local else (fotos_local[1] if len(fotos_local) > 1 else (fotos_fachada[1] if len(fotos_fachada) > 1 else ""))
    
    return {
        "foto_hero": hero,
        "foto_secundaria": sec,
        "fotos": todas
    }


def sanitizar_telefone(valor: str) -> tuple[str, str]:
    """Retorna número WhatsApp e formato visual, ou campos vazios se inválido."""
    digitos = re.sub(r"\D", "", valor or "").lstrip("0")
    if digitos.startswith("55") and len(digitos) in (12, 13):
        ddd, numero, whatsapp = digitos[2:4], digitos[4:], digitos
    elif len(digitos) in (10, 11):
        ddd, numero, whatsapp = digitos[:2], digitos[2:], f"55{digitos}"
    else:
        return "", ""
    exibicao = f"({ddd}) {numero[:5]}-{numero[5:]}" if len(numero) == 9 else f"({ddd}) {numero[:4]}-{numero[4:]}"
    return whatsapp, exibicao


def _normalizar(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


def _extrair_avaliacoes(texto: str) -> int | None:
    match = re.search(r"([\d.]+)\s+avalia(?:ção|ções|coes|cao)", texto, re.I)
    return int(match.group(1).replace(".", "")) if match else None


def _extrair_endereco(texto: str) -> str:
    for padrao in (
        r"(?:Endereço|Address)\s*[:·-]?\s*([^\n]+)",
        r"·\s*((?:Av\.|Avenida|R\.|Rua|Praça|Estr\.)[^\n·]+)",
    ):
        match = re.search(padrao, texto, re.I)
        if match:
            return match.group(1).strip(" -·")
    return ""


def buscar_google_maps_via_jina(nicho: str, cidade: str, max_results: int = 10) -> list[dict]:
    """Consulta o Google Maps em pt-BR e devolve somente registros completos."""
    consulta = "+".join(re.sub(r"[^\w\s]", " ", f"{nicho} em {cidade}").split())
    origem = f"https://www.google.com/maps/search/{consulta}?hl=pt-BR"
    log(f"Consultando Google Maps: {nicho} em {cidade}")
    try:
        resposta = requests.get(f"https://r.jina.ai/{origem}", headers={"Accept-Language": "pt-BR,pt;q=0.9"}, timeout=30)
        resposta.raise_for_status()
    except requests.RequestException as erro:
        log(f"Falha ao consultar Jina Reader: {erro}")
        return []

    partes = re.split(r"\[([^\]]+)\]\(https://www\.google\.com/maps/place/[^)]+\)", resposta.text)
    leads, nomes = [], set()
    for indice in range(1, len(partes), 2):
        empresa, bloco = partes[indice].strip(), partes[indice + 1] if indice + 1 < len(partes) else ""
        chave = _normalizar(empresa)
        telefone_bruto = re.search(r"(?:\+55\s*)?(?:\(?\d{2}\)?\s*)?9?\d{4}[-\s]?\d{4}", bloco)
        nota = re.search(r"\b([1-5][,.][0-9])\b", bloco)
        avaliacoes, endereco = _extrair_avaliacoes(bloco), _extrair_endereco(bloco)
        whatsapp, telefone = sanitizar_telefone(telefone_bruto.group(0) if telefone_bruto else "")
        tem_site = bool(re.search(r"\[?(?:Website|Site)\]?", bloco, re.I))
        insta_match = re.search(r"instagram\.com/([a-zA-Z0-9._]+)", bloco, re.I)
        instagram = f"@{insta_match.group(1)}" if insta_match and insta_match.group(1).lower() not in ["explore", "p", "reel"] else ""
        if not (empresa and chave not in nomes and whatsapp and nota and avaliacoes is not None and endereco):
            log(f"Ignorado por dados não verificáveis: {empresa or 'resultado sem nome'}")
            continue
        nomes.add(chave)
        leads.append({"empresa": empresa, "nicho": nicho, "cidade": cidade, "bairro": "", "endereco": endereco,
                      "endereco_completo": endereco, "telefone_whatsapp": whatsapp, "telefone_formatado": telefone,
                      "instagram": instagram,
                      "nota": nota.group(1).replace(",", "."), "avaliacoes": avaliacoes, "tem_site": tem_site,
                      "maps_origem": origem})
        if len(leads) >= max_results:
            break
    sem_site = [lead for lead in leads if not lead["tem_site"]]
    log(f"{len(leads)} empresas verificadas; {len(sem_site)} sem Website indicado no Maps.")
    leads_finais = (sem_site + [lead for lead in leads if lead["tem_site"]])[:max_results]

    # Enriquece cada lead com fotos autênticas do Google Maps (fachada e instalações)
    for lead in leads_finais:
        fotos_info = extrair_fotos_estabelecimento(lead["empresa"], lead["cidade"], lead.get("endereco", ""))
        lead["foto_hero"] = fotos_info.get("foto_hero", "")
        lead["foto_secundaria"] = fotos_info.get("foto_secundaria", "")
        lead["fotos"] = fotos_info.get("fotos", [])
        if lead["foto_hero"]:
            log(f"  ✓ Fotos capturadas para {lead['empresa']}: {len(lead['fotos'])} fotos reais")
        else:
            log(f"  ℹ Sem fotos públicas no Maps para {lead['empresa']} (usará banco nichado de alta conversão)")

    return leads_finais


def prospectar(nicho: str, cidade: str, quantidade: int = 5, jina_api_key: str | None = None) -> list[dict]:
    """Executa a consulta e salva JSON/CSV; a chave é mantida por compatibilidade."""
    del jina_api_key
    if quantidade < 1:
        raise ValueError("--qtd deve ser maior que zero")
    leads = buscar_google_maps_via_jina(nicho, cidade, quantidade)
    Path("leads_encontrados.json").write_text(json.dumps(leads, ensure_ascii=False, indent=2), encoding="utf-8")
    csv_path = Path("Planilhas/leads_prospeccao.csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    campos = ["empresa", "nicho", "cidade", "bairro", "endereco", "endereco_completo", "telefone_whatsapp", "telefone_formatado", "instagram", "nota", "avaliacoes", "tem_site", "foto_hero", "foto_secundaria", "maps_origem"]
    with csv_path.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(leads)
    log(f"Prospecção concluída: {len(leads)} lead(s) verificável(is) com campo de Instagram.")
    return leads


if __name__ == "__main__":
    prospectar(sys.argv[1] if len(sys.argv) > 1 else "Odontologia", sys.argv[2] if len(sys.argv) > 2 else "São Paulo, SP", int(sys.argv[3]) if len(sys.argv) > 3 else 5)

