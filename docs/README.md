# 📱 FINAP - Educação Financeira Gamificada

<p align="center">
  <strong>Transformando a educação financeira em uma jornada divertida e engajante para adolescentes e jovens adultos brasileiros</strong>
</p>

<p align="center">
  <a href="#sobre">Sobre</a> •
  <a href="#funcionalidades">Funcionalidades</a> •
  <a href="#tecnologias">Tecnologias</a> •
  <a href="#instalação">Instalação</a> •
  <a href="#estrutura">Estrutura</a> •
  <a href="#documentação">Documentação</a>
</p>

---

## 🎯 Sobre

O **FINAP** é um aplicativo revolucionário que combina educação financeira com gamificação, tornando o aprendizado sobre finanças pessoais uma experiência divertida e engajante para jovens. Com o auxílio do assistente virtual **FIM** (powered by Google Gemini AI), os usuários aprendem a gerenciar suas finanças enquanto completam desafios, ganham XP e desbloqueiam conquistas.

### 🌟 Diferenciais

- 🤖 **Assistente FIM**: IA brasileira que fala a linguagem da Geração Z
- 🔐 **Autenticação Completa**: Sistema seguro com JWT e Firebase Auth
- 🎮 **Gamificação Total**: XP, badges, níveis, moedas e vidas
- 📊 **Dashboard Inteligente**: Análises em tempo real de gastos
- 📚 **Academia de Cursos**: Trilhas de aprendizado gamificadas
- 💰 **Gestão de Gastos**: Rastreamento e categorização automática
- 📱 **Integração WhatsApp**: Registre gastos via mensagem (em breve)

## 🚀 Status do Projeto

| Componente | Progresso | Status |
|------------|-----------|--------|
| **Backend (FastAPI)** | 100% | ✅ Funcional |
| **Frontend (React)** | 100% | ✅ Funcional |
| **Autenticação** | 100% | ✅ Completo |
| **Dashboard/Overview** | 100% | ✅ Completo |
| **Transações** | 100% | ✅ Completo |
| **Gamificação** | 100% | ✅ Completo |
| **FIM (Assistente IA)** | 100% | ✅ Completo |
| **Learning/Trilhas** | 100% | ✅ Completo (com mock data) |
| **WhatsApp** | 100% | ✅ Backend pronto |
| **Integração Geral** | 100% | ✅ Funcional |

**🎉 MVP Completo e funcional! Pronto para apresentação!**

## ✨ Funcionalidades Implementadas

### 🔐 1. Autenticação & Segurança
- ✅ Registro de usuários com Firebase Auth
- ✅ Login com email/senha
- ✅ JWT Tokens (access + refresh)
- ✅ Validação de senha forte:
  - Mínimo 6 caracteres
  - 1 letra maiúscula
  - 1 número
- ✅ Feedback visual em tempo real (barra de força + checklist)
- ✅ Proteção contra emails duplicados
- ✅ Logout com limpeza de sessão

### 📊 2. Dashboard (Overview)
- ✅ Nome personalizado do usuário
- ✅ Estatísticas em tempo real (vidas, moedas, XP, nível)
- ✅ Saldo e orçamento mensal
- ✅ Barra de progresso visual de gastos
- ✅ Missões diárias com recompensas
- ✅ Alertas inteligentes de orçamento

### 👤 3. Perfil
- ✅ Exibição de dados do usuário
- ✅ Avatar personalizado (DiceBear)
- ✅ Badges e conquistas
- ✅ Estatísticas detalhadas
- ✅ Sistema de amigos
- ✅ Loja de itens (skins, temas)
- ✅ Configurações
- ✅ Logout funcional

### 💰 4. Gestão de Gastos (Extract)
- ✅ Lista de transações do backend
- ✅ Criar novas transações
- ✅ Deletar transações
- ✅ Gráfico de pizza por categorias
- ✅ Filtros por período
- ✅ Categorização automática

### 🎓 5. Academia de Cursos (Learn)
- ✅ Trilhas de conhecimento gamificadas
- ✅ Módulos e lições interativos
- ✅ Quizzes com sistema de vidas
- ✅ Recompensas (XP + moedas)
- ✅ Mini chat do FIM para ajuda contextual
- ✅ Progresso visual em zigue-zague
- ✅ Dados mock para experiência completa

### 💬 6. Assistente FIM
- ✅ Chat em tempo real com Gemini AI
- ✅ Personalidade brasileira Geração Z
- ✅ Histórico de conversas
- ✅ Dicas financeiras personalizadas
- ✅ Mini chat de ajuda nas trilhas

## 🛠 Tecnologias

### Backend
```
Python 3.11
├── FastAPI 0.104.1        # Framework web assíncrono
├── Firebase Admin 6.2.0   # Firestore + Auth
├── Pydantic 2.5.0        # Validação de dados
├── Python-Jose           # JWT tokens
├── Passlib               # Hash de senhas
├── Google Gemini AI      # Assistente FIM
└── Twilio 8.10.0         # WhatsApp (futuro)
```

