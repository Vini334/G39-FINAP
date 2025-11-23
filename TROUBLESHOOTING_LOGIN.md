# 🔧 Troubleshooting - Problema de Login no FINAP

**Data**: 2025-11-22
**Status**: ❌ NÃO RESOLVIDO - Login retornando 401 Unauthorized
**Impacto**: Usuários não conseguem fazer login com credenciais válidas

---

## 📋 Resumo do Problema

O sistema de autenticação está apresentando falha no login. Apesar do registro de usuários funcionar corretamente, o endpoint de login retorna erro `401 Unauthorized` mesmo com credenciais válidas.

### Sintomas Observados:
- ✅ Registro de novos usuários funciona
- ✅ Firebase Admin SDK inicializado corretamente
- ✅ Firestore conectado e operacional
- ✅ Usuários são criados no Firebase Auth
- ✅ Dados são salvos no Firestore
- ❌ Login retorna `401 Unauthorized` com mensagem "Email ou senha inválidos"
- ❌ Erro aparece rapidamente no console e retorna para tela inicial

---

## 🔍 Causa Raiz Identificada

### Problema Principal: Identity Toolkit API Desabilitada

A autenticação do Firebase usa a **Identity Toolkit API** para verificar senhas via REST API. Esta API estava **DESABILITADA** no projeto Google Cloud.

**NOTA IMPORTANTE**: O projeto ID 725539841605 que aparece nos logs pode não corresponder diretamente ao seu projeto `finap-mvp`. O Firebase Web API Key pode estar apontando para um projeto diferente. Verifique qual conta/projeto está sendo usada.

**Erro retornado pelo Firebase:**
```json
{
  "error": {
    "code": 403,
    "message": "Identity Toolkit API has not been used in project 725539841605 before or it is disabled.",
    "status": "PERMISSION_DENIED",
    "details": [{
      "@type": "type.googleapis.com/google.rpc.ErrorInfo",
      "reason": "SERVICE_DISABLED",
      "domain": "googleapis.com",
      "metadata": {
        "service": "identitytoolkit.googleapis.com",
        "activationUrl": "https://console.developers.google.com/apis/api/identitytoolkit.googleapis.com/overview?project=725539841605"
      }
    }]
  }
}
```

---

## 🛠️ Soluções Possíveis

### Solução 1: Habilitar Identity Toolkit API (RECOMENDADO)

#### Passo a Passo:

1. **Acessar o Google Cloud Console:**
   - URL direta: https://console.developers.google.com/apis/api/identitytoolkit.googleapis.com/overview?project=725539841605
   - Ou vá para: Google Cloud Console > APIs & Services > Library > Identity Toolkit API

2. **Habilitar a API:**
   - Clique em "ENABLE" ou "ATIVAR"
   - Aguarde alguns minutos para a propagação (pode levar até 10 minutos)

3. **Verificar habilitação:**
   ```bash
   gcloud services list --enabled --project=finap-mvp | grep identitytoolkit
   ```

4. **Testar login após habilitação:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"teste@teste.com","password":"Senha123"}'
   ```

#### Permissões Necessárias:
- Você precisa ter papel de **Owner** ou **Editor** no projeto Google Cloud
- Ou ter a permissão `serviceusage.services.enable`

---

### Solução 2: Workaround Temporário (APENAS DESENVOLVIMENTO)

Foi implementado um workaround no código que permite login sem verificação de senha quando a API está desabilitada.

⚠️ **ATENÇÃO**: Este workaround é **INSEGURO** e deve ser usado APENAS em desenvolvimento!

**Código implementado em** `backend/services/auth_service.py:230-249`:

```python
try:
    password_valid = self._verify_password_with_firebase(email, password)
    if not password_valid:
        raise Exception("Email ou senha inválidos")
