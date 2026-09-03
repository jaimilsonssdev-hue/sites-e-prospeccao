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
from datetime import datetime
from pathlib import Path

import requests


def log(mensagem: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {mensagem}", flush=True)


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
    return (sem_site + [lead for lead in leads if lead["tem_site"]])[:max_results]


def prospectar(nicho: str, cidade: str, quantidade: int = 5, jina_api_key: str | None = None) -> list[dict]:
    """Executa a consulta e salva JSON/CSV; a chave é mantida por compatibilidade."""
    del jina_api_key
    if quantidade < 1:
        raise ValueError("--qtd deve ser maior que zero")
    leads = buscar_google_maps_via_jina(nicho, cidade, quantidade)
    Path("leads_encontrados.json").write_text(json.dumps(leads, ensure_ascii=False, indent=2), encoding="utf-8")
    csv_path = Path("Planilhas/leads_prospeccao.csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    campos = ["empresa", "nicho", "cidade", "bairro", "endereco", "endereco_completo", "telefone_whatsapp", "telefone_formatado", "instagram", "nota", "avaliacoes", "tem_site", "maps_origem"]
    with csv_path.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(leads)
    log(f"Prospecção concluída: {len(leads)} lead(s) verificável(is) com campo de Instagram.")
    return leads


if __name__ == "__main__":
    prospectar(sys.argv[1] if len(sys.argv) > 1 else "Odontologia", sys.argv[2] if len(sys.argv) > 2 else "São Paulo, SP", int(sys.argv[3]) if len(sys.argv) > 3 else 5)

