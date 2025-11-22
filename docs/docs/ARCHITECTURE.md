# 🏗️ Arquitetura do Sistema - FINAP

## 📊 Visão Geral da Arquitetura

O FINAP utiliza uma arquitetura de microserviços simplificada, com separação clara entre frontend mobile, backend API e serviços externos. A escolha tecnológica prioriza escalabilidade, manutenibilidade e custo-benefício.

```
┌─────────────────────────────────────────────────────────┐
│                    Mobile Apps (iOS/Android)             │
│                     React Native + Expo                  │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS/WSS
                       ▼
┌──────────────────────────────────────────────────────────┐
│                    API Gateway Layer                      │
│                  FastAPI + Uvicorn                        │
│              Rate Limiting | Auth | CORS                  │
└──────────────────────────────────────────────────────────┘
                       │
┌──────────────────────────────────────────────────────────┐
│                    Business Logic Layer                   │
├────────────┬────────────┬────────────┬──────────────────┤
│   Auth     │ Financial  │    AI      │   WhatsApp       │
│  Service   │  Service   │  Service   │   Service        │
├────────────┴────────────┴────────────┴──────────────────┤
│                 Shared Domain Models                      │
└──────────────────────────────────────────────────────────┘
                       │
┌──────────────────────────────────────────────────────────┐
│                    Data Access Layer                      │
├─────────────────┬────────────────┬──────────────────────┤
│   Firestore     │  Firebase Auth │    Redis Cache       │
│   (NoSQL)       │    (Users)     │   (Sessions)         │
└─────────────────┴────────────────┴──────────────────────┘
                       │
┌──────────────────────────────────────────────────────────┐
│                  External Services                        │
├──────────┬──────────┬──────────┬────────────────────────┤
│  Gemini  │  Twilio  │  Cloud   │   Monitoring          │
│   API    │   API    │   Run    │  (Sentry/GA)          │
└──────────┴──────────┴──────────┴────────────────────────┘
```

## 🔧 Componentes Principais

### 1. Frontend Mobile (React Native + Expo)

#### Estrutura de Pastas
```
frontend/
├── App.tsx                    # Entry point
├── app.json                   # Expo config
├── babel.config.js
├── tsconfig.json
├── package.json
├── src/
│   ├── screens/              # Telas do app
│   │   ├── Auth/
│   │   │   ├── LoginScreen.tsx
│   │   │   ├── RegisterScreen.tsx
│   │   │   └── ForgotPasswordScreen.tsx
│   │   ├── Dashboard/
│   │   │   ├── HomeScreen.tsx
│   │   │   └── components/
│   │   ├── Transactions/
│   │   ├── Gamification/
│   │   ├── FIM/
│   │   └── Profile/
│   ├── components/           # Componentes reutilizáveis
│   │   ├── common/
│   │   ├── forms/
│   │   └── charts/
│   ├── navigation/           # React Navigation
│   │   ├── AppNavigator.tsx
│   │   ├── AuthNavigator.tsx
│   │   └── TabNavigator.tsx
│   ├── services/             # Comunicação com API
│   │   ├── api.ts
│   │   ├── auth.service.ts
│   │   └── transaction.service.ts
│   ├── store/                # Redux Toolkit
│   │   ├── index.ts
│   │   ├── slices/
│   │   └── hooks.ts
│   ├── hooks/                # Custom hooks
│   ├── utils/                # Funções utilitárias
│   ├── constants/            # Constantes do app
│   ├── types/                # TypeScript types
│   └── assets/               # Imagens, fontes, etc
```

#### Configuração Base
```typescript
// src/services/api.ts
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'https://api.finap.com.br';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor para adicionar token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor para refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = await AsyncStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        
        const { access_token } = response.data;
        await AsyncStorage.setItem('access_token', access_token);
        
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Redirect to login
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

### 2. Backend API (Python/FastAPI)

#### Estrutura de Pastas
```
backend/
├── main.py                   # FastAPI app entry
├── requirements.txt
├── .env.example
├── Dockerfile
├── alembic.ini              # Database migrations
├── api/
│   ├── __init__.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── transactions.py
│   │   ├── gamification.py
│   │   ├── fim.py
│   │   └── whatsapp.py
│   ├── dependencies/        # Dependency injection
│   │   ├── auth.py
│   │   └── database.py
│   └── middlewares/         # Middlewares
│       ├── cors.py
│       ├── rate_limit.py
│       └── error_handler.py
├── core/
│   ├── config.py            # Settings
│   ├── security.py          # JWT, hashing
│   └── database.py          # Firebase config
├── services/
│   ├── auth_service.py
│   ├── transaction_service.py
│   ├── gamification_service.py
│   ├── ai_service.py
│   └── whatsapp_service.py
├── models/                  # Pydantic models
│   ├── user.py
│   ├── transaction.py
│   └── challenge.py
├── schemas/                 # Request/Response schemas
│   ├── auth.py
│   ├── transaction.py
│   └── common.py
├── utils/
│   ├── validators.py
│   ├── formatters.py
│   └── helpers.py
└── tests/
    ├── conftest.py
    ├── test_auth.py
    └── test_transactions.py
