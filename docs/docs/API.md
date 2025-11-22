# 📡 API Documentation - FINAP

## Base URL
```
Production: https://api.finap.com.br
Staging: https://staging-api.finap.com.br  
Development: http://localhost:8000
```

## Authentication
All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Response Format
All responses follow this structure:
```json
{
  "success": true,
  "data": {},
  "message": "Success message",
  "errors": []
}
```

Error responses:
```json
{
  "success": false,
  "data": null,
  "message": "Error description",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

---

## 🔐 Authentication Endpoints

### Register User
```http
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "João Silva",
  "phone": "+5511999999999"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "user": {
      "uid": "abc123",
      "email": "user@example.com",
      "name": "João Silva"
    },
    "tokens": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "token_type": "bearer",
      "expires_in": 900
    }
  }
}
```

### Login
```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "uid": "abc123",
      "email": "user@example.com",
      "name": "João Silva",
      "gamification": {
        "level": 5,
        "xp": 1250,
        "coins": 300
      }
    },
    "tokens": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "token_type": "bearer",
      "expires_in": 900
    }
  }
}
```

### Refresh Token
```http
POST /api/v1/auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGc...",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

### Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### Forgot Password
```http
POST /api/v1/auth/forgot-password
```

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset email sent"
}
```

---

## 👤 User Endpoints

### Get User Profile
```http
GET /api/v1/users/profile
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "uid": "abc123",
    "email": "user@example.com",
    "name": "João Silva",
    "phone": "+5511999999999",
    "created_at": "2024-01-01T00:00:00Z",
    "profile": {
      "age": 25,
      "monthly_income": 3000.00,
      "financial_goals": ["emergency_fund", "travel", "investment"],
      "avatar_url": "https://..."
    },
    "gamification": {
      "level": 5,
      "xp": 1250,
      "coins": 300,
      "lives": 4,
      "badges": ["first_transaction", "week_streak", "saver"],
      "current_streak": 7,
      "longest_streak": 15,
      "last_login": "2024-11-19T10:00:00Z"
    },
    "preferences": {
      "notifications": true,
      "dark_mode": false,
      "language": "pt-BR",
      "currency": "BRL"
    }
  }
}
```

### Update User Profile
```http
PUT /api/v1/users/profile
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "João Silva Santos",
  "profile": {
    "age": 26,
    "monthly_income": 3500.00,
    "financial_goals": ["emergency_fund", "car", "investment"]
  },
  "preferences": {
    "dark_mode": true,
    "notifications": false
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "message": "Profile updated successfully",
    "user": { /* updated user object */ }
  }
}
```

### Get User Statistics
```http
GET /api/v1/users/statistics
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `period`: `week` | `month` | `year` | `all` (default: `month`)
- `start_date`: ISO date string
- `end_date`: ISO date string

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "period": "month",
    "total_income": 3500.00,
    "total_expenses": 2800.00,
    "balance": 700.00,
    "savings_rate": 20.0,
    "top_categories": [
      {
        "category": "alimentação",
        "amount": 800.00,
        "percentage": 28.57,
        "transaction_count": 45
      },
      {
        "category": "transporte",
        "amount": 400.00,
        "percentage": 14.29,
        "transaction_count": 20
      }
    ],
    "daily_average": 93.33,
    "comparison_previous_period": {
      "expenses_change": -15.5,
      "income_change": 0,
      "savings_change": 25.0
    }
  }
}
```

---

## 💰 Transaction Endpoints

### List Transactions
```http
GET /api/v1/transactions
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: integer (default: 1)
- `limit`: integer (default: 20, max: 100)
- `type`: `income` | `expense` | `all` (default: `all`)
- `category`: string
- `start_date`: ISO date string
- `end_date`: ISO date string
- `search`: string (search in description)
- `sort`: `date_desc` | `date_asc` | `amount_desc` | `amount_asc` (default: `date_desc`)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "id": "trans123",
        "type": "expense",
        "amount": 45.50,
        "category": "alimentação",
        "description": "Almoço no restaurante",
        "date": "2024-11-19T12:30:00Z",
        "source": "app",
        "tags": ["restaurante", "almoço"],
        "is_recurrent": false,
        "created_at": "2024-11-19T12:35:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total_items": 150,
      "total_pages": 8,
      "has_next": true,
      "has_previous": false
    },
    "summary": {
      "total_income": 3500.00,
      "total_expenses": 2800.00,
      "balance": 700.00
    }
  }
}
```

### Create Transaction
```http
POST /api/v1/transactions
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "type": "expense",
  "amount": 45.50,
  "category": "alimentação",
  "description": "Almoço no restaurante",
  "date": "2024-11-19T12:30:00Z",
  "tags": ["restaurante", "almoço"],
  "is_recurrent": false
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "transaction": {
      "id": "trans123",
      "type": "expense",
      "amount": 45.50,
      "category": "alimentação",
      "description": "Almoço no restaurante",
      "date": "2024-11-19T12:30:00Z",
      "source": "app",
      "tags": ["restaurante", "almoço"],
      "is_recurrent": false,
      "created_at": "2024-11-19T12:35:00Z"
    },
    "gamification": {
      "xp_earned": 5,
      "new_total_xp": 1255,
      "badges_earned": [],
      "challenge_progress": [
        {
          "challenge_id": "daily_track",
          "progress": 3,
          "target": 5
        }
      ]
    }
  }
}
```

### Get Transaction
```http
GET /api/v1/transactions/{transaction_id}
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "transaction": { /* transaction object */ }
  }
}
```

### Update Transaction
```http
PUT /api/v1/transactions/{transaction_id}
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "amount": 50.00,
  "description": "Almoço executivo",
  "tags": ["restaurante", "almoço", "trabalho"]
}
```

### Delete Transaction
```http
DELETE /api/v1/transactions/{transaction_id}
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Transaction deleted successfully"
}
```

### Get Categories
```http
GET /api/v1/transactions/categories
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "categories": [
      {
        "id": "alimentacao",
        "name": "Alimentação",
        "icon": "🍔",
        "color": "#FF6B6B",
        "budget_suggestion": 600.00
      },
      {
        "id": "transporte",
        "name": "Transporte",
        "icon": "🚗",
        "color": "#4ECDC4",
        "budget_suggestion": 300.00
      }
    ]
  }
}
```

### Get Analytics
```http
GET /api/v1/transactions/analytics
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `period`: `week` | `month` | `quarter` | `year`
- `group_by`: `category` | `day` | `week` | `month`

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "period": "month",
    "analytics": {
      "by_category": [
        {
          "category": "alimentação",
          "total": 800.00,
          "percentage": 28.57,
          "count": 45,
          "average": 17.78,
          "trend": "increasing"
        }
      ],
      "by_time": [
        {
          "date": "2024-11-01",
          "income": 0,
          "expenses": 120.00
        },
        {
          "date": "2024-11-02",
          "income": 0,
          "expenses": 85.50
        }
      ],
      "insights": [
        {
          "type": "warning",
          "message": "Seus gastos com alimentação aumentaram 25% este mês"
        },
        {
          "type": "tip",
          "message": "Você poderia economizar R$ 200 reduzindo delivery"
        }
      ]
    }
  }
}
```

---

## 🎮 Gamification Endpoints

### Get Gamification Status
```http
GET /api/v1/gamification/status
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "level": 5,
    "xp": 1255,
    "xp_to_next_level": 245,
    "coins": 300,
    "lives": 4,
    "lives_recharge_at": "2024-11-19T15:30:00Z",
    "current_streak": 7,
    "longest_streak": 15,
    "total_badges": 12,
    "rank": 145,
    "percentile": 85.5
  }
}
```

### Get Leaderboard
```http
GET /api/v1/gamification/leaderboard
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `type`: `global` | `friends` | `squad` (default: `global`)
- `period`: `week` | `month` | `all` (default: `month`)
- `limit`: integer (default: 20, max: 100)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "leaderboard": [
      {
        "rank": 1,
        "user": {
          "uid": "user123",
          "name": "Maria Silva",
          "avatar_url": "https://..."
        },
        "xp": 5250,
        "level": 12,
        "badges_count": 25
      }
    ],
    "user_position": {
      "rank": 145,
      "xp": 1255,
      "level": 5
    }
  }
}
```

### Get Badges
```http
GET /api/v1/gamification/badges
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "earned_badges": [
      {
        "id": "first_transaction",
        "name": "Primeira Transação",
        "description": "Registrou sua primeira transação",
        "icon": "🎯",
        "rarity": "common",
        "earned_at": "2024-11-01T10:00:00Z",
        "xp_reward": 50
      }
    ],
    "available_badges": [
      {
        "id": "month_saver",
        "name": "Poupador do Mês",
        "description": "Economize 20% da renda por um mês",
        "icon": "💰",
        "rarity": "rare",
        "xp_reward": 200,
        "requirement": {
          "type": "savings_rate",
          "target": 20,
          "current": 15,
          "period": "month"
        }
      }
    ],
    "statistics": {
      "total_earned": 12,
      "total_available": 50,
      "completion_percentage": 24.0,
      "rarity_breakdown": {
        "common": 8,
        "uncommon": 3,
        "rare": 1,
        "epic": 0,
        "legendary": 0
      }
    }
  }
}
```

---

## 🤖 FIM Assistant Endpoints

### Chat with FIM
```http
POST /api/v1/fim/chat
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "message": "Como posso economizar no supermercado?",
  "context": {
    "include_transactions": true,
    "include_goals": true
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "response": "Ótima pergunta! 🛒 Baseado nos seus gastos, vejo que você gastou R$ 450 em mercado este mês. Aqui vão minhas dicas:\n\n1. **Faça uma lista** antes de ir ao mercado\n2. **Compare preços** entre marcas\n3. **Evite ir com fome** para não comprar por impulso\n4. **Use cupons** e apps de desconto\n\nVi que você vai ao mercado 3x por semana. Que tal tentar compras semanais? Isso pode reduzir compras por impulso! 💡",
    "suggestions": [
      "Como fazer uma lista de compras eficiente?",
      "Quais apps de desconto você recomenda?",
      "Como planejar refeições da semana?"
    ],
    "actions": [
      {
        "type": "create_goal",
        "label": "Criar meta de economia",
        "data": {
          "category": "alimentação",
          "target_reduction": 20
        }
      }
    ]
  }
}
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Invalid request data",
  "errors": [
    {
      "field": "amount",
      "message": "Amount must be greater than 0"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Invalid or expired token",
  "errors": []
}
```

### 403 Forbidden
```json
{
  "success": false,
  "message": "You don't have permission to access this resource",
  "errors": []
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Resource not found",
  "errors": []
}
```

### 429 Too Many Requests
```json
{
  "success": false,
  "message": "Rate limit exceeded",
  "errors": [],
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "An unexpected error occurred",
  "errors": [],
  "request_id": "req_abc123"
}
```

---

## 📝 Notes

- All dates are in ISO 8601 format
- All monetary values are in BRL (Brazilian Real)
- Pagination starts at page 1
- Rate limits: 100 requests per minute per user
- API versioning through URL path (/api/v1/)

---

**API Version:** 1.0.0  
**Last Updated:** November 2024  
**Contact:** api@finap.com.br