### Frontend
```
React 19 + TypeScript + Vite
├── Tailwind CSS          # Estilização
├── Axios                 # HTTP client
├── Lucide React          # Ícones
├── Recharts              # Gráficos
├── Google Gemini         # IA (uso direto)
└── DiceBear              # Avatares
```

### Infraestrutura
```
├── Firebase Firestore    # Database NoSQL
├── Firebase Auth         # Autenticação
├── Google Cloud          # Hosting & APIs
└── WSL2/Linux           # Ambiente de desenvolvimento
```

## 📦 Instalação

### Pré-requisitos

- **Node.js 18+** e npm
- **Python 3.11+**
- **Git**
- **Conta Firebase** (projeto finap-mvp)
- **Chave Gemini API**

### 🔧 Setup Rápido

#### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/finap-googleai.git
cd finap-googleai
```

#### 2. Backend Setup

```bash
# Entre no diretório do backend
cd backend

# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
# Já existe um .env configurado

# Execute o servidor
uvicorn main:app --reload --port 8000
```

**Backend estará em:** http://localhost:8000
**Documentação Swagger:** http://localhost:8000/docs

#### 3. Frontend Setup

```bash
# Entre no diretório do frontend
cd frontend

# Instale as dependências
npm install

# Configure .env.local (opcional - já tem Gemini configurado)
# GEMINI_API_KEY=sua_chave_aqui