```

#### Configuração Base
```python
# core/config.py
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "FINAP API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "exp://"]
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Firebase
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    
    # External APIs
    GEMINI_API_KEY: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_WHATSAPP_NUMBER: str
    
    # Redis (optional)
    REDIS_URL: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from core.config import settings
from core.database import init_firebase
from api.routes import auth, transactions, gamification, fim, whatsapp
from api.middlewares.error_handler import ErrorHandlerMiddleware
from api.middlewares.rate_limit import RateLimitMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_firebase()
    if settings.SENTRY_DSN:
        sentry_sdk.init(dsn=settings.SENTRY_DSN)
    yield
    # Shutdown
    pass

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(RateLimitMiddleware)

if settings.SENTRY_DSN:
    app.add_middleware(SentryAsgiMiddleware)

# Routes
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])
app.include_router(transactions.router, prefix=f"{settings.API_V1_PREFIX}/transactions", tags=["transactions"])
app.include_router(gamification.router, prefix=f"{settings.API_V1_PREFIX}/gamification", tags=["gamification"])
app.include_router(fim.router, prefix=f"{settings.API_V1_PREFIX}/fim", tags=["fim"])
app.include_router(whatsapp.router, prefix=f"{settings.API_V1_PREFIX}/whatsapp", tags=["whatsapp"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
```

### 3. Database Schema (Firestore)

#### Estrutura de Coleções
```javascript
// Estrutura Firestore
firestore/
├── users/                    
│   └── {userId}/
│       ├── profile
│       ├── settings
│       └── gamification
├── transactions/
│   └── {transactionId}/
├── challenges/
│   └── {challengeId}/
├── squads/
│   └── {squadId}/
│       └── members/
│           └── {userId}/
├── learning_modules/
│   └── {moduleId}/
├── fim_conversations/
│   └── {userId}/
│       └── messages/
│           └── {messageId}/
└── system/
    ├── categories/
    ├── badges/
    └── config/
```

#### Modelos de Dados
```python
# models/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserProfile(BaseModel):
    age: Optional[int] = None
    monthly_income: Optional[float] = None
    financial_goals: List[str] = []
    avatar_url: Optional[str] = None

class UserGamification(BaseModel):
    level: int = 1
    xp: int = 0
    coins: int = 100
    lives: int = 5
    badges: List[str] = []
    current_streak: int = 0
    longest_streak: int = 0
    last_login: datetime

class User(BaseModel):
    uid: str
    email: EmailStr
    name: str
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    profile: UserProfile
    gamification: UserGamification
    is_active: bool = True
    is_premium: bool = False

# models/transaction.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionSource(str, Enum):
    APP = "app"
    WHATSAPP = "whatsapp"
    IMPORT = "import"

class Transaction(BaseModel):
    id: str
    user_id: str
    type: TransactionType
    amount: float
    category: str
    description: Optional[str] = None
    date: datetime
    source: TransactionSource
    tags: List[str] = []
    is_recurrent: bool = False
    recurrence_period: Optional[str] = None
    attachments: List[str] = []
    created_at: datetime
    updated_at: datetime
```

### 4. Serviços Externos

#### Gemini API (FIM Assistant)
```python
# services/ai_service.py
import google.generativeai as genai
from core.config import settings
from typing import List, Dict

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def get_fim_response(
        self, 
        user_message: str, 
        context: Dict,
        conversation_history: List[Dict]
    ) -> str:
        """
        Gera resposta do FIM baseada no contexto do usuário
        """
        system_prompt = """
        Você é o FIM, assistente financeiro virtual do FINAP.
        
        Personalidade:
        - Amigável e encorajador
        - Educativo mas não condescendente
        - Usa linguagem jovem mas profissional
        - Pode usar emojis com moderação
        
        Objetivos:
        - Ajudar o usuário a gerenciar suas finanças
        - Educar sobre conceitos financeiros
        - Motivar a atingir metas
        - Sugerir melhorias nos hábitos
        
        Contexto do usuário:
        {context}
        
        Regras:
        - Sempre seja positivo e motivador
        - Dê dicas práticas e acionáveis
        - Celebre conquistas do usuário
        - Nunca julgue decisões financeiras
        - Não dê conselhos de investimento específicos
        """
        
        prompt = system_prompt.format(context=context)
        
        # Adicionar histórico da conversa
        messages = [{"role": "system", "content": prompt}]
        for msg in conversation_history[-10:]:  # Últimas 10 mensagens
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        messages.append({"role": "user", "content": user_message})
        
        response = self.model.generate_content(
            " ".join([m["content"] for m in messages])
        )
        
        return response.text
    
    async def analyze_spending(self, transactions: List[Dict]) -> Dict:
        """
        Analisa padrões de gastos e gera insights
        """
        prompt = f"""
        Analise os seguintes gastos e forneça insights em JSON:
        {transactions}
        
        Retorne um JSON com:
        - summary: resumo geral
        - top_categories: top 3 categorias de gasto
        - alerts: alertas importantes
        - tips: 3 dicas práticas
        - emotional_analysis: análise de gastos impulsivos
        """
        
        response = self.model.generate_content(prompt)
        # Parse JSON response
        return response.text
```

#### Twilio WhatsApp Integration
```python
# services/whatsapp_service.py
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from core.config import settings
import re
from typing import Dict, Optional

class WhatsAppService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER
        
    async def send_message(self, to: str, body: str, media_url: Optional[str] = None):
        """
        Envia mensagem via WhatsApp
        """
        message = self.client.messages.create(
            from_=f'whatsapp:{self.whatsapp_number}',
            to=f'whatsapp:{to}',
            body=body,
            media_url=[media_url] if media_url else []
        )
        return message.sid
    
    async def process_incoming_message(self, from_number: str, body: str) -> Dict:
        """
        Processa mensagem recebida e extrai informações
        """
        # Normalizar texto
        text = body.lower().strip()
        
        # Patterns para extrair informações
        patterns = {
            'expense': r'gastei?\s+(?:r\$)?\s*(\d+(?:[.,]\d{2})?)\s+(?:no|na|em)?\s*(.+)',
            'income': r'recebi?\s+(?:r\$)?\s*(\d+(?:[.,]\d{2})?)\s+(?:de)?\s*(.+)',
            'balance': r'(?:saldo|extrato)',
            'help': r'(?:ajuda|help|\?)',
            'categories': r'categorias',
            'goal': r'meta\s+(?:r\$)?\s*(\d+(?:[.,]\d{2})?)'
        }
        
        for intent, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                if intent in ['expense', 'income']:
                    amount = float(match.group(1).replace(',', '.'))
                    description = match.group(2).strip()
                    return {
                        'intent': intent,
                        'amount': amount,
                        'description': description,
                        'category': self._infer_category(description)
                    }
                elif intent == 'goal':
                    amount = float(match.group(1).replace(',', '.'))
                    return {
                        'intent': intent,
                        'amount': amount
                    }
                else:
                    return {'intent': intent}
        
        return {'intent': 'unknown', 'text': body}
    
    def _infer_category(self, description: str) -> str:
        """
        Inferir categoria baseada na descrição
        """
        categories = {
            'alimentação': ['mercado', 'supermercado', 'almoço', 'jantar', 'lanche', 'comida', 'restaurante', 'ifood', 'delivery'],
            'transporte': ['uber', '99', 'taxi', 'ônibus', 'metrô', 'combustível', 'gasolina', 'álcool', 'estacionamento'],
            'moradia': ['aluguel', 'condomínio', 'luz', 'água', 'gás', 'internet', 'telefone'],
            'saúde': ['farmácia', 'remédio', 'médico', 'consulta', 'exame', 'hospital', 'plano'],
            'educação': ['curso', 'livro', 'faculdade', 'escola', 'material'],
            'lazer': ['cinema', 'netflix', 'spotify', 'jogo', 'bar', 'festa', 'show'],
            'compras': ['roupa', 'sapato', 'presente', 'shopping', 'loja'],
        }
        
        description_lower = description.lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category
        
        return 'outros'
    
    def format_response(self, response_type: str, data: Dict) -> str:
        """
        Formata resposta para enviar via WhatsApp
        """
        templates = {
            'transaction_created': """
✅ *Transação Registrada!*

💰 Valor: R$ {amount:.2f}
📁 Categoria: {category}
📝 Descrição: {description}

💳 Saldo atual: R$ {balance:.2f}

💡 *Dica do FIM:* {tip}
            """,
            
            'balance': """
📊 *Seu Resumo Financeiro*

💰 Saldo: R$ {balance:.2f}
📈 Receitas do mês: R$ {income:.2f}
📉 Despesas do mês: R$ {expenses:.2f}

*Top 3 Gastos:*
{top_expenses}

Use "ajuda" para ver mais comandos! 😊
            """,
            
            'help': """
🤖 *Comandos Disponíveis:*

💸 *Registrar gasto:*
"Gastei 50 no mercado"

💰 *Registrar receita:*
"Recebi 1000 de salário"

📊 *Ver saldo:*
"Saldo" ou "Extrato"

🎯 *Definir meta:*
"Meta 500"

📁 *Ver categorias:*
"Categorias"

❓ *Ajuda:*
"Ajuda" ou "?"

Estou sempre aqui para ajudar! 😊
            """,
            
            'error': """
❌ *Ops! Não entendi sua mensagem.*

Tente algo como:
• "Gastei 30 no almoço"
• "Saldo"
• "Ajuda"

Digite "ajuda" para ver todos os comandos! 🤔
            """
        }
        
        return templates.get(response_type, templates['error']).format(**data)
```

## 🔒 Segurança

### Autenticação e Autorização
```python
# core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

### Rate Limiting
```python
# api/middlewares/rate_limit.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = timedelta(seconds=period)
        self.clients = defaultdict(list)
        
    async def dispatch(self, request: Request, call_next):
        client_id = request.client.host
        now = datetime.now()
        
        # Limpar chamadas antigas
        self.clients[client_id] = [
            call_time for call_time in self.clients[client_id]
            if call_time > now - self.period
        ]
        
        # Verificar limite
        if len(self.clients[client_id]) >= self.calls:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
        
        # Adicionar chamada atual
        self.clients[client_id].append(now)
        
        response = await call_next(request)
        return response
```

## 🚀 Deploy e DevOps

### Docker Configuration
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ENV=development
    env_file:
      - ./backend/.env
    volumes:
      - ./backend:/app
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### GitHub Actions CI/CD
```yaml
# .github/workflows/deploy.yml
name: Deploy to Google Cloud Run

on:
  push:
    branches: [main]

env:
  PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  SERVICE_NAME: finap-api
  REGION: us-central1

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - id: 'auth'
      uses: 'google-github-actions/auth@v1'
      with:
        credentials_json: ${{ secrets.GCP_SA_KEY }}
    
    - name: Set up Cloud SDK
      uses: 'google-github-actions/setup-gcloud@v1'
    
    - name: Build and Push Docker image
      run: |
        gcloud builds submit \
          --tag gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA \
          ./backend
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy $SERVICE_NAME \
          --image gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA \
          --region $REGION \
          --platform managed \
          --allow-unauthenticated
```

## 📊 Monitoramento

### Logging Strategy
```python
# utils/logger.py
import logging
import sys
from core.config import settings

def setup_logger():
    logger = logging.getLogger("finap")
    
    # Set level based on environment
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
```

### Health Checks
```python
# api/routes/health.py
from fastapi import APIRouter, Depends
from core.database import get_firestore_client
import redis
from typing import Dict

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict:
    """
    Health check endpoint
    """
    health_status = {
        "status": "healthy",
        "services": {}
    }
    
    # Check Firestore
    try:
        db = get_firestore_client()
        # Simple read operation
        db.collection('system').document('health').get()
        health_status["services"]["firestore"] = "healthy"
    except Exception as e:
        health_status["services"]["firestore"] = "unhealthy"
        health_status["status"] = "degraded"
    
    # Check Redis (if configured)
    if settings.REDIS_URL:
        try:
            r = redis.from_url(settings.REDIS_URL)
            r.ping()
            health_status["services"]["redis"] = "healthy"
        except Exception as e:
            health_status["services"]["redis"] = "unhealthy"
            health_status["status"] = "degraded"
    
    return health_status

@router.get("/readiness")
async def readiness_check() -> Dict:
    """
    Readiness check for Kubernetes/Cloud Run
    """
    # Check if all required services are initialized
    return {"ready": True}
```

## 🔄 Padrões e Convenções

### Naming Conventions
- **Python**: snake_case para variáveis e funções, PascalCase para classes
- **TypeScript/React**: camelCase para variáveis e funções, PascalCase para componentes
- **API Endpoints**: kebab-case para URLs
- **Database**: snake_case para coleções e campos

### Git Workflow
```bash
# Branch naming
feature/TASK-123-description
bugfix/TASK-456-description
hotfix/TASK-789-description

# Commit messages
feat: Add WhatsApp integration
fix: Resolve login issue
docs: Update API documentation
test: Add unit tests for auth service
refactor: Optimize transaction queries
```

### Code Quality
```python
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
```

---

**Documento versão:** 1.0.0  
**Última atualização:** Novembro 2024  
**Mantenedor:** Equipe FINAP Tech
