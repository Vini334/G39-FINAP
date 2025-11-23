# 🧪 GUIA DE TESTE COMPLETO - FINAP

## ✅ SERVIDORES NECESSÁRIOS

Certifique-se de que ambos os servidores estão rodando:

1. **Backend** (porta 8000):
   ```bash
   cd /mnt/c/Bitbucket/finap-googleai/backend
   python3 -m uvicorn main:app --reload --port 8000
   ```
   - Teste: `curl http://localhost:8000/health`
   - Resposta esperada: `{"status":"healthy","version":"1.0.0","environment":"development"}`

2. **Frontend** (porta 3000):
   ```bash
   cd /mnt/c/Bitbucket/finap-googleai/frontend
   npm run dev
   ```
   - URL: http://localhost:3000

---

## 📋 PASSO 1: LIMPAR DADOS DO NAVEGADOR

1. Abra http://localhost:3000
2. Pressione **F12** para abrir DevTools
3. Vá em **Application** → **Local Storage** → **http://localhost:3000**
4. Clique com botão direito e selecione **Clear**
5. Recarregue a página (**F5** ou **Ctrl+R**)

---

## 🔐 PASSO 2: TESTAR VALIDAÇÃO DE SENHA (IMPORTANTE!)

### ❌ Teste 1: Senha SEM letra maiúscula
1. Na tela de Onboarding, clique em **"Cadastre-se"**
2. Preencha:
   - **Email**: teste1@finap.com.br
   - **Senha**: senha123 (sem maiúscula)
   - **Nome**: João Silva
   - **Telefone**: (11) 98765-4321

3. **RESULTADO ESPERADO:**
   - ❌ Barra de força da senha VERMELHA (1/3)
   - ❌ Indicador "Uma letra maiúscula" em cinza/opaco
   - ❌ Ao clicar "Próximo", deve mostrar erro: **"Senha deve conter pelo menos uma letra maiúscula"**

---

### ❌ Teste 2: Senha SEM número
1. Limpe os campos e preencha:
   - **Email**: teste2@finap.com.br
   - **Senha**: SenhaForte (sem número)
   - **Nome**: Maria Santos

2. **RESULTADO ESPERADO:**
   - ❌ Barra de força da senha AMARELA (2/3)
   - ❌ Indicador "Um número" em cinza/opaco
   - ❌ Ao clicar "Próximo", deve mostrar erro: **"Senha deve conter pelo menos um número"**

---

### ❌ Teste 3: Senha com menos de 6 caracteres
1. Limpe os campos e preencha:
   - **Email**: teste3@finap.com.br
   - **Senha**: Ab1 (muito curta)
   - **Nome**: Pedro Costa

2. **RESULTADO ESPERADO:**
   - ❌ Barra de força da senha VERMELHA (1/3)
   - ❌ Indicador "Mínimo 6 caracteres" em cinza/opaco
   - ❌ Ao clicar "Próximo", deve mostrar erro: **"Senha deve ter no mínimo 6 caracteres"**

---

### ✅ Teste 4: Senha VÁLIDA (todas as regras atendidas)
1. Limpe os campos e preencha:
   - **Email**: teste@finap.com.br
   - **Senha**: Teste@123
   - **Nome**: Carlos Oliveira
   - **Telefone**: (11) 98765-4321
   - **Data de Nascimento**: 15/05/2005
   - **Gênero**: Masculino

2. **RESULTADO ESPERADO:**
   - ✅ Barra de força da senha VERDE (3/3)
   - ✅ TODOS os 3 indicadores em VERDE com check:
     - ✅ Mínimo 6 caracteres
     - ✅ Uma letra maiúscula
     - ✅ Um número
   - ✅ Ao clicar "Próximo", deve permitir avançar para os próximos passos

3. Complete o cadastro:
   - Preencha os dados adicionais
   - Clique em "Próximo" até o final
   - Você deve ser redirecionado para a **tela Overview**

---

## 🏠 PASSO 3: VERIFICAR INTEGRAÇÃO COM BACKEND - OVERVIEW

Na tela Overview, você deve ver:

### ✅ Dados Personalizados:
- **Nome**: "E aí, Carlos!" (primeiro nome do usuário)
- **Estatísticas**:
  - Vidas: 5 ❤️
  - Sequência: 0 🔥
  - Moedas: 100 🪙
  - Nível: 1

### ✅ Saldo e Orçamento:
- **Saldo Restante**: R$ 3.424,50
- **Gasto**: R$ 75,50
- **Limite**: R$ 3.000,00
- **Barra de progresso** visual verde

### ✅ Missões Diárias:
- Lista de missões com recompensas em moedas

---

## 👤 PASSO 4: VERIFICAR INTEGRAÇÃO - PROFILE

1. Clique no **avatar do usuário** no canto superior direito da Overview
2. Você deve ir para a tela **Profile**

### ✅ Dados Exibidos:
- **Nome completo**: Carlos Oliveira
- **Email**: teste@finap.com.br
- **Estatísticas** (Nível, Moedas, XP)
- **Avatar** personalizado

### ✅ Testar Logout:
1. Clique no ícone de **Configurações** (⚙️ engrenagem)
2. No menu lateral que abrir, role até o final
3. Clique no botão vermelho **"Sair"**
4. **RESULTADO ESPERADO:**
   - ✅ Toast verde de confirmação: "Logout realizado com sucesso!"
   - ✅ Redirecionamento para tela de **Onboarding**
   - ✅ Dados de autenticação limpos do localStorage