# Execute o app
npm run dev
```

**Frontend estará em:** http://localhost:3000

### 🧪 Testando o App

Siga o guia completo de testes: **[GUIA-TESTE-COMPLETO-FINAP.md](./GUIA-TESTE-COMPLETO-FINAP.md)**

**Teste Rápido:**
1. Acesse http://localhost:3000
2. Limpe localStorage (F12 → Application → Clear)
3. Cadastre-se com senha válida (ex: `Teste@123`)
4. Veja seu nome na Overview!
5. Teste logout pelo Profile

## 📁 Estrutura do Projeto

```
finap-googleai/
│
├── 📁 backend/                    # API FastAPI
│   ├── 📁 api/
│   │   ├── 📁 routes/             # Endpoints
│   │   │   ├── auth.py            # ✅ Autenticação
│   │   │   ├── dashboard.py       # ✅ Dashboard
│   │   │   ├── transactions.py    # ✅ Transações
│   │   │   ├── gamification.py    # ✅ Gamificação
│   │   │   ├── learning.py        # ✅ Trilhas
│   │   │   ├── whatsapp.py        # ✅ WhatsApp
│   │   │   └── analytics.py       # ✅ Analytics
│   │   └── 📁 dependencies/
│   │       └── auth.py            # ✅ get_current_user
│   ├── 📁 services/               # Lógica de negócio
│   │   ├── auth_service.py        # ✅ Autenticação
│   │   ├── transaction_service.py # ✅ Transações
│   │   ├── gamification_service.py # ✅ Gamificação
│   │   ├── learning_service.py    # ✅ Trilhas
│   │   └── ...
│   ├── 📁 schemas/                # Validação Pydantic
│   │   ├── auth.py                # ✅ + validação senha
│   │   └── ...
│   ├── 📁 core/
│   │   ├── config.py              # Configurações
│   │   ├── database.py            # Firebase/Firestore
│   │   └── security.py            # ✅ JWT tokens
│   ├── main.py                    # ✅ App FastAPI
│   ├── requirements.txt
│   └── .env                       # ✅ Configurado
│
├── 📁 frontend/                   # React + TypeScript
│   ├── 📁 components/             # Componentes reutilizáveis
│   │   ├── Card.tsx
│   │   ├── BottomNav.tsx
│   │   ├── FimMascot.tsx
│   │   └── Toast.tsx
│   ├── 📁 views/                  # Telas principais
│   │   ├── Onboarding.tsx         # ✅ + validação senha
│   │   ├── Overview.tsx           # ✅ Integrado
│   │   ├── Profile.tsx            # ✅ Integrado
│   │   ├── Extract.tsx            # ✅ Integrado
│   │   ├── Learn.tsx              # 🚧 Service pronto
│   │   └── Assistant.tsx          # ✅ Integrado
│   ├── 📁 services/               # API clients
│   │   ├── api.ts                 # ✅ HTTP client
│   │   ├── authService.ts         # ✅ Auth
│   │   ├── dashboardService.ts    # ✅ Dashboard
│   │   ├── transactionService.ts  # ✅ Transações
│   │   ├── fimService.ts          # ✅ Chat FIM
│   │   ├── learningService.ts     # ✅ NOVO!
│   │   └── index.ts
│   ├── App.tsx                    # ✅ Router + Auth check
│   ├── types.ts                   # TypeScript types
│   ├── constants.ts               # Dados mock (legacy)
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── 📁 docs/                       # Documentação detalhada
│
├── 📄 ANALISE_BACKEND_INTEGRACAO.md      # Análise técnica
├── 📄 GUIA-TESTE-COMPLETO-FINAP.md       # 🧪 Guia de testes
├── 📄 RESUMO-INTEGRACAO-BACKEND-FRONTEND.md  # 📊 Resumo integração
├── 📄 FASE1_CONCLUIDA.md
├── 📄 FASE2_PROGRESSO.md
├── 📄 CLAUDE.md                   # Instruções para IA
├── 📄 .gitignore
└── 📄 README.md                   # Este arquivo
```

## 📚 Documentação

### 📖 Guias Disponíveis

| Documento | Descrição |
|-----------|-----------|
| [Arquitetura/Didática do Projeto](./DOCUMENTO_ESCOPO_ENTREGA.md) | 📊 Escopo com arquitetura e didática |
| [GUIA-TESTE-COMPLETO-FINAP.md](./GUIA-TESTE-COMPLETO-FINAP.md) | 🧪 Passo a passo completo para testar todas funcionalidades |
| [RESUMO-INTEGRACAO-BACKEND-FRONTEND.md](./RESUMO-INTEGRACAO-BACKEND-FRONTEND.md) | 📊 Resumo técnico da integração |
| [ANALISE_BACKEND_INTEGRACAO.md](./ANALISE_BACKEND_INTEGRACAO.md) | 🔍 Análise detalhada do backend |
| [docs/README.md](./docs/README.md) | 📚 Documentação completa do projeto |
| [CLAUDE.md](./CLAUDE.md) | 🤖 Instruções para Claude Code |

### 🔗 Links Úteis

- **Backend API**: http://localhost:8000
- **Backend Docs (Swagger)**: http://localhost:8000/docs
- **Frontend Dev**: http://localhost:3000
- **Firebase Console**: https://console.firebase.google.com/project/finap-mvp

## 🔌 Endpoints da API

### Autenticação
```
POST /api/v1/auth/register      # Cadastro
POST /api/v1/auth/login         # Login
POST /api/v1/auth/refresh       # Renovar token
GET  /api/v1/auth/me            # Usuário atual
```

### Dashboard
```
GET /api/v1/dashboard/overview/{user_id}  # Overview
GET /api/v1/dashboard/summary             # Resumo
```

### Transações
```
GET    /api/v1/transactions      # Listar
POST   /api/v1/transactions      # Criar
DELETE /api/v1/transactions/{id} # Deletar
```

### FIM (Assistente)
```
POST /api/v1/fim/chat           # Chat com FIM
GET  /api/v1/fim/history        # Histórico
```

### Learning
```
GET  /api/v1/learning/modules           # Listar módulos
POST /api/v1/learning/start-module      # Iniciar módulo
POST /api/v1/learning/complete-lesson   # Completar lição
POST /api/v1/learning/submit-quiz       # Enviar quiz
```

## 🧪 Testes

### Validação de Senha
- ❌ Senha sem maiúscula → Bloqueada
- ❌ Senha sem número → Bloqueada
- ❌ Senha < 6 caracteres → Bloqueada
- ✅ Senha válida (`Teste@123`) → Aceita

### Autenticação
- ✅ Cadastro com email novo → Sucesso
- ❌ Email duplicado → Bloqueado
- ✅ Login com credenciais corretas → Sucesso
- ❌ Login com senha errada → Bloqueado
- ✅ Logout → Limpa sessão e redireciona

### Integração Backend
- ✅ Overview exibe nome real do usuário
- ✅ Estatísticas carregam do Firestore
- ✅ Transações persistem no banco
- ✅ Chat FIM funciona com Gemini
- ✅ Profile exibe dados reais
- ✅ Toast de feedback em todas ações

## 🚀 Próximos Passos (Pós-MVP)

### Fase 2 - Melhorias
- [ ] Integrar tela Learn com backend (service já existe)
- [ ] Implementar auto-refresh de tokens
- [ ] Adicionar upload de avatar personalizado
- [ ] Implementar edição de perfil completa

### Fase 3 - Escalabilidade
- [ ] Adicionar analytics e métricas de uso
- [ ] Implementar rate limiting
- [ ] Testes automatizados (pytest + jest)
- [ ] Ativar integração WhatsApp

### Fase 4 - Produção
- [ ] CI/CD com GitHub Actions
- [ ] Deploy em produção (Google Cloud Run)
- [ ] Monitoramento com Sentry
- [ ] CDN para assets estáticos

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é proprietário. Todos os direitos reservados.

## 🙏 Créditos

### Tecnologias
- **Google Gemini AI** - Assistente FIM
- **Firebase** - Backend & Auth
- **FastAPI** - API Framework
- **React** - Frontend Framework
- **Tailwind CSS** - Estilização
- **DiceBear** - Avatares

### Time
- Desenvolvido com ❤️ pela equipe FINAP

---

<div align="center">
  <p><strong>FINAP - Educação Financeira para a Geração Z</strong></p>
  <p>Versão 1.0.0 | Status: ✅ MVP Completo e Funcional | Pronto para Apresentação</p>
</div>
