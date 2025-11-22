"""
Seed Learning Module - Finanças Básicas
Populates Firestore with the first learning module.
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import init_firebase, get_firestore_client
from models.learning import LearningModule, Lesson, Quiz, Question, QuestionType


def seed_financas_basicas():
    """Seed the 'Finanças Básicas' learning module"""

    # Initialize Firebase
    init_firebase()
    db = get_firestore_client()

    # Create lessons
    lessons = [
        Lesson(
            id="lesson-1",
            title="O que é orçamento?",
            content="""
# O que é orçamento? 💰

Um **orçamento** é um plano financeiro que mostra quanto dinheiro você tem, quanto gasta e quanto sobra.

## Por que fazer um orçamento?

- **Controle**: Saber para onde seu dinheiro está indo
- **Planejamento**: Alcançar seus objetivos financeiros
- **Tranquilidade**: Evitar surpresas no fim do mês

## Como funciona?

1. **Anote suas receitas** (salário, freelances, etc.)
2. **Liste suas despesas** (aluguel, comida, transporte, etc.)
3. **Compare** receitas e despesas
4. **Ajuste** seus gastos se necessário

## Regra de Ouro

💡 **Gaste menos do que ganha!**

Se suas receitas são R$ 2.000 e suas despesas são R$ 2.500, você está gastando demais!

## Dica do FIM

Comece simples! Anote tudo que gasta por uma semana. Você vai se surpreender com pequenos gastos que somam muito no fim do mês! 📊
            """,
            duration_minutes=5,
            order=1
        ),
        Lesson(
            id="lesson-2",
            title="Receitas vs Despesas",
            content="""
# Receitas vs Despesas 💵

Entender a diferença entre receitas e despesas é o primeiro passo para o sucesso financeiro!

## Receitas 📈

São **entradas de dinheiro**:
- Salário
- Freelances
- Vendas
- Mesada
- Qualquer dinheiro que ENTRA

## Despesas 📉

São **saídas de dinheiro**:
- Aluguel
- Alimentação
- Transporte
- Lazer
- Qualquer dinheiro que SAI

## Tipos de Despesas

### 1. Despesas Fixas
Sempre o mesmo valor todo mês:
- Aluguel
- Internet
- Plano de celular

### 2. Despesas Variáveis
Mudam todo mês:
- Supermercado
- Transporte
- Lazer

### 3. Despesas Essenciais
Você não pode viver sem:
- Moradia
- Alimentação
- Saúde

### 4. Despesas Não-Essenciais
Pode cortar se precisar:
- Streaming (Netflix, Spotify)
- Delivery
- Compras por impulso

## Equação Básica

```
Receitas - Despesas = Saldo
```

Se o saldo é **positivo**, você está economizando! 🎉
Se o saldo é **negativo**, você está gastando mais do que ganha! ⚠️

## Dica do FIM

Separe suas despesas em categorias! Assim você vê exatamente onde está gastando mais e pode fazer ajustes. 🎯
            """,
            duration_minutes=7,
            order=2
        ),
        Lesson(
            id="lesson-3",
            title="Como economizar",
            content="""
# Como Economizar 🐷

Economizar não significa deixar de viver! É fazer escolhas inteligentes com seu dinheiro.

## A Regra 50-30-20

Uma forma simples de dividir seu dinheiro:

- **50%** - Necessidades (aluguel, comida, transporte)
- **30%** - Desejos (lazer, restaurantes, streaming)
- **20%** - Economia e investimentos

### Exemplo com salário de R$ 2.000:
- R$ 1.000 para necessidades
- R$ 600 para desejos
- R$ 400 para economizar

## Técnicas de Economia

### 1. Pague-se primeiro
Assim que receber o salário, separe o valor para economizar ANTES de gastar com qualquer coisa.

### 2. Corte gastos desnecessários
- Cancele assinaturas que não usa
- Evite delivery, cozinhe mais em casa
- Use transporte público quando possível

### 3. Cuidado com pequenos gastos
R$ 10 no café todo dia = R$ 300 por mês! 😱

### 4. Use a regra das 24 horas
Antes de comprar algo caro, espere 24 horas. Às vezes o desejo passa!

### 5. Compare preços
Pesquise antes de comprar. Pode economizar muito!

## Objetivos de Economia

Defina metas claras:
- ✅ "Quero economizar R$ 500 até dezembro"
- ❌ "Quero economizar dinheiro" (muito vago!)

## Comece Pequeno

Não precisa economizar muito de uma vez! Comece com:
- R$ 50 por mês
- Depois R$ 100
- Depois R$ 200

