# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FINAP é um aplicativo gamificado de educação financeira para adolescentes e jovens adultos brasileiros. O app apresenta o FIM, um assistente de IA financeiro brasileiro jovem e descontraído, alimentado pelo Google Gemini, que ajuda os usuários a aprender sobre gestão de dinheiro, economia e conceitos financeiros de forma envolvente e gamificada.

## Project Structure

O projeto está organizado em duas pastas principais:

```
finap-googleai/
├── frontend/          # Aplicação React (código atual)
└── backend/           # Backend com Firebase, ngrok, etc (a ser adicionado)
```

## Development Commands (Frontend)

```bash
# Navegar para a pasta do frontend
cd frontend

# Instalar dependências
npm install

# Executar servidor de desenvolvimento (inicia na porta 3000)
npm run dev

# Build para produção
npm run build

# Preview do build de produção
npm run preview
```

## Environment Setup

Crie um arquivo `.env.local` na pasta `frontend/` e configure sua chave da API do Gemini:

```
GEMINI_API_KEY=sua_chave_aqui
```

O Vite mapeia isso para `process.env.API_KEY` para uso na aplicação.

## Architecture

### Application Structure

O app segue um padrão de aplicação de página única (SPA) usando React com TypeScript:

- **frontend/App.tsx** - Ponto de entrada principal que gerencia o estado global de visualização usando o enum `ViewState`
- **frontend/index.tsx** - Inicialização do root do React
- **frontend/types.ts** - Definições de tipos centrais compartilhadas em toda a aplicação
- **frontend/constants.ts** - Dados mock e estado inicial (estatísticas do usuário, transações, missões, perguntas de quiz)

### View System

A navegação é baseada em estado, não em rotas. O app usa um enum `ViewState` para alternar entre diferentes telas:

- `ONBOARDING` - Experiência inicial do usuário (mostra primeiro, depois navega para Overview)
- `OVERVIEW` - Dashboard com estatísticas, missões e visão geral financeira
- `EXTRACT` - Histórico de transações e análise de gastos
- `LEARN` - Conteúdo educacional com cursos, módulos e quizzes (trilhas de aprendizado gamificadas)
- `SOCIAL` - Recursos sociais
- `ASSISTANT` - Interface de chat com FIM, o assistente de IA
- `PROFILE` - Perfil do usuário e configurações

A navegação é controlada pelo componente `BottomNav`, que fica oculto nas telas Profile e Onboarding.

### Gemini Integration

O app integra com a IA Gemini do Google via pacote `@google/genai`:

- **frontend/services/geminiService.ts** contém toda a lógica de IA
- `createChatSession()` inicializa um chat com a instrução de sistema que define a personalidade do FIM
- `sendMessageToFim()` lida com envio de mensagens e tratamento de erros
- FIM é configurado como um "assistente financeiro divertido, animado e educativo para adolescentes" brasileiro usando o modelo `gemini-2.5-flash`
- FIM usa gírias brasileiras da Geração Z como: "mano", "tipo assim", "tá ligado?", "slk", "na moral", "firmeza", "maneiro", etc.
- FIM aparece em dois contextos:
  1. A view Assistant dedicada (interface de chat completa)
  2. Mini chat de ajuda dentro da view Learn nas trilhas de cursos

### Component Architecture

**Componentes Reutilizáveis** (em `frontend/components/`):
- `Card` - Wrapper de card base para estilização consistente
- `BottomNav` - Barra de navegação persistente
- `FimMascot` - Personagem mascote animado com diferentes tamanhos e emoções

**Componentes de View** (em `frontend/views/`):
Cada view é um componente React autocontido que gerencia seu próprio estado e sub-navegação. Views principais:

- **Learn.tsx** tem seu próprio sistema complexo de sub-navegação com múltiplos modos de visualização:
  - `COURSES` - Visão geral da lista de cursos
  - `TRAIL` - Caminho de progressão de módulos (com design visual em zigue-zague)
  - `INTRO` - Detalhes do módulo antes de começar
  - `QUIZ` - Quiz interativo com sistema de vidas
  - `RESULT` - Tela de conclusão do quiz

  A view Learn também apresenta um mini chat do FIM que pode ser alternado para ajuda contextual.

### State Management

Atualmente usa estado local do React (useState). Não há biblioteca de gerenciamento de estado global. O estado é passado como props onde necessário:

- Estatísticas do usuário (`UserStats`) são inicializadas em constants e passadas para views
- Sessões de chat mantêm seu próprio estado com refs para o cliente Gemini
- Cada view gerencia seu próprio estado local independentemente

### Styling

- Usa Tailwind CSS com esquema de cores personalizado
- Cores personalizadas: `finap-primary` (teal), `finap-success` (emerald), `finap-gold`, `finap-bg`, `finap-dark`
- Design mobile-first com restrição de largura máxima (max-w-md mx-auto) para simular um app mobile
- Animações e transições usando utilitários Tailwind
- Sem arquivos CSS separados - toda estilização é inline com classes Tailwind

### Data Flow

O app atualmente usa dados mock de `constants.ts`:
- `INITIAL_USER_STATS` - Nível do usuário, XP, moedas, vidas, sequência
- `MOCK_TRANSACTIONS` - Histórico de transações de exemplo
- `DAILY_MISSIONS` - Missões/tarefas de exemplo
- `QUIZ_SAMPLE` - Perguntas de quiz para o módulo Learn

Estes são atualmente estáticos e não persistem entre sessões.

## Language and Localization

**IMPORTANTE**: Todo o aplicativo está em PT-BR (Português Brasileiro):
- Todos os textos da interface estão em português
- O FIM fala português brasileiro com gírias da Geração Z
- Categorias de transações: 'Alimentação', 'Transporte', 'Lazer', 'Educação', 'Outros'
- Sempre mantenha a consistência do idioma ao adicionar novos recursos

## Tech Stack

- **React 19** com TypeScript
- **Vite** para build e servidor de desenvolvimento
- **@google/genai** para integração com Gemini AI
- **Tailwind CSS** para estilização
- **Lucide React** para ícones
- **Recharts** para visualização de dados
- **Node.js** necessário para desenvolvimento

## Key Implementation Notes

1. **Injeção de Chave API**: A chave da API do Gemini é injetada em tempo de build via config `define` do Vite, mapeando `GEMINI_API_KEY` de .env.local para `process.env.API_KEY`

2. **Aliases de Path**: O alias `@/` resolve para a raiz do projeto (configurado em tsconfig.json e vite.config.ts)

3. **Sistema de Vidas**: A view Learn implementa um sistema de vidas onde respostas erradas no quiz deduzem vidas. Ficar sem vidas mostra uma tela de retry.

4. **Persistência de Chat**: Cada sessão de chat nas views Assistant e Learn usa uma ref para manter a instância do chat Gemini entre renders

5. **TypeScript**: TypeScript estrito com JSX como react-jsx. O projeto usa decorators experimentais e tem useDefineForClassFields definido como false.

## Future Integration with Backend

Quando o backend for adicionado:
- Integrar autenticação de usuários
- Persistir dados de usuário (stats, progresso, transações)
- Conectar com Firebase para armazenamento
- Implementar APIs RESTful ou GraphQL para comunicação frontend-backend
- Configurar ngrok para desenvolvimento/testes externos