except Exception as e:
    error_msg = str(e)
    # Se a Identity Toolkit API está desabilitada, permite login sem verificação
    if "Identity Toolkit API" in error_msg or "SERVICE_DISABLED" in error_msg:
        print(f"⚠️  WARNING: Identity Toolkit API not enabled. Password verification skipped.")
        # LOGIN SEM VERIFICAÇÃO DE SENHA - NÃO USAR EM PRODUÇÃO!
    else:
        raise
```

**Status do workaround**: ❌ NÃO FUNCIONANDO CONFORME ESPERADO

---

## 🔬 Verificações Necessárias

### 1. Verificar Configuração do Firebase

#### a) Arquivo `.env` está correto?

**Localização**: `backend/.env`

Verificar se as seguintes variáveis estão configuradas:

```bash
cd /mnt/c/Bitbucket/finap-googleai/backend
cat .env | grep FIREBASE
```

**Valores esperados:**
```env
FIREBASE_PROJECT_ID=finap-mvp
FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...(chave em uma única linha)...-----END PRIVATE KEY-----\n
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-fbsvc@finap-mvp.iam.gserviceaccount.com
FIREBASE_WEB_API_KEY=AIzaSyBCtE2KZN8OHMFFrzzt16RAYjhxrq9We40
```

⚠️ **IMPORTANTE**:
- Não usar aspas duplas nas variáveis
- `FIREBASE_PRIVATE_KEY` deve estar em UMA ÚNICA LINHA
- Quebras de linha devem ser `\n` (escapadas)

#### b) Arquivo de credenciais JSON existe?

```bash
ls -la /mnt/c/Bitbucket/finap-googleai/credentials/firebase-service-account.json
```

Deve mostrar o arquivo com ~2-3KB de tamanho.

#### c) Firebase está inicializando corretamente?

Verificar logs do backend ao iniciar:
```bash
# Deve aparecer esta mensagem:
✅ Firebase initialized successfully from credentials file
```

Se aparecer:
```
⚠️  Firebase credentials not configured. Using mock data.
```
Então há problema na configuração.

---

### 2. Verificar Identity Toolkit API

#### a) API está habilitada?

```bash
gcloud services list --enabled --project=finap-mvp | grep identitytoolkit
```

**Saída esperada se habilitada:**
```
identitytoolkit.googleapis.com   Identity Toolkit API
```

**Se não aparecer nada**: API está desabilitada (é esse o problema atual!)

#### b) Habilitar via gcloud (se tiver permissão):

```bash
gcloud services enable identitytoolkit.googleapis.com --project=finap-mvp
```

**Erro de permissão?**
```
ERROR: (gcloud.services.enable) PERMISSION_DENIED
```
Você não tem permissão. Solicite a um administrador ou habilite via Console Web.

---

### 3. Testar Endpoint de Login

#### a) Criar usuário de teste:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"usuario_teste@teste.com",
    "password":"SenhaForte123",
    "name":"Usuario Teste"
  }'
```

**Resposta esperada:** `201 Created` com dados do usuário e tokens

#### b) Tentar fazer login:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"usuario_teste@teste.com",
    "password":"SenhaForte123"
  }'
```

**Resposta esperada se funcionando:** `200 OK` com dados e tokens

**Resposta atual (com erro):**
```json
{
  "detail": "Email ou senha inválidos"
}
```

#### c) Verificar logs do backend:

Logs devem mostrar um dos seguintes:

**Se API habilitada e senha correta:**
```
INFO: POST /api/v1/auth/login HTTP/1.1" 200 OK
```

**Se API desabilitada (problema atual):**
```
DEBUG - Firebase Auth Response Status: 403
DEBUG - Firebase Auth Response: {...SERVICE_DISABLED...}
⚠️  WARNING: Identity Toolkit API not enabled. Password verification skipped.
INFO: POST /api/v1/auth/login HTTP/1.1" 401 Unauthorized
```

---

### 4. Verificar Usuários no Firebase

#### a) Listar usuários cadastrados:

```bash
cd /mnt/c/Bitbucket/finap-googleai/backend
python3 -c "
from firebase_admin import auth
from core.database import init_firebase

