# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## REGRA CRITICA DE SEGURANCA - NUNCA IGNORAR

**NUNCA escreva chaves de API, tokens, senhas ou qualquer credencial em arquivos .md, README, documentacao ou qualquer arquivo que possa ser commitado no git.**

Isso inclui mas nao se limita a:
- API Keys (Firebase, Gemini, Meta, etc.)
- Private Keys
- Auth Tokens
- Senhas
- Client Secrets
- Service Account JSON contents

**Onde credenciais DEVEM estar:**
- Arquivos `.env` (que estao no .gitignore)
- Pasta `credentials/` (que esta no .gitignore)
- Variaveis de ambiente do sistema

**Se o usuario pedir para documentar credenciais, use SEMPRE placeholders:**
- `sua_api_key_aqui`
- `YOUR_API_KEY`
- `<sua-chave>`
- `***REDACTED***`

## Project Overview

FINAP e um aplicativo gamificado de educacao financeira para adolescentes e jovens adultos brasileiros. O app apresenta o FIM, um assistente de IA financeiro brasileiro jovem e descontraido, alimentado pelo Google Gemini, que ajuda os usuarios a aprender sobre gestao de dinheiro, economia e conceitos financeiros de forma envolvente e gamificada.

## Project Structure

O projeto esta organizado em duas pastas principais:

```
finap-googleai/
├── frontend/              # Aplicacao React + TypeScript
│   ├── components/        # Componentes reutilizaveis (BottomNav, Card, FimMascot, Toast)
│   ├── views/             # Telas principais (9 views)
│   ├── services/          # API clients (auth, dashboard, transactions, fim, learning, mission)
│   ├── contexts/          # AuthContext e GamificationContext
│   ├── utils/             # Utilitarios (splitBillCalculator, missionTracker)
│   └── types/             # TypeScript types
├── backend/               # Backend FastAPI + Firebase
│   ├── api/routes/        # Endpoints REST (auth, dashboard, transactions, gamification, learning, fim, whatsapp)
│   ├── services/          # Logica de negocio
│   ├── schemas/           # Validacao Pydantic
│   ├── core/              # Config, database, security
│   ├── models/            # Modelos de dados
│   └── scripts/           # Scripts auxiliares
└── credentials/           # Credenciais Firebase (gitignored)
```

**STATUS**: MVP 100% funcional e integrado. Backend e frontend totalmente conectados via API REST.

## Development Commands

### Frontend
```bash
cd frontend
npm install
npm run dev      # Inicia na porta 3000
npm run build    # Build para producao
npm run preview  # Preview do build
```

### Backend
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Architecture

### Frontend Structure

O frontend e uma SPA React com TypeScript usando navegacao baseada em estado:

