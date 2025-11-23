# 📸 Guia de Screenshots para Entrega - FINAP

**Data:** 23 de Novembro de 2024
**Objetivo:** Capturar as melhores telas do MVP para incluir no documento de escopo

---

## 🎯 SCREENSHOTS OBRIGATÓRIOS

### 1. **Tela de Login/Registro** ⭐⭐⭐
**Arquivo:** `01_login_register.png`

**O que capturar:**
- Tela de login completa
- Ou tela de registro com validação de senha

**Por que é importante:**
- Mostra autenticação real funcionando
- Design moderno e profissional
- Validação em tempo real

**Como capturar:**
```bash
# Acesse
http://localhost:3000

# Limpe localStorage para ver tela de login
F12 → Application → Clear Storage
```

**Elementos que devem aparecer:**
- Logo FINAP
- Mascote FIM
- Formulário de email/senha
- Validação de senha (barra de força)
- Botão de ação

---

### 2. **Dashboard/Overview** ⭐⭐⭐⭐⭐
**Arquivo:** `02_dashboard_overview.png`

**O que capturar:**
- Tela principal com estatísticas
- Saldo e orçamento
- Missões diárias
- Gráfico de gastos

**Por que é importante:**
- Tela mais importante do app
- Mostra gamificação (XP, moedas, vidas)
- Dados reais do backend
- Design completo e funcional

**Como capturar:**
```bash
# Após login, estará na tela Overview
# Certifique-se de ter:
- Nome do usuário no topo
- Stats de gamificação visíveis
- Pelo menos 1 missão ativa
- Gráfico de pizza com categorias
```

**Elementos que devem aparecer:**
- Nome do usuário (do banco)
- XP, Nível, Moedas, Vidas
- Saldo e orçamento mensal
- Barra de progresso de gastos
- Cards de missões diárias
- Gráfico de pizza

---

### 3. **Chat com FIM (Assistente IA)** ⭐⭐⭐⭐⭐
**Arquivo:** `03_chat_fim_assistant.png`

**O que capturar:**
- Conversa ativa com o FIM
- Mensagens do usuário e respostas da IA
- Sugestões de perguntas (quick replies)

**Por que é importante:**
- Demonstra integração com Google Gemini
- Mostra personalidade brasileira do FIM
- Diferencial competitivo principal

**Como capturar:**
```bash
# Navegue para Assistant
# Envie mensagens como:
- "Oi FIM! Como você pode me ajudar?"
- "Gastei muito esse mês, o que fazer?"
- "O que é educação financeira?"
```

**Elementos que devem aparecer:**
- Interface de chat (bubbles)
- Avatar do FIM
- Mensagens do usuário (lado direito)
- Respostas do FIM (lado esquerdo)
- Sugestões de perguntas embaixo
- Timestamp das mensagens

**⚠️ IMPORTANTE:**
- Capture uma conversa real (não vazia)
- Pelo menos 3-4 trocas de mensagens
- Resposta do FIM deve estar completa

---

### 4. **Gestão de Transações (Extract)** ⭐⭐⭐⭐
**Arquivo:** `04_transactions_extract.png`

**O que capturar:**
- Lista de transações
- Formulário de criação/edição aberto
- Ou gráfico de categorias

**Por que é importante:**
- Funcionalidade core do app
- Mostra CRUD completo
- Categorização visual

**Como capturar:**
```bash
# Navegue para Extract
# Certifique-se de ter várias transações listadas
# Pode capturar:
- Opção A: Lista de transações + gráfico
- Opção B: Formulário de criar transação aberto
```

**Elementos que devem aparecer:**
- Lista de transações por data
- Valores em reais (R$)
- Categorias coloridas
- Gráfico de pizza (categorias)
- Botão de adicionar (+)

---

### 5. **Trilha de Aprendizado (Learn)** ⭐⭐⭐⭐
**Arquivo:** `05_learning_trails.png`

**O que capturar:**
- Tela de trilhas de conhecimento
- Visualização em zigue-zague
- Ou quiz ativo com sistema de vidas

**Por que é importante:**
- Mostra gamificação educacional
- Sistema de vidas único
- Design criativo

**Como capturar:**
```bash
# Navegue para Learn
# Opções:
- Capturar tela de trilhas (overview)
- Ou entrar em um módulo e capturar quiz
```