O importante é criar o hábito! 💪

## Dica do FIM

Crie uma conta separada só para economia. Quando o dinheiro está misturado com o que você usa todo dia, é muito fácil gastar! 🏦
            """,
            duration_minutes=8,
            order=3
        )
    ]

    # Create quiz questions
    questions = [
        Question(
            id="q1",
            question="Qual é a regra 50-30-20?",
            options=[
                "50% necessidades, 30% desejos, 20% economia",
                "50% economia, 30% necessidades, 20% desejos",
                "50% desejos, 30% economia, 20% necessidades",
                "50% investimentos, 30% despesas, 20% lazer"
            ],
            correct_answer=0,
            explanation="A regra 50-30-20 divide seu dinheiro em: 50% para necessidades, 30% para desejos e 20% para economia/investimentos.",
            type=QuestionType.MULTIPLE_CHOICE
        ),
        Question(
            id="q2",
            question="O que são despesas fixas?",
            options=[
                "Despesas que variam todo mês",
                "Despesas que sempre têm o mesmo valor",
                "Despesas com lazer",
                "Despesas com alimentação"
            ],
            correct_answer=1,
            explanation="Despesas fixas são aquelas que sempre têm o mesmo valor todo mês, como aluguel, internet e plano de celular.",
            type=QuestionType.MULTIPLE_CHOICE
        ),
        Question(
            id="q3",
            question="Qual é a equação básica das finanças pessoais?",
            options=[
                "Receitas + Despesas = Saldo",
                "Receitas - Despesas = Saldo",
                "Receitas x Despesas = Saldo",
                "Receitas / Despesas = Saldo"
            ],
            correct_answer=1,
            explanation="A equação básica é: Receitas - Despesas = Saldo. Se o saldo é positivo, você está economizando!",
            type=QuestionType.MULTIPLE_CHOICE
        ),
        Question(
            id="q4",
            question="O que significa 'pagar-se primeiro'?",
            options=[
                "Pagar todas as contas antes de guardar dinheiro",
                "Separar dinheiro para economizar antes de gastar com qualquer coisa",
                "Pagar o salário antes do fim do mês",
                "Pagar dívidas antes de economizar"
            ],
            correct_answer=1,
            explanation="'Pagar-se primeiro' significa separar o valor para economizar ANTES de gastar com qualquer outra coisa. Assim você garante que vai economizar!",
            type=QuestionType.MULTIPLE_CHOICE
        ),
        Question(
            id="q5",
            question="Por que pequenos gastos diários podem ser um problema?",
            options=[
                "Porque eles são ilegais",
                "Porque eles se acumulam e podem somar muito no fim do mês",
                "Porque você não pode comprar café",
                "Porque eles não fazem diferença"
            ],
            correct_answer=1,
            explanation="Pequenos gastos diários parecem insignificantes, mas se acumulam! R$ 10 por dia = R$ 300 por mês. É importante estar atento a eles.",
            type=QuestionType.MULTIPLE_CHOICE
        )
    ]

    # Create quiz
    quiz = Quiz(
        id="quiz-financas-basicas",
        title="Quiz: Finanças Básicas",
        description="Teste seus conhecimentos sobre orçamento, receitas, despesas e economia!",
        questions=questions,
        passing_score=70,
        xp_reward=50,
        coins_reward=20,
        lives_cost=1
    )

    # Create module
    module = LearningModule(
        id="module-financas-basicas",
        title="Finanças Básicas",
        description="Aprenda os conceitos fundamentais de finanças pessoais: orçamento, receitas, despesas e como economizar.",
        icon="📚",
        lessons=lessons,
        quiz=quiz,
        xp_reward=80,
        coins_reward=30,
        estimated_duration_minutes=30,
        difficulty="beginner",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Save to Firestore
    module_ref = db.collection('learning_modules').document(module.id)

    # Check if already exists
    if module_ref.get().exists:
        print(f"⚠️  Module '{module.title}' already exists. Skipping...")
        return

    module_ref.set(module.dict())

    print(f"✅ Created learning module: {module.title}")
    print(f"   📖 Lessons: {len(module.lessons)}")
    print(f"   ❓ Quiz questions: {len(module.quiz.questions)}")
    print(f"   🎯 XP Reward: {module.xp_reward}")
    print(f"   💰 Coins Reward: {module.coins_reward}")
    print(f"\n🎉 Seed completed successfully!")


if __name__ == "__main__":
    print("🌱 Seeding 'Finanças Básicas' learning module...")
    print()
    seed_financas_basicas()
