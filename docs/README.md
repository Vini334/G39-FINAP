# 📱 FINAP - Aplicativo de Educação Financeira Gamificado

<p align="center">
  <img src="docs/assets/logo.png" alt="FINAP Logo" width="200">
</p>

<p align="center">
  <strong>Transformando a educação financeira em uma jornada divertida e engajante para jovens</strong>
</p>

<p align="center">
  <a href="#sobre">Sobre</a> •
  <a href="#funcionalidades">Funcionalidades</a> •
  <a href="#tecnologias">Tecnologias</a> •
  <a href="#instalação">Instalação</a> •
  <a href="#estrutura">Estrutura</a> •
  <a href="#documentação">Documentação</a> •
  <a href="#contribuindo">Contribuindo</a>
</p>

---

## 🎯 Sobre

O **FINAP** é um aplicativo revolucionário que combina educação financeira com gamificação, tornando o aprendizado sobre finanças pessoais uma experiência divertida e engajante para jovens. Com o auxílio do assistente virtual **FIM**, powered by IA, os usuários aprendem a gerenciar suas finanças enquanto completam desafios, ganham XP e desbloqueiam conquistas.

### 🌟 Diferenciais

- 🤖 **Assistente FIM**: IA personalizada para orientação financeira
- 📱 **Integração WhatsApp**: Registre gastos via mensagem
- 🎮 **Gamificação Completa**: XP, badges, níveis e desafios
- 👥 **FNAP Squad**: Metas financeiras colaborativas com amigos
- 📊 **Análises Inteligentes**: Relatórios mensais detalhados
- 📚 **Trilhas de Conhecimento**: Aprenda conceitos financeiros

## 🚀 Funcionalidades

### Core Features

#### 1. **Dashboard Financeiro**
- Visão geral do status financeiro
- Alertas visuais inteligentes
- Progresso de metas em tempo real
- Missões diárias personalizadas

#### 2. **Gestão de Gastos**
- Categorização automática de despesas
- Gráficos e análises detalhadas
- Filtros temporais (mensal, semestral, anual)
- Integração WhatsApp para registro rápido

#### 3. **Educação Gamificada**
- Trilhas de conhecimento interativas
- Quizzes com recompensas
- Sistema de vidas e moedas
- Certificados digitais

#### 4. **Social & Desafios**
- Desafios semanais/mensais
- Grupos colaborativos (FNAP Squad)
- Divisão de gastos entre amigos
- Rankings e competições

#### 5. **Assistente Virtual FIM**
- Chat interativo com IA
- Dicas personalizadas
- Análises comportamentais
- Suporte 24/7

#### 6. **Relatórios Inteligentes**
- Análise mensal automática
- Mapa emocional de gastos
- Previsões e sugestões
- Exportação de dados

## 🛠 Tecnologias

### Backend
- **Python 3.11** - Linguagem principal
- **FastAPI** - Framework web assíncrono
- **Firebase Firestore** - Banco de dados NoSQL
- **Firebase Auth** - Autenticação
- **Twilio API** - Integração WhatsApp
- **Gemini API** - IA para o assistente FIM
- **Google Cloud Run** - Deploy e escalabilidade

### Frontend Mobile
- **React Native** - Framework cross-platform
- **Expo** - Toolchain e bibliotecas
- **React Navigation** - Navegação
- **Redux Toolkit** - Gerenciamento de estado
- **React Hook Form** - Formulários
- **Victory Native** - Gráficos

### Ferramentas & DevOps
- **Docker** - Containerização
- **GitHub Actions** - CI/CD
- **Sentry** - Monitoramento de erros
- **Google Analytics** - Analytics

## 📦 Instalação

### Pré-requisitos

- Node.js 18+ e npm/yarn
- Python 3.11+
- Expo CLI
- Firebase CLI
- Git

### Backend Setup

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/finap.git
cd finap

# Entre no diretório do backend
cd backend

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais

# Execute o servidor de desenvolvimento
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
# Entre no diretório do frontend
cd frontend

# Instale as dependências
npm install
# ou
yarn install

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env

# Inicie o Expo
npx expo start
```

## 📁 Estrutura do Projeto

```
finap/
├── 📁 backend/
│   ├── 📁 api/
│   │   ├── 📁 routes/
│   │   ├── 📁 middlewares/
│   │   └── 📁 dependencies/
│   ├── 📁 core/
│   │   ├── 📁 config/
│   │   ├── 📁 security/
│   │   └── 📁 database/
│   ├── 📁 services/
│   │   ├── 📁 ai/
│   │   ├── 📁 whatsapp/
│   │   ├── 📁 gamification/
│   │   └── 📁 financial/
│   ├── 📁 models/
│   ├── 📁 schemas/
│   ├── 📁 utils/
│   ├── 📁 tests/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 screens/
│   │   ├── 📁 components/
│   │   ├── 📁 navigation/
│   │   ├── 📁 services/
│   │   ├── 📁 store/
│   │   ├── 📁 hooks/
│   │   ├── 📁 utils/
│   │   ├── 📁 assets/
│   │   └── 📁 constants/
│   ├── app.json
│   ├── package.json
│   └── babel.config.js
│
├── 📁 docs/
│   ├── 📁 api/
│   ├── 📁 architecture/
│   ├── 📁 guides/
│   ├── 📁 features/
│   └── 📁 deployment/
│
├── 📁 scripts/
├── 📁 .github/
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 📚 Documentação

### Documentos Principais

- [Arquitetura do Sistema](DOCUMENTO_ESCOPO_ENTREGA.md)
- [API Documentation](docs/api/API.md)
- [Guia de Desenvolvimento](docs/guides/DEVELOPMENT.md)
- [Plano de Fases](docs/PHASES.md)
- [Especificações de Features](docs/features/FEATURES.md)
- [Deploy & DevOps](docs/deployment/DEPLOYMENT.md)

### Quick Links

- [Configuração do Ambiente](docs/guides/SETUP.md)
- [Padrões de Código](docs/guides/CODE_STANDARDS.md)
- [Testes](docs/guides/TESTING.md)
- [Segurança](docs/guides/SECURITY.md)

## 🤝 Contribuindo

Adoramos contribuições! Por favor, leia nosso [Guia de Contribuição](CONTRIBUTING.md) para detalhes sobre nosso código de conduta e processo de submissão de pull requests.

### Como Contribuir

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Time de desenvolvimento
- Comunidade open source
- Usuários beta testers

## 📞 Contato

- **Email**: contato@finap.com.br
- **Website**: [www.finap.com.br](https://www.finap.com.br)
- **LinkedIn**: [FINAP](https://linkedin.com/company/finap)

---

<p align="center">
  Feito com ❤️ pela equipe FINAP
</p>