**Elementos que devem aparecer:**
- Trilhas de conhecimento (cards)
- Progresso visual
- Sistema de vidas (5 corações)
- Quiz com opções (se capturar quiz)
- Recompensas (XP + moedas)

---

### 6. **Perfil e Badges** ⭐⭐⭐
**Arquivo:** `06_profile_badges.png`

**O que capturar:**
- Tela de perfil com estatísticas
- Badges desbloqueados
- Avatar do usuário

**Por que é importante:**
- Mostra sistema de conquistas
- Personalização do perfil
- Gamificação completa

**Como capturar:**
```bash
# Navegue para Profile
# Role para baixo para ver badges
```

**Elementos que devem aparecer:**
- Avatar do usuário
- Nome e email
- Nível e XP
- Grid de badges
- Estatísticas (streak, transações, etc.)

---

## 🔧 SCREENSHOTS TÉCNICOS (BACKEND)

### 7. **Swagger UI - Documentação da API** ⭐⭐⭐⭐⭐
**Arquivo:** `07_swagger_api_docs.png`

**O que capturar:**
- Interface Swagger completa
- Lista de endpoints
- Um endpoint expandido mostrando schema

**Por que é importante:**
- Prova que o backend é real
- Mostra profissionalismo técnico
- 30+ endpoints documentados

**Como capturar:**
```bash
# Acesse
http://localhost:8000/docs

# Role para mostrar vários endpoints
# Expanda um endpoint (ex: POST /auth/register)
```

**Elementos que devem aparecer:**
- Logo FastAPI no topo
- Lista de grupos (Auth, Dashboard, Transactions, etc.)
- Pelo menos 10+ endpoints visíveis
- Um endpoint expandido com schema Pydantic
- Botão "Try it out"

---

### 8. **Firestore - Banco de Dados** ⭐⭐⭐
**Arquivo:** `08_firebase_firestore.png`

**O que capturar:**
- Console do Firebase
- Collections (users, transactions, etc.)
- Dados reais salvos

**Por que é importante:**
- Mostra persistência de dados
- Prova que não é mock
- Infraestrutura real

**Como capturar:**
```bash
# Acesse Firebase Console
https://console.firebase.google.com

# Projeto: finap-mvp
# Firestore Database → Data

# Capture a view mostrando:
- Collection "users" com documentos
- Ou "transactions" com dados
```

**Elementos que devem aparecer:**
- Collections visíveis (users, transactions)
- Documentos com IDs
- Campos de dados (name, email, gamification, etc.)
- Timestamps

---

### 9. **Código - Estrutura do Projeto** ⭐⭐
**Arquivo:** `09_code_structure.png`

**O que capturar:**
- VS Code aberto
- Estrutura de pastas do projeto
- Arquivo main.py ou App.tsx aberto

**Por que é importante:**
- Mostra organização do código
- Profissionalismo técnico
- Código limpo e estruturado

**Como capturar:**
```bash
# Abra VS Code
code /mnt/c/Bitbucket/finap-googleai

# Expanda pastas:
- backend/
- frontend/

# Abra arquivo main.py ou App.tsx
```

**Elementos que devem aparecer:**
- Estrutura de pastas organizada
- Code syntax highlighting
- Comentários (se houver)
- Imports e estrutura clara

---

## 📐 CONFIGURAÇÕES DE CAPTURA

### Resolução
- **Ideal:** 1920x1080 (Full HD)
- **Mínimo:** 1280x720 (HD)
- **Formato:** PNG (alta qualidade)

### Ferramentas

**Windows:**
```
Win + Shift + S (recorte)
Print Screen (tela inteira)
Ferramenta de Captura (nativa)
```

**Mac:**
```
Cmd + Shift + 4 (área selecionada)
Cmd + Shift + 3 (tela inteira)
```

**Linux:**
```
Print Screen (tela inteira)
Shift + Print Screen (área)
Flameshot (recomendado)
```

### Dicas de Qualidade

1. **Limpe a interface:**
   - Feche abas desnecessárias
   - Esconda bookmarks bar
   - Remova extensões visíveis
   - Limpe console do DevTools

2. **Use dados realistas:**
   - Nomes próprios (não "teste123")
   - Valores monetários reais (R$ 50,00 não R$ 1,00)
   - Descrições descritivas (não "test")
   - Datas recentes

