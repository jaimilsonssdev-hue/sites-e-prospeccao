---
name: creative-site-craft
description: Diretrizes de design editorial, arquétipos de nicho, copywriting sensorial de alta conversão e otimização de tokens para geração e refinamento de sites com IA.
---

# Skill: Creative Site Craft & High-Conversion Architecture

Esta skill define as regras de ouro, arquétipos de design, diretrizes de copywriting direto e padrões de economia de tokens para o motor de geração e refinamento de sites do **Studio IA** e da **Prospecção**.

Inspirada nas melhores práticas de repositórios do GitHub (v0, Lovable, Tailwind UI e shadcn/ui), esta skill transforma fichas frias do Google Maps em experiências digitais cinematográficas com alta taxa de conversão.

---

## 1. Os 5 Arquétipos Visuais de Nicho

Para evitar layouts genéricos, cafonas ou repetitivos, cada negócio é mapeado para um arquétipo rigoroso com design tokens restritos:

### 1.1 `luxury-editorial`
- **Nichos aplicáveis**: Alta gastronomia, bistrôs, confeitarias finas, cafés especiais, joalherias, arquitetura de luxo, clínicas VIP.
- **Paleta de cores**:
  - Fundo: `#0a0a0c` (ébano profundo)
  - Acento: `#f59e0b` (âmbar nobre) ou `#d4d4d8` (titânio platina)
  - Superfície dos cards: `#121217` com borda `border-white/10`
- **Tipografia**: `serif` (fontes com serifa elegante nos títulos, sans limpa no corpo).
- **Estilo de borda**: `glass` (vidro fosco com `backdrop-blur-md`).
- **Atmosfera**: Intimista, iluminação suave, silêncio acústico, exclusividade.

### 1.2 `clean-biotech`
- **Nichos aplicáveis**: Odontologia, dermatologia, estética corporal, cirurgia plástica, fisioterapia, spas médicos, longevidade.
- **Paleta de cores**:
  - Fundo: `#070b0c` (ardósia escurecida)
  - Acento: `#10b981` (esmeralda suave) ou `#06b6d4` (ciano clínico)
  - Superfície dos cards: `#0e1416` com borda `border-emerald-500/20`
- **Tipografia**: `sans` (moderna, arejada, transmitindo máxima clareza e higiene).
- **Estilo de borda**: `glass` acetinado.
- **Atmosfera**: Rigor biomédico, segurança farmacológica, previsibilidade de resultados.

### 1.3 `cyber-tech`
- **Nichos aplicáveis**: Barbearias modernas/industriais, estúdios de tatuagem tech, software, automação, engenharia, estética automotiva.
- **Paleta de cores**:
  - Fundo: `#06090e` (azul noturno quase preto)
  - Acento: `#00f0ff` (cyan elétrico) ou `#38bdf8` (azul glacial)
  - Superfície dos cards: `#0c1017` com borda `border-sky-500/20`
- **Tipografia**: `mono` ou `sans` de traços retos e precisos.
- **Estilo de borda**: `sharp` (cantos precisos, linhas de corte milimétricas).
- **Atmosfera**: Alta engenharia, precisão técnica, latência zero.

### 1.4 `dark-brutalist`
- **Nichos aplicáveis**: Tatuadores autorais, moda underground, fotografia artística, estúdios de design, advocacia disruptiva.
- **Paleta de cores**:
  - Fundo: `#09090b` (preto carvão)
  - Acento: `#ffffff` (titânio puro) e escala de cinzas médios `#a1a1aa`
  - Superfície dos cards: `#141417` com bordas sutis
- **Tipografia**: `display` em caixa alta com forte contraste.
- **Estilo de borda**: `subtle` ou `sharp`.
- **Atmosfera**: Autenticidade crua, sem ornamentos descartáveis, foco no portfólio visual.

### 1.5 `neo-pop-d2c`
- **Nichos aplicáveis**: Hamburguerias artesanais, energéticos, suplementação, streetwear, academias de crossfit/luta.
- **Paleta de cores**:
  - Fundo: `#070709`
  - Acento: `#ccff00` (volt neon) ou `#ff0055` (crimson vibrante)
  - Superfície dos cards: `#111116`
- **Tipografia**: `display` de alta energia.
- **Estilo de borda**: `pill` (cantos arredondados e botões em pílula).
- **Atmosfera**: Velocidade, intensidade, experiência pulsante 24/7.

---

## 2. Copywriting Sensorial de Alta Conversão

### 2.1 Lista Negra de Clichês Proibidos
A IA **nunca** deve escrever frases vazias como:
- ❌ *"O melhor da cidade"*
- ❌ *"Qualidade e excelência garantidas"*
- ❌ *"Venha conferir nossas novidades"*
- ❌ *"Atendimento humanizado e diferenciado"*
- ❌ *"Tradição e modernidade juntas"*

### 2.2 Regras de Ouro de Substituição
- **Prove com números**: Em vez de *"somos muito elogiados"*, use *"Nota 4.9 no Google com mais de 180 avaliações de clientes reais"*.
- **Descreva sensorialmente**: Em vez de *"comida gostosa"*, use *"Massa artesanal de fermentação lenta maturada por 48 horas e assada em forno a 450°C"*.
- **Destaque a comodidade inegociável**: *"Atendimento com hora marcada e tolerância de 15 minutos sem fila de espera"*, *"Ambiente com isolamento acústico e estacionamento privativo"*.
- **Preço e Duração nos Serviços**: Cada destaque deve conter faixa de valor realista (*"A partir de R$ 180"*) e tempo estimado de cadeira (*"1h 15m • Mais Pedido"*).

---

## 3. Estratégia de Economia de Tokens e Baixa Latência (Performance)

1. **Schema JSON Direto**: A IA não perde tempo gerando marcação HTML redundante. Ela gera diretamente a estrutura de dados tipada `CinematicPageData`.
2. **Compactação de Briefing**: Ao invés de enviar centenas de avaliações brutas, o sistema seleciona as 3 a 5 avaliações mais ricas em detalhes concretos.
3. **Modo Delta (Preservação de Dados Reais)**:
   - A IA preserva integralmente: `whatsapp`, `address`, `rating`, `openingHours`, `businessName` e URLs de fotos reais do Google Maps.
   - Ela reescreve apenas as propriedades que o usuário solicitou alterar (ex: headline, paleta ou novos itens de menu).
4. **Fallback Heurístico Instantâneo (Zero Custo / Zero Delay)**:
   - Se a chave de API da IA estiver ausente ou atingir limite de cota (Rate Limit), o motor aciona a matriz determinística de presets por nicho.
   - O usuário recebe a página instantaneamente em menos de 50 milissegundos sem telas de erro.

---

## 4. Integração Contínua com o Studio e a Prospecção

- **No Radar de Prospecção**: Puxa os dados reais da ficha (fotos originais em alta resolução, nota e comentários). A IA diagnostica a especialidade e injeta na página sem modelos estáticos rígidos.
- **No Studio**: O chat do copiloto recebe os comandos do usuário em linguagem natural e aplica as mudanças ao vivo no Canvas interativo em tempo real.