init_firebase()
users = auth.list_users()
for user in users.iterate_all():
    print(f'Email: {user.email}, UID: {user.uid}')
"
```

Deve listar os usuários, incluindo os que foram registrados.

#### b) Verificar se usuário específico existe:

```bash
python3 -c "
from firebase_admin import auth
from core.database import init_firebase

init_firebase()
try:
    user = auth.get_user_by_email('teste@teste.com')
    print(f'Usuário encontrado: {user.email} (UID: {user.uid})')
except:
    print('Usuário NÃO encontrado')
"
```

---

## 🐛 Debug Avançado

### 1. Adicionar logs detalhados ao auth_service.py

Editar `backend/services/auth_service.py` na função `login()`:

```python
async def login(self, email: str, password: str) -> Dict[str, Any]:
    db = self._get_db()

    print(f"🔍 DEBUG - Tentando login para: {email}")  # ADICIONAR

    try:
        # 1. Get user by email from Firebase Auth
        try:
            firebase_user = firebase_auth.get_user_by_email(email)
            user_id = firebase_user.uid
            print(f"✅ DEBUG - Usuário encontrado no Firebase Auth: {user_id}")  # ADICIONAR
        except firebase_auth.UserNotFoundError:
            print(f"❌ DEBUG - Usuário NÃO encontrado no Firebase Auth")  # ADICIONAR
            raise Exception("Email ou senha inválidos")

        # 2. Get user data from Firestore
        user_doc = db.collection('users').document(user_id).get()

        if not user_doc.exists:
            print(f"❌ DEBUG - Usuário NÃO encontrado no Firestore")  # ADICIONAR
            raise Exception("Usuário não encontrado no banco de dados")

        print(f"✅ DEBUG - Usuário encontrado no Firestore")  # ADICIONAR
        user_data = user_doc.to_dict()

        # 3. Verify password
        print(f"🔐 DEBUG - Tentando verificar senha via Firebase REST API")  # ADICIONAR
        try:
            password_valid = self._verify_password_with_firebase(email, password)
            if not password_valid:
                print(f"❌ DEBUG - Senha inválida")  # ADICIONAR
                raise Exception("Email ou senha inválidos")
            print(f"✅ DEBUG - Senha válida")  # ADICIONAR
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️  DEBUG - Erro na verificação de senha: {error_msg[:200]}")  # ADICIONAR

            if "Identity Toolkit API" in error_msg or "SERVICE_DISABLED" in error_msg:
                print(f"⚠️  WARNING: Identity Toolkit API not enabled. Password verification skipped.")
            else:
                raise

        # Continue with login...
```

### 2. Verificar resposta da API REST do Firebase

Editar `backend/services/auth_service.py` na função `_verify_password_with_firebase()`:

```python
def _verify_password_with_firebase(self, email: str, password: str) -> bool:
    try:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        print(f"🌐 DEBUG - Fazendo requisição para Firebase Auth REST API")  # ADICIONAR
        print(f"🌐 DEBUG - URL: {self.FIREBASE_AUTH_URL}?key={settings.FIREBASE_WEB_API_KEY[:20]}...")  # ADICIONAR

        response = requests.post(
            f"{self.FIREBASE_AUTH_URL}?key={settings.FIREBASE_WEB_API_KEY}",
            json=payload,
            timeout=30
        )

        print(f"📡 DEBUG - Status Code: {response.status_code}")  # ADICIONAR
        print(f"📡 DEBUG - Response: {response.text[:500]}")  # ADICIONAR

        if response.status_code == 200:
            return True
        # ...resto do código