3. **Timing:**
   - Capture quando interface estiver carregada
   - Sem spinners de loading
   - Sem mensagens de erro
   - Sem toasts (a menos que relevante)

4. **Foco:**
   - Centralize elemento principal
   - Evite espaços vazios excessivos
   - Crop se necessário
   - Alta resolução

---

## 📂 ORGANIZAÇÃO DOS ARQUIVOS

### Estrutura Sugerida
```
finap-googleai/
└── screenshots/
    ├── frontend/
    │   ├── 01_login_register.png
    │   ├── 02_dashboard_overview.png
    │   ├── 03_chat_fim_assistant.png
    │   ├── 04_transactions_extract.png
    │   ├── 05_learning_trails.png
    │   └── 06_profile_badges.png
    ├── backend/
    │   ├── 07_swagger_api_docs.png
    │   ├── 08_firebase_firestore.png
    │   └── 09_code_structure.png
    └── README.md (este arquivo)
```

### Criar pasta:
```bash
cd /mnt/c/Bitbucket/finap-googleai
mkdir -p screenshots/frontend
mkdir -p screenshots/backend
```

---

## ✅ CHECKLIST DE SCREENSHOTS

### Antes de Capturar
- [ ] Backend rodando (http://localhost:8000)
- [ ] Frontend rodando (http://localhost:3000)
- [ ] Usuário criado com dados reais
- [ ] Transações adicionadas (5-10)
- [ ] Chat FIM com histórico
- [ ] Badges desbloqueados
- [ ] Missões ativas

### Frontend (6 screenshots)
- [ ] 01 - Login/Register
- [ ] 02 - Dashboard/Overview ⭐
- [ ] 03 - Chat FIM ⭐
- [ ] 04 - Transactions/Extract
- [ ] 05 - Learning Trails
- [ ] 06 - Profile/Badges

### Backend (3 screenshots)
- [ ] 07 - Swagger UI ⭐
- [ ] 08 - Firebase Firestore
- [ ] 09 - Code Structure

### Qualidade
- [ ] Resolução mínima 1280x720
- [ ] Formato PNG
- [ ] Interface limpa (sem lixo visual)
- [ ] Dados realistas (não "test123")
- [ ] Sem erros ou loading visíveis
- [ ] Boa iluminação/contraste

### Organização
- [ ] Pasta `/screenshots/` criada
- [ ] Arquivos nomeados corretamente
- [ ] Subpastas (frontend/backend)
- [ ] README.md explicativo

---

## 🎨 EDIÇÃO PÓS-CAPTURA (OPCIONAL)

### Ferramentas Recomendadas
- **Simples:** Paint.NET (Windows), Preview (Mac)
- **Avançado:** GIMP (free), Photoshop
- **Anotações:** Greenshot, Snagit

### Edições Sugeridas

1. **Adicionar anotações (opcional):**
   - Setas apontando para features importantes
   - Círculos destacando elementos-chave
   - Texto explicativo (fonte clara)

2. **Crop/Redimensionar:**
   - Remover espaços vazios
   - Centralizar elemento principal
   - Manter aspect ratio 16:9

3. **Ajustes de cor:**
   - Aumentar contraste levemente
   - Garantir legibilidade de texto
   - Não exagerar (manter natural)

**⚠️ Não exagere:** Screenshots devem parecer naturais, não editados demais.

---

## 📋 COMO USAR NO DOCUMENTO

### No Markdown:
```markdown
![Dashboard Overview](./screenshots/frontend/02_dashboard_overview.png)
*Dashboard principal com estatísticas em tempo real e gamificação*
```

### No PDF (ao converter):
- Insira imagens em alta resolução
- Adicione legendas descritivas
- Mantenha proporção original
- Centralize imagens

---

## 🚀 PRÓXIMOS PASSOS

1. **Capturar screenshots** (30-40 min)
2. **Organizar em pastas** (5 min)
3. **Revisar qualidade** (10 min)
4. **Inserir no documento de escopo** (15 min)
5. **Converter para PDF** (10 min)

**Tempo total estimado:** ~1h30min

---

**Preparado por:** Claude (Sonnet 4.5)
**Data:** 23 de Novembro de 2024
**Versão:** 1.0
