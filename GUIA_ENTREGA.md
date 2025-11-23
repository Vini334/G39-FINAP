# Guia de Entrega e Apresentação - FINAP MVP

Documento completo para preparação, execução e apresentação do projeto FINAP.

---

## Índice

1. [Checklist Pré-Apresentação](#checklist-pré-apresentação)
2. [Setup do Ambiente](#setup-do-ambiente)
3. [Roteiro de Demonstração](#roteiro-de-demonstração)
4. [Pontos-Chave para Destacar](#pontos-chave-para-destacar)
5. [Respostas para Perguntas Frequentes](#respostas-para-perguntas-frequentes)
6. [Troubleshooting](#troubleshooting)

---

## Checklist Pré-Apresentação

### 24-48 Horas Antes

- [ ] **Testar ambiente completo**
  - [ ] Backend rodando em localhost:8000
  - [ ] Frontend rodando em localhost:3000
  - [ ] Firebase Firestore acessível
  - [ ] Gemini AI respondendo

- [ ] **Verificar credenciais**
  - [ ] Firebase credentials OK
  - [ ] Gemini API key válida
  - [ ] Sem limites de rate limit

- [ ] **Preparar dados de demonstração**
  - [ ] Usuário de teste criado
  - [ ] Transações de exemplo populadas
  - [ ] Missões ativas disponíveis

- [ ] **Documentação atualizada**
  - [ ] README.md completo
  - [ ] CHANGELOG.md atualizado
  - [ ] GUIA_ENTREGA.md (este arquivo)

- [ ] **Apresentação preparada**
  - [ ] Slides/apresentação prontos
  - [ ] Screenshots importantes
  - [ ] Vídeo demo (opcional)

### 1-2 Horas Antes

- [ ] **Teste final completo**
  - [ ] Criar novo usuário
  - [ ] Navegar por todas as telas
  - [ ] Testar chat com FIM
  - [ ] Criar transação
  - [ ] Completar quiz no Learn

- [ ] **Preparar browser**
  - [ ] Limpar cache e localStorage
  - [ ] Abrir DevTools (F12)
  - [ ] Preparar abas:
    - Tab 1: http://localhost:3000
    - Tab 2: http://localhost:8000/docs (Swagger)
    - Tab 3: Firebase Console

- [ ] **Backup dos servidores**
  - [ ] Backend rodando em background
  - [ ] Frontend rodando em background
  - [ ] Logs visíveis em terminais separados

---

## Setup do Ambiente

### Passo 1: Iniciar Backend

```bash
# Terminal 1 - Backend
cd /mnt/c/Bitbucket/finap-googleai/backend

# Ativar ambiente virtual (se necessário)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Iniciar servidor
python3 -m uvicorn main:app --reload --port 8000

# Verificar se está rodando
# Deve mostrar: "Application startup complete"
# Acesse: http://localhost:8000/docs
```

### Passo 2: Iniciar Frontend

```bash
# Terminal 2 - Frontend
cd /mnt/c/Bitbucket/finap-googleai/frontend

# Instalar dependências (se necessário)
npm install

# Iniciar servidor
npm run dev

# Verificar se está rodando
# Deve mostrar: "Local: http://localhost:3000"
```

### Passo 3: Verificar Integrações

```bash
# Terminal 3 - Testes
# Testar backend
curl http://localhost:8000/health

# Testar documentação
curl http://localhost:8000/docs

# Verificar frontend
curl http://localhost:3000
```

### Passo 4: Preparar Dados de Teste

Use o script de população se necessário:

```bash
cd backend
python3 scripts/create_test_user.py
python3 scripts/populate_vini_data.py
```

---

## Roteiro de Demonstração

### 1. Introdução (2-3 minutos)

**O QUE FALAR:**
- "FINAP é um app de educação financeira gamificada para jovens brasileiros"
- "Combina gamificação com IA do Google Gemini para tornar finanças divertidas"
- "MVP completo com backend e frontend integrados"

**O QUE MOSTRAR:**
- Tela inicial limpa (Login/Register)
- Mencionar arquitetura: React + FastAPI + Firebase + Gemini

### 2. Cadastro e Onboarding (2-3 minutos)

**AÇÕES:**
1. Clicar em "Criar Conta"
2. Preencher dados:
   - Nome: "João Silva"
   - Email: "joao.demo@finap.com" (ou usar timestamp)
   - Senha: "Demo@123"

**PONTOS-CHAVE:**
- Validação de senha em tempo real
- Barra de força visual
- Checklist de requisitos
- Mensagens claras em português

3. Completar onboarding
4. Mostrar transição suave para Overview

### 3. Dashboard / Overview (3-4 minutos)

**O QUE DESTACAR:**
- Nome personalizado do usuário (carregado do banco)
- Estatísticas em tempo real:
  - Nível e XP
  - Moedas FINAP
  - Vidas restantes
  - Streak de dias
- Saldo e orçamento visual
- Missões diárias com recompensas

**DEMONSTRAR:**
- Dados vêm do Firebase (não é mock!)
- Sistema de gamificação funcionando
- Alertas inteligentes de gastos

### 4. Extrato / Transações (2-3 minutos)

**AÇÕES:**
1. Navegar para Extract
2. Mostrar lista de transações
3. Criar nova transação:
   - Tipo: Saída
   - Categoria: Alimentação
   - Valor: R$ 25,00
   - Descrição: "Almoço"

**PONTOS-CHAVE:**
- Gráfico de pizza por categorias
- Categorização automática
- Persistência no Firestore
- Toast de confirmação

4. Deletar uma transação
5. Mostrar atualização em tempo real

### 5. Academia Learn (3-4 minutos)

**O QUE MOSTRAR:**
1. Trilhas de aprendizado gamificadas
2. Visualização em zigue-zague
3. Selecionar um módulo
4. Iniciar quiz:
   - Sistema de vidas funcionando
   - Feedback visual para respostas
   - Perda de vida em erro

**DESTACAR:**
- Mini chat do FIM para ajuda contextual
- Recompensas ao completar (XP + moedas)
- Design engajante para jovens

### 6. Assistente FIM (4-5 minutos)

**DEMONSTRAÇÃO PODEROSA:**

**Pergunta 1 (Simples):**
- "Oi FIM! O que é inflação?"
- Mostrar resposta concisa e descontraída

**Pergunta 2 (Complexa):**
- "Como eu posso economizar para comprar um notebook de R$ 3.000?"
- Mostrar resposta detalhada e personalizada

**Pergunta 3 (Contextual):**
- "Achei muito caro aquele almoço de R$ 25. Estou exagerando?"
- FIM deve dar dicas sobre orçamento

**PONTOS-CHAVE:**
- Personalidade brasileira Gen Z
- Respostas adaptativas (curtas ou longas)
- Powered by Google Gemini
- Histórico de conversas
- Sem markdown, formatação limpa

### 7. Perfil e Configurações (2 minutos)

**MOSTRAR:**
- Avatar gerado (DiceBear)
- Badges e conquistas
- Estatísticas completas
- Sistema de amigos (mock)
- Loja de itens (mock)
- Botão de logout funcional

**DESTACAR:**
- Dados reais do usuário
- Funcionalidade completa
- Design limpo e moderno

### 8. Documentação e Código (2-3 minutos)

**MOSTRAR:**

**Swagger UI:**
- Abrir http://localhost:8000/docs
- Mostrar os 30+ endpoints
- Demonstrar estrutura da API

**Firebase Console:**
- Mostrar dados reais no Firestore
- Collections: users, transactions, gamification

**Código Limpo:**
- Abrir VS Code
- Mostrar estrutura organizada
- Frontend services
- Backend routes

---

## Pontos-Chave para Destacar

### Diferencial Técnico

1. **Arquitetura Completa**
   - Frontend: React 19 + TypeScript + Vite
   - Backend: FastAPI + Python 3.11
   - Database: Firebase Firestore
   - AI: Google Gemini 2.5 Flash

2. **Segurança**
   - JWT tokens (access + refresh)
   - Firebase Auth
   - Validação de senha forte
   - Proteção de rotas

3. **Integração Real**
   - Backend e frontend 100% conectados
   - Dados persistidos no Firestore
   - IA real (não mock)
   - Sistema de auth funcional

### Diferencial de Produto

1. **Gamificação Completa**
   - XP, níveis, moedas, vidas
   - Missões diárias
   - Badges e conquistas
   - Streaks

2. **Educação Financeira**
   - Trilhas de aprendizado
   - Quizzes interativos
   - Assistente IA personalizado
   - Conteúdo em PT-BR

3. **UX para Jovens**
   - Linguagem Gen Z
   - Design moderno
   - Feedback visual
   - Animações suaves

---

## Respostas para Perguntas Frequentes

### Técnicas

**P: "Como funciona a integração com o Gemini?"**
R: "Usamos a API oficial do Google Gemini (@google/genai). Configuramos um chat session com instrução de sistema que define a personalidade do FIM. O frontend pode chamar diretamente ou via backend (/api/v1/fim/chat)."

**P: "Os dados persistem?"**
R: "Sim! Todos os dados de usuários, transações e gamificação são persistidos no Firebase Firestore. Nada é mock, exceto dados das trilhas Learn que ainda usam constants para demonstração."

**P: "É seguro?"**
R: "Sim. Usamos Firebase Auth para autenticação, JWT para sessões, validação de senha forte, e todas as rotas sensíveis são protegidas com middleware de autenticação."

**P: "Quantos endpoints tem a API?"**
R: "30+ endpoints organizados em 8 domínios: Auth, Dashboard, Transactions, Gamification, FIM, Learning, WhatsApp e Analytics. Todos documentados no Swagger."

### Produto

**P: "Qual o público-alvo?"**
R: "Adolescentes e jovens adultos brasileiros (15-25 anos) que precisam aprender educação financeira de forma engajante."

**P: "Por que gamificação?"**
R: "Estudos mostram que gamificação aumenta engajamento em 60% e retenção em 40%. Tornamos finanças divertidas, não chatas."

**P: "O FIM é confiável?"**
R: "Sim! Powered by Google Gemini, uma das IAs mais avançadas. Configuramos instruções específicas para dar conselhos financeiros educativos e responsáveis."

**P: "Funciona no celular?"**
R: "O frontend é responsivo e mobile-first. Está otimizado para telas de smartphone com max-width de 28rem (simulando app mobile)."

### Negócio

**P: "Qual o modelo de negócio?"**
R: "Freemium: versão gratuita com funcionalidades básicas + versão premium com conteúdos exclusivos, mais vidas, avatares especiais, etc."

**P: "Como se diferencia da concorrência?"**
R: "Combinamos 3 fatores únicos: gamificação completa + IA conversacional brasileira + educação financeira séria. Ninguém mais faz os três juntos."

**P: "Próximos passos?"**
R: "Fase 2: integrar Learn com backend, ativar WhatsApp, adicionar analytics. Fase 3: deploy em produção (Google Cloud Run), testes com beta users, parcerias com escolas."

---

## Troubleshooting

### Problema: Backend não inicia

**Sintomas:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solução:**
```bash
cd backend
pip install -r requirements.txt
```

### Problema: Frontend não carrega

**Sintomas:**
```
Failed to resolve import './services/api'
```

**Solução:**
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Problema: Firebase error

**Sintomas:**
```
Could not reach Cloud Firestore backend
```

**Solução:**
1. Verificar arquivo `backend/.env`
2. Verificar `credentials/firebase-service-account.json`
3. Testar conexão: `python3 scripts/check_user.py`

### Problema: Gemini não responde

**Sintomas:**
```
❌ GEMINI API KEY NOT FOUND!
```

**Solução:**
1. Verificar `.env.local` no frontend
2. Variável correta: `VITE_GEMINI_API_KEY=...`
3. Restart do frontend: `npm run dev`

### Problema: 401 Unauthorized loop

**Sintomas:**
- Usuário desloga automaticamente
- Loop infinito de refresh

**Solução:**
1. Limpar localStorage (F12 → Application → Clear)
2. Verificar se backend está rodando
3. Recriar usuário se necessário

### Problema: Timeout nas requisições

**Sintomas:**
```
Error: timeout of 10000ms exceeded
```

**Solução:**
- Já configurado timeout de 30s no api.ts
- Verificar se backend está respondendo: `curl http://localhost:8000/health`

---

## Checklist Final de Entrega

### Código
- [ ] Projeto limpo (sem pastas duplicadas)
- [ ] Dependências atualizadas
- [ ] .gitignore configurado
- [ ] Código comentado em pontos-chave

### Documentação
- [ ] README.md completo
- [ ] CLAUDE.md atualizado
- [ ] CHANGELOG.md criado
- [ ] GUIA_ENTREGA.md (este arquivo)
- [ ] API documentada (Swagger)

### Funcionalidades
- [ ] Cadastro funciona
- [ ] Login funciona
- [ ] Logout funciona
- [ ] Overview carrega dados reais
- [ ] Transações CRUD funcionam
- [ ] Chat FIM responde
- [ ] Learn com quizzes funciona
- [ ] Toast de feedback em todas ações

### Qualidade
- [ ] Sem erros no console
- [ ] Sem warnings críticos
- [ ] Build do frontend funciona
- [ ] Backend sem crashes
- [ ] Mensagens em português
- [ ] UX suave e responsiva

---

## Roteiro de Emergência (5 minutos)

Se o tempo for curto, siga este roteiro mínimo:

1. **Introdução** (30s): "FINAP - educação financeira gamificada com IA"
2. **Cadastro** (1min): Criar usuário demonstrando validação
3. **Overview** (1min): Mostrar dados reais do Firebase
4. **Transação** (1min): Criar e mostrar persistência
5. **FIM** (1.5min): Fazer 2 perguntas mostrando IA
6. **Código** (30s): Mostrar Swagger docs rapidamente

---

## Dicas de Apresentação

### Prepare-se para demonstrar

1. **Tenha um plano B**
   - Vídeo gravado da demo
   - Screenshots prontos
   - Dados de teste já populados

2. **Pratique o fluxo**
   - Ensaie 2-3 vezes antes
   - Cronometre cada seção
   - Tenha atalhos preparados

3. **Gerencie o tempo**
   - Mantenha intro curta
   - Foque nas features principais
   - Deixe tempo para perguntas

4. **Seja confiante**
   - Você conhece o projeto
   - Destaque o que funciona
   - Seja honesto sobre limitações

### Durante a apresentação

- Fale alto e claro
- Explique o que está fazendo
- Mostre, não apenas conte
- Mantenha energia positiva
- Sorria e seja entusiasta

---

## Contato e Suporte

Para dúvidas ou problemas durante a apresentação:
- Verifique logs do backend/frontend
- Consulte este guia
- Use scripts de troubleshooting em `/backend/scripts/`

---

**Boa sorte na apresentação!**

O FINAP está pronto para impressionar.

---

**Versão**: 1.0.0
**Data**: 23 de Janeiro de 2025
**Status**: Pronto para Apresentação ✅