```

---

## 📊 Status dos Componentes

| Componente | Status | Observação |
|------------|--------|------------|
| Firebase Admin SDK | ✅ OK | Inicializando corretamente |
| Firestore | ✅ OK | Conectado e funcional |
| Firebase Auth (Admin) | ✅ OK | Criando usuários com sucesso |
| Identity Toolkit API | ❌ DESABILITADA | **Este é o problema!** |
| Registro de usuários | ✅ OK | Funcionando perfeitamente |
| Login | ❌ FALHA | Retorna 401 Unauthorized |
| Workaround | ❌ NÃO FUNCIONA | Não está capturando exceção corretamente |

---

## 🎯 Próximos Passos Recomendados

### Imediato:
1. ✅ **Habilitar Identity Toolkit API no Google Cloud Console**
   - Esta é a solução definitiva e mais segura
   - URL: https://console.developers.google.com/apis/api/identitytoolkit.googleapis.com/overview?project=725539841605

2. ⏱️ **Aguardar propagação (5-10 minutos)**

3. 🧪 **Testar login novamente**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"teste@teste.com","password":"Senha123"}'
   ```

### Alternativo (se não conseguir habilitar API):
1. Investigar por que o workaround não está funcionando
2. Considerar implementar verificação de senha local (menos seguro)
3. Ou usar apenas o Firebase Admin SDK sem REST API (limitações)

---

## 📝 Arquivos Modificados Durante Debug

1. `/mnt/c/Bitbucket/finap-googleai/backend/.env`
   - Corrigido formato da `FIREBASE_PRIVATE_KEY`
   - Removidas aspas desnecessárias

2. `/mnt/c/Bitbucket/finap-googleai/backend/core/database.py:34-36`
   - Corrigido caminho para arquivo de credenciais

3. `/mnt/c/Bitbucket/finap-googleai/backend/services/auth_service.py:230-249`
   - Adicionado workaround para Identity Toolkit API desabilitada
   - **Status**: Não funcionando como esperado

---

## 🔗 Links Úteis

- **Habilitar Identity Toolkit API**: https://console.developers.google.com/apis/api/identitytoolkit.googleapis.com/overview?project=725539841605
- **Firebase Console**: https://console.firebase.google.com/project/finap-mvp
- **Firebase Auth Docs**: https://firebase.google.com/docs/auth
- **Identity Toolkit API Docs**: https://cloud.google.com/identity-platform/docs/reference/rest

---

## ✍️ Notas Adicionais

- O login estava funcionando anteriormente (conforme relatado)
- Algo mudou na configuração ou nas permissões do projeto
- A Identity Toolkit API pode ter sido desabilitada automaticamente ou nunca foi habilitada
- O registro funciona porque usa apenas o Firebase Admin SDK, que não depende da REST API

---

---

## 📊 Status Atual (Última Atualização: 2025-11-22 19:17 BRT)

### ✅ Ações Realizadas:
1. Identity Toolkit API foi **HABILITADA** pelo usuário
2. Registro de usuários continua funcionando perfeitamente
3. Teste com novo usuário criado: `novousuario@teste.com` / `SenhaForte123`

### ❌ Problema Persiste:
- Login ainda retorna `401 Unauthorized` mesmo após habilitar a API
- Pode ser:
  - **Propagação da API** (leva 5-10 minutos, às vezes mais)
  - **Projeto ID incorreto** (725539841605 vs finap-mvp)
  - **Firebase Web API Key** apontando para projeto errado

### 🔧 Próximas Ações Recomendadas:

1. **Aguardar mais 10-15 minutos** e testar novamente:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"novousuario@teste.com","password":"SenhaForte123"}'
   ```

2. **Verificar se Web API Key está correta**:
   - Acessar Firebase Console: https://console.firebase.google.com/project/finap-mvp/settings/general
   - Copiar a "Chave da API da Web"
   - Atualizar no `.env`: `FIREBASE_WEB_API_KEY=...`

3. **Verificar qual projeto a API Key pertence**:
   - O projeto ID 725539841605 pode ser diferente de finap-mvp
   - Confirmar que a Identity Toolkit API está habilitada NO PROJETO CORRETO

---

**Última atualização**: 2025-11-22 19:17 BRT
**Responsável**: Claude Code
**Prioridade**: 🔴 ALTA - Bloqueador para login de usuários
**Status**: AGUARDANDO PROPAGAÇÃO DA API + VERIFICAÇÃO DE PROJETO ID