- **App.tsx** - Componente raiz que gerencia ViewState global
- **views/** - Telas principais (Login, Register, Onboarding, Overview, Extract, Learn, Assistant, Social, Profile)
- **components/** - Componentes reutilizaveis (BottomNav, Card, FimMascot, Toast)
- **services/** - Comunicacao com API backend
- **contexts/** - AuthContext e GamificationContext para estado global
- **utils/** - Funcoes utilitarias (splitBillCalculator, missionTracker)

### View System

Estados de navegacao (ViewState enum):
- `LOGIN` - Tela de login
- `REGISTER` - Tela de registro
- `ONBOARDING` - Experiencia inicial do usuario
- `OVERVIEW` - Dashboard com estatisticas e missoes
- `EXTRACT` - Historico de transacoes
- `LEARN` - Trilhas de aprendizado gamificadas
- `SOCIAL` - Squad e divisao de contas
- `ASSISTANT` - Chat com FIM
- `PROFILE` - Perfil e configuracoes

### Backend Structure

API REST com FastAPI:

- **api/routes/** - Endpoints organizados por dominio (auth, dashboard, transactions, gamification, learning, fim, whatsapp)
- **services/** - Logica de negocio separada das rotas
- **schemas/** - Validacao com Pydantic
- **core/** - Configuracao (config.py, database.py, security.py)
- **models/** - Modelos de dados Firestore

### State Management

- **AuthContext** - Gerencia usuario autenticado e tokens JWT
- **GamificationContext** - Gerencia XP, moedas, vidas, missoes
- Estado local com useState para estado de componentes

### Gemini Integration

O app integra com Google Gemini de duas formas:
1. **Backend** - Atraves do fim_service.py para chat com contexto do usuario
2. **Frontend** - Diretamente via geminiService.ts para respostas rapidas

FIM e configurado como assistente financeiro brasileiro usando girias Gen Z:
- "mano", "tipo assim", "ta ligado?", "slk", "na moral", "firmeza", "maneiro"

### Styling

- Tailwind CSS com cores personalizadas (finap-primary, finap-success, finap-gold, finap-bg, finap-dark)
- Design mobile-first (max-w-md mx-auto)
- Sem arquivos CSS separados - estilizacao inline com Tailwind

## Key Features

### Learn.tsx - Sistema de Trilhas
Sub-navegacao complexa:
- `COURSES` - Lista de cursos
- `TRAIL` - Progressao de modulos (design zig-zag)
- `INTRO` - Detalhes do modulo
- `QUIZ` - Quiz com sistema de vidas
- `RESULT` - Resultado do quiz

### Social.tsx - Divisao de Contas
Funcionalidade estilo Splitwise:
- Criar eventos de divisao
- Adicionar despesas com divisao personalizada
- Ajustar valores individuais (+/-)
- Visualizar saldos (verde/vermelho)

### Split Bill Calculator
Utilitario em `frontend/utils/splitBillCalculator.ts`:
- `calculateMemberBalances()` - Saldo de cada membro
- `calculateDetailedDebts()` - Quem deve para quem
- `calculateTotalSpent()` - Total do evento

## API Endpoints

### Autenticacao
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/register`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/refresh-token`

### Dashboard
- `GET /api/v1/dashboard/overview/{user_id}`

### Transacoes
- `GET /api/v1/transactions`
- `POST /api/v1/transactions`
- `DELETE /api/v1/transactions/{id}`

### Gamificacao
- `GET /api/v1/gamification/stats`
- `POST /api/v1/gamification/mission/{id}/complete`

### Learning
- `GET /api/v1/learning/courses`
- `GET /api/v1/learning/courses/{id}/modules`

### FIM AI
- `POST /api/v1/fim/chat`

## Language and Localization

**IMPORTANTE**: Todo o aplicativo esta em PT-BR (Portugues Brasileiro):
- Todos os textos da interface em portugues
- FIM fala portugues brasileiro com girias Gen Z
- Categorias: 'Alimentacao', 'Transporte', 'Lazer', 'Educacao', 'Outros'
- Mantenha consistencia do idioma ao adicionar recursos

## Tech Stack

### Frontend
- React 19 + TypeScript
- Vite 6
- Tailwind CSS
- Axios
- Recharts
- Lucide React
- @google/genai

### Backend
- FastAPI >=0.115.0
- Python 3.11
- Firebase Admin
- Pydantic >=2.10.0
- python-jose (JWT)
- google-generativeai

## Key Implementation Notes

1. **Autenticacao**: JWT com access e refresh tokens, validados em cada requisicao
2. **Aliases de Path**: `@/` resolve para raiz do projeto (tsconfig + vite.config)
3. **Sistema de Vidas**: Quiz deduz vidas em erros, 0 vidas mostra tela de retry
4. **Persistencia**: Dados salvos no Firebase Firestore via backend
5. **CORS**: Backend configurado para aceitar localhost:3000-3003

## Scripts Auxiliares (Backend)

```bash
python scripts/create_test_user.py           # Cria usuario de teste
python scripts/seed_courses.py               # Popula cursos
python scripts/seed_learning_module.py       # Popula modulos de aprendizado
python scripts/setup_firebase_collections.py # Setup inicial do Firestore
python scripts/populate_vini_data.py         # Dados de teste (usuario Vini)
python scripts/test_whatsapp_meta.py         # Testa integracao WhatsApp
python scripts/get_phone_info.py             # Verifica telefone do usuario
python scripts/update_user_phone.py          # Atualiza telefone do usuario
```

## Environment Variables

### Backend (.env)
```
FIREBASE_CREDENTIALS_PATH=credentials/firebase-service-account.json
JWT_SECRET_KEY=sua_chave_secreta
JWT_ALGORITHM=HS256
GEMINI_API_KEY=sua_api_key
META_WHATSAPP_TOKEN=seu_token
META_PHONE_NUMBER_ID=seu_phone_id
META_VERIFY_TOKEN=seu_verify_token
```

### Frontend (.env.local)
```
VITE_GEMINI_API_KEY=sua_api_key
VITE_API_URL=http://localhost:8000
```
