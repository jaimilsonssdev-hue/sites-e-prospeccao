---
trigger: always_on
---

# Diretriz para Adição de Componentes Visuais (shadcn/ui)

Sempre que o usuário solicitar um componente visual (como botões, carrosséis, modais, drawers, tabs, cards, tabelas, efeitos visuais ou animações):

1. **Execução Automática via CLI**: Execute diretamente no terminal o comando nativo:
   ```bash
   npx shadcn@latest add <componente> -y
   ```
   *(ou `npx shadcn@latest add <url-do-registro> -y` para registries open-source como Magic UI, Aceternity ou 21st.dev)*.

2. **Injeção Direta da Nuvem**: O CLI busca e injeta o código TypeScript/Tailwind automaticamente na pasta `@/components/ui`, instalando dependências necessárias sem exigir que o usuário precise baixar ou copiar nada manualmente.

3. **Integração Imediata**: Utilize o componente importando de `@/components/ui/<nome-do-componente>` no layout ou página indicada.