---

## 🔄 PASSO 5: TESTAR LOGIN (com validação de senha errada)

### ❌ Teste 1: Login com senha ERRADA
1. Na tela de Onboarding, clique em **"Já tenho conta"**
2. Preencha:
   - **Email**: teste@finap.com.br
   - **Senha**: SenhaErrada123

3. **RESULTADO ESPERADO:**
   - ❌ Erro: **"Credenciais inválidas"** ou **"Senha incorreta"**
   - ❌ NÃO deve permitir login

---

### ❌ Teste 2: Login com email não cadastrado
1. Preencha:
   - **Email**: naoexiste@finap.com.br
   - **Senha**: Teste@123

2. **RESULTADO ESPERADO:**
   - ❌ Erro: **"Usuário não encontrado"** ou **"Credenciais inválidas"**

---

### ✅ Teste 3: Login com credenciais CORRETAS
1. Preencha:
   - **Email**: teste@finap.com.br
   - **Senha**: Teste@123 (a senha correta que você cadastrou)

2. **RESULTADO ESPERADO:**
   - ✅ Login bem-sucedido
   - ✅ Redirecionamento para **Overview**
   - ✅ Nome personalizado: "E aí, Carlos!"

---

## 🎯 PASSO 6: TESTAR EMAIL JÁ CADASTRADO

1. Faça **logout** (se estiver logado)
2. Tente criar uma nova conta com o mesmo email:
   - **Email**: teste@finap.com.br (já existe!)
   - **Senha**: OutraSenha123
   - **Nome**: Outro Nome

3. **RESULTADO ESPERADO:**
   - ❌ Erro: **"Este email já está cadastrado. Tente fazer login."**
   - ❌ NÃO deve permitir criar conta duplicada

---

## ✅ CHECKLIST COMPLETO DE FUNCIONALIDADES

### Validação de Senha:
- [ ] Senha sem maiúscula é rejeitada (frontend e backend)
- [ ] Senha sem número é rejeitada (frontend e backend)
- [ ] Senha com menos de 6 caracteres é rejeitada
- [ ] Barra de força visual funciona (vermelho/amarelo/verde)
- [ ] Indicadores de requisitos funcionam (check verde quando OK)
- [ ] Senha válida permite cadastro

### Autenticação:
- [ ] Cadastro com senha válida funciona
- [ ] Email duplicado é bloqueado
- [ ] Login com senha errada é rejeitado
- [ ] Login com email não cadastrado é rejeitado
- [ ] Login com credenciais corretas funciona
- [ ] Logout funciona e limpa dados

### Integração Backend - Overview:
- [ ] Nome do usuário é exibido corretamente
- [ ] Estatísticas carregam do backend
- [ ] Saldo e orçamento exibidos corretamente
- [ ] Loading state aparece durante carregamento
- [ ] Erros são tratados com toasts

### Integração Backend - Profile:
- [ ] Nome completo é exibido
- [ ] Email é exibido
- [ ] Loading state funciona
- [ ] Botão de logout redireciona para Onboarding
- [ ] Toast de confirmação de logout aparece

---

## 🐛 COMO VERIFICAR ERROS

### No Console do Navegador (F12):
- **Network tab**: Veja as requisições HTTP
  - ✅ Status 200: Sucesso
  - ❌ Status 400: Erro de validação (senha fraca, email duplicado)
  - ❌ Status 401: Credenciais inválidas
  - ❌ Status 500: Erro no servidor

### No Console:
- Não deve ter erros vermelhos após login bem-sucedido
- Pode ter avisos sobre Tailwind CDN (ignorar em desenvolvimento)

---

## 📊 DADOS DE TESTE SUGERIDOS

Para testar múltiplas contas:

| Email | Senha | Nome |
|-------|-------|------|
| teste1@finap.com.br | Teste@123 | João Silva |
| teste2@finap.com.br | Senha@456 | Maria Santos |
| teste3@finap.com.br | Forte@789 | Pedro Costa |

**IMPORTANTE:** Todas as senhas devem ter:
- ✅ Mínimo 6 caracteres
- ✅ Pelo menos 1 letra MAIÚSCULA
- ✅ Pelo menos 1 número

---

## 🎬 FLUXO COMPLETO DE TESTE (5 minutos)

1. ✅ **Limpar localStorage** (F12 → Application → Clear)
2. ❌ **Testar senha fraca** (sem maiúscula: "teste123") → deve bloquear
3. ❌ **Testar senha fraca** (sem número: "TesteSenha") → deve bloquear
4. ✅ **Cadastrar com senha válida** (Teste@123)
5. ✅ **Verificar Overview** com nome personalizado
6. ✅ **Ir para Profile** e verificar dados
7. ✅ **Fazer logout**
8. ❌ **Tentar login com senha errada** → deve bloquear
9. ✅ **Login com senha correta** → deve funcionar
10. ❌ **Tentar cadastrar email duplicado** → deve bloquear

---

## 🚀 PRONTO!

Se todos os testes acima passaram, sua aplicação está 100% funcional com:
- ✅ Validação de senha forte (frontend + backend)
- ✅ Autenticação completa (login + registro + logout)
- ✅ Integração com Firebase/Firestore
- ✅ Proteção contra emails duplicados
- ✅ Proteção contra senhas fracas
- ✅ Feedback visual em tempo real
- ✅ Mensagens de erro adequadas
