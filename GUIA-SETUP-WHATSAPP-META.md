# 🤖 Guia Completo - Setup WhatsApp com Meta API

## 📋 Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Teste Rápido - Enviar Mensagem](#teste-rápido---enviar-mensagem)
4. [Rodar o Backend (Servidor API)](#rodar-o-backend-servidor-api)
5. [Configurar Webhook (Para Receber Mensagens)](#configurar-webhook-para-receber-mensagens)
6. [Comandos Disponíveis no WhatsApp](#comandos-disponíveis-no-whatsapp)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Pré-requisitos

- **Python 3.9+** instalado
- **Git** instalado
- Conta **Meta Developers** configurada
- **WhatsApp Business API** configurado no Meta Developers

### ✅ Credenciais Já Configuradas

As seguintes credenciais já estão no arquivo `backend/.env`:

```
META_WHATSAPP_TOKEN=EAALmf481QMUBQFxzsue91AXVSZBgYS6O1W9Ost9RITDtC3khABMC9Sb6ATb5C8qe1eZCRxTNVp4Dm0ltJz4hMtanw3YbICfZAk3jVHZB69iUMvqvrzI6YZCWfoDZCvxPlm6dfUtk45k9GGQ8WZBM0psZAox2D7M9UIltqNJz0xCILJFULT1ZAFqyeMadvmMiqzZAIur5qcPLowbEhdCA2OV4zFZBBACSZAJjNolYuN26M8hh0r8SysRsRAGMmkQYsAxa9xnSCq3udq9ROeMNeOUB290PmAIX
META_WHATSAPP_PHONE_ID=964874743366135
META_WHATSAPP_API_VERSION=v22.0
META_WHATSAPP_FROM_NUMBER=+15551534852
```

**Número de destino (seu WhatsApp):** `+5511995989872`

---

## ⚙️ Configuração do Ambiente

### 1. Navegar para a pasta do backend

```bash
cd backend
```

### 2. Criar ambiente virtual Python (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 🚀 Teste Rápido - Enviar Mensagem

Antes de rodar o backend completo, teste se a integração com WhatsApp está funcionando:

### Execute o script de teste:

```bash
python scripts/test_whatsapp_meta.py
```

### O que o script faz:
- ✅ Envia uma mensagem de teste para o seu WhatsApp (+5511995989872)
- ✅ Mostra o status da requisição
- ✅ Confirma se as credenciais estão corretas

### Resultado esperado:

```
============================================================
🤖 TESTE DE INTEGRAÇÃO WHATSAPP - META API
============================================================

📱 De: +15551534852
📱 Para: +5511995989872
📞 Phone ID: 964874743366135
🔑 Token: EAALmf481QMUBQFxzsue91AXVS...

📤 Enviando mensagem de teste...

📊 Status: 200
📄 Resposta:
{
  "messaging_product": "whatsapp",
  "contacts": [...],
  "messages": [...]
}

✅ Mensagem enviada com sucesso!
✅ Verifique seu WhatsApp no número: +5511995989872
```

**Se você recebeu a mensagem no WhatsApp, está tudo certo! ✅**

---

## 🖥️ Rodar o Backend (Servidor API)

### 1. Certifique-se de que está na pasta `backend`

```bash
cd backend
```

### 2. Iniciar o servidor FastAPI

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### O servidor vai iniciar em:

```
http://localhost:8000
```

### Endpoints disponíveis:

- **Documentação API:** http://localhost:8000/docs
- **Webhook WhatsApp:** http://localhost:8000/api/v1/whatsapp/webhook
- **Teste WhatsApp:** http://localhost:8000/api/v1/whatsapp/test

---

## 🌐 Configurar Webhook (Para Receber Mensagens)

Para que o bot **RECEBA** mensagens dos usuários e responda automaticamente, você precisa expor o backend para a internet e configurar o webhook na Meta.

### Opção 1: Usar ngrok (Recomendado para desenvolvimento)

#### 1. Instalar ngrok

Baixe em: https://ngrok.com/download

#### 2. Rodar ngrok

Em um **novo terminal** (deixe o backend rodando no outro):

```bash
ngrok http 8000
```

#### 3. Copiar a URL pública

O ngrok vai mostrar algo como:

```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

Copie a URL `https://abc123.ngrok.io`

#### 4. Configurar webhook na Meta

1. Acesse: https://developers.facebook.com/apps
2. Selecione seu app
3. Vá em **WhatsApp** > **Configuration**
4. Clique em **Edit** no campo "Webhook"
5. Cole a URL do webhook:

```
https://abc123.ngrok.io/api/v1/whatsapp/webhook
```

6. Cole o **Verify Token** (deve ser exatamente este):

```
finap_webhook_verify_token_2025
```

7. Clique em **Verify and Save**

#### 5. Subscrever aos eventos

Ainda na página de configuração do webhook, marque:
- ✅ **messages** (mensagens recebidas)

Clique em **Subscribe**.

**Pronto! Agora o bot pode receber e responder mensagens! 🎉**

---

## 💬 Comandos Disponíveis no WhatsApp

Depois de configurar tudo, envie mensagens para o número do bot no WhatsApp:

### 📝 Registrar Gasto

```
Gastei 50 no mercado
Gastei 30 no almoço
Paguei 100 na farmácia
```

**Resposta do bot:**
```
✅ Registrado!
💸 Débito: R$ 50.00
📁 Categoria: alimentação
💰 Saldo atual: R$ XXX.XX
```

### 💰 Registrar Receita

```
Recebi 1000 de salário
Recebi 500 de freelance
```

**Resposta do bot:**
```
💰 Boa! Dinheiro entrando!
➕ Receita: R$ 1000.00
📝 salário
💵 Saldo atual: R$ XXX.XX
```

### 📊 Ver Saldo

```
saldo
extrato
resumo
```

**Resposta do bot:**
```
📊 Seu resumo financeiro:

💰 Saldo: R$ XXX.XX
📈 Receitas do mês: R$ XXX.XX
📉 Gastos do mês: R$ XXX.XX

*Top 3 Gastos:*
1. alimentação: R$ 150.00
2. transporte: R$ 80.00
3. lazer: R$ 50.00

Use "ajuda" para ver mais comandos! 😊
```

### ❓ Ajuda

```
ajuda
help
?
```

---

## 🔍 Troubleshooting

### Erro: "Phone Number ID not found"

**Solução:** Verifique se o `META_WHATSAPP_PHONE_ID` está correto no arquivo `.env`:

```
META_WHATSAPP_PHONE_ID=964874743366135
```

### Erro: "Invalid access token"

**Solução:** O token pode ter expirado. Gere um novo token no Meta Developers:

1. Acesse: https://developers.facebook.com/apps
2. Vá em **WhatsApp** > **Getting Started**
3. Copie o novo **Temporary Access Token**
4. Atualize no arquivo `backend/.env`:

```
META_WHATSAPP_TOKEN=novo_token_aqui
```

### Mensagem não chegou no teste

**Possíveis causas:**

1. **Token expirado** - Gere um novo token
2. **Phone Number ID incorreto** - Verifique na Meta
3. **Número de destino não registrado** - Adicione o número na lista de testes na Meta:
   - WhatsApp > Getting Started > Add phone number

### Webhook não verifica

**Checklist:**

- ✅ Backend está rodando (`uvicorn main:app`)
- ✅ ngrok está rodando e gerando URL pública
- ✅ URL do webhook está correta: `https://SEU-NGROK.ngrok.io/api/v1/whatsapp/webhook`
- ✅ Verify Token está correto: `finap_webhook_verify_token_2025`

### Bot não responde mensagens

**Checklist:**

1. ✅ Webhook está configurado e verificado
2. ✅ Eventos "messages" estão subscritos
3. ✅ Backend está rodando
4. ✅ ngrok está rodando
5. ✅ Usuário existe no Firebase com o número de telefone cadastrado

Para testar se o usuário existe:

```bash
python scripts/check_user.py
```

Para adicionar número de telefone ao usuário:

```bash
python scripts/update_user_phone.py
```

---

## 📱 Testar Tudo Funcionando

### 1. Backend rodando:
```bash
cd backend
uvicorn main:app --reload
```

### 2. ngrok rodando (em outro terminal):
```bash
ngrok http 8000
```

### 3. Webhook configurado na Meta

### 4. Envie uma mensagem para o bot:

```
ajuda
```

**Se o bot responder, está tudo funcionando! 🎉**

---

## 🎯 Próximos Passos

1. **Configurar Firebase** - Para persistir dados de usuários e transações
2. **Configurar Gemini AI** - Para respostas inteligentes do FIM
3. **Deploy em produção** - Usar Heroku, Railway, ou outro serviço cloud
4. **Token permanente** - Configurar token de longa duração na Meta

---

## 📞 Contatos da Integração

- **Número do Bot:** +1 555 153 4852
- **Seu Número:** +55 11 99598-9872
- **Phone Number ID:** 964874743366135
- **API Version:** v22.0

---

**Criado para o projeto FINAP - Educação Financeira Gamificada** 🚀
