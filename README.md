# FINAP - Educacao Financeira Gamificada

**Transformando a educacao financeira em uma jornada divertida para jovens brasileiros**

![Status](https://img.shields.io/badge/Status-MVP%20Completo-success)
![React](https://img.shields.io/badge/React-19-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![Firebase](https://img.shields.io/badge/Firebase-Ready-orange)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4)

---

## Sobre

O **FINAP** e uma plataforma de educacao financeira que revoluciona o aprendizado sobre gestao de dinheiro para jovens brasileiros (16-30 anos) atraves da combinacao de **gamificacao**, **inteligencia artificial** e **integracao com WhatsApp**.

Com o assistente virtual **FIM** (powered by Google Gemini AI), os usuarios aprendem a gerenciar suas financas enquanto completam desafios, ganham XP e desbloqueiam conquistas.

---

## Funcionalidades

### Dashboard Inteligente
- Visao geral financeira em tempo real
- Saldo, receitas e despesas do mes
- Graficos de pizza por categoria
- Missoes diarias com recompensas

### Gestao de Transacoes
- Registro rapido de gastos
- Categorizacao automatica
- Historico completo com filtros

### FIM - Assistente Financeiro IA
- Chat em tempo real com Google Gemini
- Personalidade brasileira Geracao Z
- Dicas personalizadas baseadas em comportamento

### Sistema de Gamificacao
- XP e niveis
- Moedas FINAP para trocar por recompensas
- Badges e conquistas
- Sistema de vidas nos quizzes

### Academia de Conhecimento
- Trilhas de aprendizado gamificadas
- Quizzes interativos com sistema de vidas
- Recompensas por conclusao

### Dividir Conta (Split Bill)
- Criar eventos de divisao de gastos
- Divisao personalizada entre participantes
- Visualizacao de saldos (quem deve/recebe)

### Integracao WhatsApp (Backend pronto)
- Registre gastos via mensagem
- Consulte saldo e extrato

---

## Tecnologias

### Frontend
- React 19 + TypeScript
- Vite 6 (build tool)
- Tailwind CSS
- Axios (HTTP client)
- Recharts (graficos)
- Lucide React (icones)
- @google/genai (Gemini)

### Backend
- FastAPI + Python 3.11
- Firebase Admin (Firestore)
- Pydantic (validacao)
- python-jose (JWT)
- google-generativeai (Gemini API)

### Infraestrutura
- Firebase Firestore (database)
- Firebase Authentication
- Google Cloud Platform

---

## Instalacao

### Pre-requisitos
- Node.js 18+
- Python 3.11+
- Git
- Conta Firebase
- Chave Gemini API

### Setup Rapido

#### 1. Clone o repositorio
```bash
git clone <url-do-repositorio>
cd finap-googleai
```

#### 2. Backend
```bash
cd backend

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instale dependencias
pip install -r requirements.txt

# Configure .env (copie de .env.example)
cp .env.example .env
# Edite .env com suas credenciais

# Execute o servidor
uvicorn main:app --reload --port 8000
```

Backend disponivel em: http://localhost:8000
Swagger Docs: http://localhost:8000/docs

#### 3. Frontend
```bash
cd frontend

# Instale dependencias
npm install

# Configure .env.local
# VITE_GEMINI_API_KEY=sua_chave_aqui

# Execute o app
npm run dev
```

Frontend disponivel em: http://localhost:3000

---

## Estrutura do Projeto

```
finap-googleai/
├── frontend/          # Aplicacao React + TypeScript
│   ├── components/    # Componentes reutilizaveis
│   ├── views/         # Telas principais
│   ├── services/      # Comunicacao com API
│   ├── contexts/      # React Context (Auth, Gamification)
│   ├── utils/         # Funcoes utilitarias
│   └── types/         # TypeScript types
│
├── backend/           # API FastAPI + Firebase
│   ├── api/routes/    # Endpoints REST
│   ├── services/      # Logica de negocio
│   ├── schemas/       # Validacao Pydantic
│   ├── core/          # Configuracao central
│   ├── models/        # Modelos de dados
│   └── scripts/       # Scripts auxiliares
│
└── credentials/       # Credenciais (gitignored)
```

---

## Endpoints da API

### Autenticacao
- `POST /api/v1/auth/register` - Cadastro
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Dados do usuario

### Dashboard
- `GET /api/v1/dashboard/overview/{user_id}` - Overview

### Transacoes
- `GET /api/v1/transactions` - Listar
- `POST /api/v1/transactions` - Criar
- `DELETE /api/v1/transactions/{id}` - Deletar

### Gamificacao
- `GET /api/v1/gamification/stats` - Estatisticas
- `POST /api/v1/gamification/mission/{id}/complete` - Completar missao

### Learning
- `GET /api/v1/learning/courses` - Listar cursos
- `GET /api/v1/learning/courses/{id}/modules` - Modulos

### FIM AI
- `POST /api/v1/fim/chat` - Enviar mensagem

---

## Scripts Uteis

### Frontend
```bash
npm run dev      # Servidor de desenvolvimento
npm run build    # Build para producao
npm run preview  # Preview do build
```

### Backend
```bash
uvicorn main:app --reload --port 8000  # Servidor dev

# Scripts auxiliares
python scripts/create_test_user.py      # Criar usuario de teste
python scripts/seed_courses.py          # Popular cursos
python scripts/seed_learning_module.py  # Popular modulos
python scripts/setup_firebase_collections.py  # Setup inicial Firebase
python scripts/test_whatsapp_meta.py    # Testar integracao WhatsApp
```

---

## Documentacao

- [CLAUDE.md](./CLAUDE.md) - Instrucoes para desenvolvimento com Claude Code
- [DOCUMENTO_ESCOPO_ENTREGA.md](./DOCUMENTO_ESCOPO_ENTREGA.md) - Escopo completo do MVP
- [GUIA-SETUP-WHATSAPP-META.md](./GUIA-SETUP-WHATSAPP-META.md) - Configuracao WhatsApp

---

## Status do Projeto

| Componente | Status |
|------------|--------|
| Backend (FastAPI) | 100% Funcional |
| Frontend (React) | 100% Funcional |
| Autenticacao | Completo |
| Dashboard/Overview | Completo |
| Transacoes | Completo |
| Gamificacao | Completo |
| FIM (Assistente IA) | Completo |
| Learning/Trilhas | Completo |
| WhatsApp | Backend pronto |
| Dividir Conta | Completo (mock) |

**MVP Completo e Funcional**

---

## Variaveis de Ambiente

### Backend (.env)
```
# Firebase
FIREBASE_CREDENTIALS_PATH=caminho/para/credenciais.json

# JWT
JWT_SECRET_KEY=sua_chave_secreta
JWT_ALGORITHM=HS256

# Gemini
GEMINI_API_KEY=sua_api_key

# WhatsApp Meta (opcional)
META_WHATSAPP_TOKEN=seu_token
META_PHONE_NUMBER_ID=seu_phone_id
META_VERIFY_TOKEN=seu_verify_token
```

### Frontend (.env.local)
```
VITE_GEMINI_API_KEY=sua_api_key
VITE_API_URL=http://localhost:8000
```

---

## Licenca

Este projeto e proprietario. Todos os direitos reservados.

---

**FINAP - Educacao Financeira para a Geracao Z**
Versao 1.0.0 | MVP Completo
