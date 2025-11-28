"""
Courses Content
Contains all course and module content for the FINAP app.
"""

# =============================================================================
# CURSO 1: INÍCIO FINANCEIRO
# =============================================================================

COURSE_1 = {
    "id": "course_inicio_financeiro",
    "title": "Início Financeiro",
    "description": "Aprenda os fundamentos para começar sua jornada financeira",
    "icon": "Wallet",
    "color": "#14B8A6",
    "gradient": "from-teal-500 to-emerald-500",
    "order": 1,
    "total_modules": 4,
    "estimated_hours": 2,
    "difficulty": "beginner"
}

# =============================================================================
# MÓDULO 1: MENTALIDADE FINANCEIRA
# =============================================================================

MODULE_1 = {
    "id": "mod_mentalidade_financeira",
    "course_id": "course_inicio_financeiro",
    "title": "Mentalidade Financeira",
    "description": "Desenvolva uma relação saudável com o dinheiro",
    "icon": "Brain",
    "order": 1,
    "difficulty": "beginner",
    "estimated_duration_minutes": 30,
    "xp_reward": 100,
    "coins_reward": 50,
    "phases": [
        # =====================================================================
        # FASE 1: O QUE É DINHEIRO?
        # =====================================================================
        {
            "id": "phase_1_dinheiro",
            "title": "O que é Dinheiro?",
            "description": "Entenda o conceito de dinheiro e sua importância",
            "order": 1,
            "lessons": [
                {
                    "id": "lesson_1_1",
                    "title": "A História do Dinheiro",
                    "order": 1,
                    "duration_minutes": 3,
                    "content": """# A História do Dinheiro 💰

Você já parou pra pensar como surgiu esse negócio de dinheiro? Bora entender!

## Antes do Dinheiro: O Escambo

Imagina só: antigamente, se você quisesse pão, tinha que trocar por algo que você tinha. Tipo, galinhas por trigo! 🐔↔️🌾

**Problema:** E se o padeiro não quisesse suas galinhas? Aí complicava tudo!

## O Surgimento das Moedas

Por volta de 600 a.C., surgiram as primeiras moedas. Elas eram feitas de metais preciosos como ouro e prata.

**Vantagens:**
- Fácil de carregar
- Todo mundo aceitava
- Durava muito tempo

## O Dinheiro Hoje

Hoje usamos:
- **Papel-moeda** (notas de real)
- **Moedas** (1 real, 50 centavos...)
- **Dinheiro digital** (Pix, cartões)

> 💡 **Dica do FIM:** O dinheiro é só uma ferramenta de troca. O importante é saber usar!"""
                },
                {
                    "id": "lesson_1_2",
                    "title": "Dinheiro como Ferramenta",
                    "order": 2,
                    "duration_minutes": 3,
                    "content": """# Dinheiro: Sua Ferramenta de Liberdade 🔧

Mano, dinheiro não é o objetivo final da vida. É uma **ferramenta** pra você conquistar o que quer!

## O Dinheiro Permite:

### 1. Segurança 🛡️
Ter uma reserva te dá paz de espírito. Imprevistos acontecem!

### 2. Escolhas ✨
Com dinheiro você pode escolher:
- Onde morar
- O que estudar
- Como se divertir

### 3. Ajudar Outros ❤️
Quando você tem, pode contribuir com causas que acredita.

## Mentalidade Saudável

**Errado:** "Preciso ter muito dinheiro pra ser feliz"

**Certo:** "Dinheiro me ajuda a construir a vida que quero"

> 💡 **Sacada importante:** Dinheiro é meio, não fim. Foque no que você quer FAZER com ele!

## Reflexão

Pense: o que você faria se tivesse mais dinheiro?
- Viajar?
- Ajudar sua família?
- Comprar algo especial?

Essas são suas motivações! Guarde elas no coração."""
                }
            ],
            "quiz": {
                "id": "quiz_phase_1",
                "title": "Quiz: O que é Dinheiro?",
                "description": "Teste seus conhecimentos sobre dinheiro",
                "passing_score": 34,  # 1 de 3 = 33.33%, arredondando
                "xp_reward": 30,
                "coins_reward": 15,
                "lives_cost": 1,
                "questions": [
                    {
                        "id": "q1_1",
                        "question": "O que era o escambo?",
                        "options": [
                            "Um tipo de moeda antiga",
                            "Troca direta de produtos ou serviços",
                            "Um banco medieval",
                            "Uma forma de investimento"
                        ],
                        "correct_answer": 1,
                        "explanation": "Escambo era a troca direta de produtos ou serviços, antes do dinheiro existir."
                    },
                    {
                        "id": "q1_2",
                        "question": "Qual a melhor forma de enxergar o dinheiro?",
                        "options": [
                            "Como objetivo final da vida",
                            "Como algo ruim e sujo",
                            "Como uma ferramenta para conquistar objetivos",
                            "Como algo impossível de conseguir"
                        ],
                        "correct_answer": 2,
                        "explanation": "Dinheiro é uma ferramenta que nos ajuda a conquistar nossos objetivos e ter mais escolhas na vida."
                    },
                    {
                        "id": "q1_3",
                        "question": "Quais formas de dinheiro usamos hoje?",
                        "options": [
                            "Apenas moedas de ouro",
                            "Apenas papel-moeda",
                            "Papel-moeda, moedas e dinheiro digital",
                            "Apenas escambo"
                        ],
                        "correct_answer": 2,
                        "explanation": "Hoje usamos várias formas: notas, moedas e dinheiro digital (Pix, cartões, etc)."
                    }
                ]
            },
            "rewards": {
                "xp": 30,
                "coins": 15
            }
        },
        # =====================================================================
        # FASE 2: RENDA vs DESPESA
        # =====================================================================
        {
            "id": "phase_2_renda_despesa",
            "title": "Renda vs Despesa",
            "description": "Entenda a diferença entre o que entra e o que sai",
            "order": 2,
            "lessons": [
                {
                    "id": "lesson_2_1",
                    "title": "O que é Renda?",
                    "order": 1,
                    "duration_minutes": 3,
                    "content": """# Entendendo sua Renda 💵

Bora falar de grana entrando! Renda é todo dinheiro que você **recebe**.

## Tipos de Renda

### 1. Renda Ativa 💪
É quando você troca seu **tempo/trabalho** por dinheiro:
- Mesada dos pais
- Salário do estágio
- Freelas e bicos
- Venda de produtos

### 2. Renda Passiva 😴
Dinheiro que entra sem você precisar trabalhar ativamente:
- Rendimento de investimentos
- Aluguel de algo seu
- Royalties

> 💡 **Meta de vida:** Construir fontes de renda passiva!

## Sua Renda Atual

Se você é jovem, provavelmente sua renda vem de:
- Mesada
- Trabalhos eventuais
- Presentes de aniversário

**E tá tudo bem!** O importante é começar a entender como funciona.

## Dica de Ouro 🏆

Anote TODA renda que você recebe. Sério, toda mesmo!
- R$ 50 da vó? Anota!
- R$ 20 por ajudar o vizinho? Anota!

Isso te dá clareza sobre quanto você realmente tem."""
                },
                {
                    "id": "lesson_2_2",
                    "title": "Controlando suas Despesas",
                    "order": 2,
                    "duration_minutes": 3,
                    "content": """# Suas Despesas na Real 💸

Despesa é todo dinheiro que **sai** do seu bolso. E aqui mora o perigo, mano!

## Tipos de Despesas

### Fixas 📌
Aquelas que vêm todo mês, no mesmo valor:
- Plano de celular
- Streaming (Netflix, Spotify)
- Mensalidade de curso

### Variáveis 📊
Mudam de mês pra mês:
- Alimentação fora
- Lazer (cinema, rolê)
- Roupas e acessórios

### Surpresa 😱
Gastos inesperados:
- Celular quebrou
- Remédio
- Presente de última hora

## A Regra de Ouro

> **Renda > Despesas = Sobra (Economia)**
> **Renda < Despesas = Problema (Dívida)**

## Gastos Invisíveis

Cuidado com os "gastinhos":
- Aquele café de R$ 8
- Delivery de R$ 25
- Skin do jogo de R$ 15

Parece pouco, mas no fim do mês... 💀

## Exercício Prático

Durante 1 semana, anote TUDO que você gastar. Tudo mesmo!

Você vai se surpreender com onde seu dinheiro vai."""
                }
            ],
            "quiz": {
                "id": "quiz_phase_2",
                "title": "Quiz: Renda vs Despesa",
                "description": "Teste seus conhecimentos sobre renda e despesas",
                "passing_score": 34,
                "xp_reward": 30,
                "coins_reward": 15,
                "lives_cost": 1,
                "questions": [
                    {
                        "id": "q2_1",
                        "question": "Qual é um exemplo de renda passiva?",
                        "options": [
                            "Salário do trabalho",
                            "Mesada dos pais",
                            "Rendimento de investimentos",
                            "Pagamento por um freela"
                        ],
                        "correct_answer": 2,
                        "explanation": "Renda passiva é aquela que você recebe sem precisar trabalhar ativamente, como rendimentos de investimentos."
                    },
                    {
                        "id": "q2_2",
                        "question": "O que acontece quando suas despesas são maiores que sua renda?",
                        "options": [
                            "Você fica rico",
                            "Você acumula dívidas",
                            "Nada acontece",
                            "Você ganha mais dinheiro"
                        ],
                        "correct_answer": 1,
                        "explanation": "Quando gastamos mais do que ganhamos, entramos em dívida. Por isso é importante controlar os gastos!"
                    },
                    {
                        "id": "q2_3",
                        "question": "Qual destes é uma despesa FIXA?",
                        "options": [
                            "Cinema no fim de semana",
                            "Lanche na escola",
                            "Assinatura do Spotify",
                            "Presente de aniversário"
                        ],
                        "correct_answer": 2,
                        "explanation": "Despesas fixas são aquelas com valor e frequência constantes, como assinaturas mensais."
                    }
                ]
            },
            "rewards": {
                "xp": 30,
                "coins": 15
            }
        },
        # =====================================================================
        # FASE 3: MENTALIDADE DE ABUNDÂNCIA
        # =====================================================================
        {
            "id": "phase_3_abundancia",
            "title": "Mentalidade de Abundância",
            "description": "Transforme sua forma de pensar sobre dinheiro",
            "order": 3,
            "lessons": [
                {
                    "id": "lesson_3_1",
                    "title": "Escassez vs Abundância",
                    "order": 1,
                    "duration_minutes": 3,
                    "content": """# Sua Mente e o Dinheiro 🧠

A forma como você PENSA sobre dinheiro muda TUDO na sua vida financeira.

## Mentalidade de Escassez 😰

Pensamentos tipo:
- "Nunca vou ter dinheiro suficiente"
- "Dinheiro é difícil de conseguir"
- "Pessoas ricas são más"
- "Não nasci pra ser rico"

**Resultado:** Medo, ansiedade, decisões ruins.

## Mentalidade de Abundância 🌟

Pensamentos tipo:
- "Existem oportunidades em todo lugar"
- "Posso aprender a ganhar mais"
- "Dinheiro é uma ferramenta neutra"
- "Mereço prosperidade"

**Resultado:** Confiança, criatividade, boas decisões.

## Qual é a sua?

Presta atenção nos seus pensamentos sobre dinheiro.

Quando você vê algo caro, pensa:
- A) "Nunca vou poder comprar isso" 😔
- B) "O que preciso fazer pra conseguir isso?" 🤔

> 💡 **A diferença:** Uma te paralisa, a outra te movimenta!

## Mudando o Chip

Toda vez que pensar "não posso", troque por "como posso?"

É treino! No começo é difícil, mas melhora."""
                },
                {
                    "id": "lesson_3_2",
                    "title": "Construindo Hábitos Financeiros",
                    "order": 2,
                    "duration_minutes": 3,
                    "content": """# Hábitos que Mudam Tudo 🔄

Sabe o que separa quem tem controle financeiro de quem não tem? **Hábitos!**

## 5 Hábitos de Ouro

### 1. Anote seus gastos 📝
Todo dia, por 5 minutos. Simples assim!

### 2. Pague-se primeiro 💰
Assim que receber dinheiro, separe uma parte pra você (economia).

### 3. Espere 24 horas ⏰
Antes de comprar algo caro, espere um dia. Se ainda quiser, compre.

### 4. Compare preços 🔍
Nunca compre a primeira opção. Pesquise!

### 5. Revise semanalmente 📊
Todo domingo, olhe seus gastos da semana.

## O Poder do Hábito

> Um hábito pequeno feito **todo dia** é mais poderoso que uma grande ação feita **uma vez**.

## Comece Devagar

Não tente mudar tudo de uma vez! Escolha UM hábito e pratique por 21 dias.

Depois, adicione outro.

## Seu Desafio 🎯

Escolha agora: qual dos 5 hábitos você vai começar essa semana?

1. Anotar gastos
2. Pagar-se primeiro
3. Esperar 24h
4. Comparar preços
5. Revisar semanalmente

**Comprometa-se!** Fala pra alguém que você vai fazer isso."""
                }
            ],
            "quiz": {
                "id": "quiz_phase_3",
                "title": "Quiz: Mentalidade de Abundância",
                "description": "Teste seus conhecimentos sobre mentalidade financeira",
                "passing_score": 34,
                "xp_reward": 30,
                "coins_reward": 15,
                "lives_cost": 1,
                "questions": [
                    {
                        "id": "q3_1",
                        "question": "O que caracteriza uma mentalidade de abundância?",
                        "options": [
                            "Acreditar que dinheiro é impossível de conseguir",
                            "Pensar que só pessoas sortudas ficam ricas",
                            "Acreditar que existem oportunidades em todo lugar",
                            "Achar que dinheiro é ruim"
                        ],
                        "correct_answer": 2,
                        "explanation": "A mentalidade de abundância acredita em oportunidades e possibilidades, não em limitações."
                    },
                    {
                        "id": "q3_2",
                        "question": "Qual hábito ajuda a evitar compras por impulso?",
                        "options": [
                            "Comprar sempre que ver promoção",
                            "Esperar 24 horas antes de comprar",
                            "Comprar tudo à vista",
                            "Nunca olhar o preço"
                        ],
                        "correct_answer": 1,
                        "explanation": "Esperar 24 horas te dá tempo pra pensar se realmente precisa daquilo."
                    },
                    {
                        "id": "q3_3",
                        "question": "O que significa 'pagar-se primeiro'?",
                        "options": [
                            "Comprar o que quiser antes de pagar contas",
                            "Separar uma parte do dinheiro pra economia assim que receber",
                            "Pagar todas as dívidas primeiro",
                            "Gastar tudo e guardar o que sobrar"
                        ],
                        "correct_answer": 1,
                        "explanation": "Pagar-se primeiro significa priorizar sua economia, guardando dinheiro antes de gastar com outras coisas."
                    }
                ]
            },
            "rewards": {
                "xp": 30,
                "coins": 15
            }
        },
        # =====================================================================
        # FASE 4: METAS FINANCEIRAS
        # =====================================================================
        {
            "id": "phase_4_metas",
            "title": "Metas Financeiras",
            "description": "Aprenda a definir e alcançar seus objetivos financeiros",
            "order": 4,
            "lessons": [
                {
                    "id": "lesson_4_1",
                    "title": "Definindo suas Metas",
                    "order": 1,
                    "duration_minutes": 3,
                    "content": """# Metas Financeiras: Seu GPS pro Sucesso 🎯

Ter dinheiro sem saber pra que é igual ter GPS sem destino. Bora definir suas metas!

## Por que ter Metas?

Metas te dão:
- **Direção:** Saber pra onde ir
- **Motivação:** Razão pra economizar
- **Foco:** Evitar gastos desnecessários

## Tipos de Metas

### Curto Prazo (até 1 ano) ⚡
- Comprar um tênis novo
- Juntar pra um role
- Comprar um jogo

### Médio Prazo (1-5 anos) 📅
- Trocar de celular
- Fazer uma viagem
- Curso ou certificação

### Longo Prazo (mais de 5 anos) 🌟
- Faculdade
- Carro próprio
- Morar sozinho

## Método SMART

Suas metas devem ser:
- **S**pecífica: O que exatamente?
- **M**ensurável: Quanto custa?
- **A**tingível: É possível?
- **R**elevante: Faz sentido pra você?
- **T**emporal: Quando vai conseguir?

> 💡 **Exemplo SMART:** "Vou juntar R$ 500 em 5 meses pra comprar um fone Bluetooth, guardando R$ 100 por mês da minha mesada."

## Sua Vez!

Escreva 3 metas:
1. Uma de curto prazo
2. Uma de médio prazo
3. Uma de longo prazo"""
                },
                {
                    "id": "lesson_4_2",
                    "title": "Alcançando suas Metas",
                    "order": 2,
                    "duration_minutes": 3,
                    "content": """# Transformando Sonhos em Realidade 🚀

Definiu suas metas? Agora vem a parte boa: fazer acontecer!

## O Plano de Ação

### 1. Calcule o Valor Total 🧮
Quanto custa sua meta? Pesquise bem!

### 2. Defina o Prazo ⏰
Em quanto tempo quer alcançar?

### 3. Divida em Parcelas 📊
Valor ÷ Meses = Quanto guardar por mês

**Exemplo:**
- Meta: R$ 600 (celular novo)
- Prazo: 6 meses
- Guardar: R$ 100/mês

## Técnicas que Funcionam

### Envelope Mental 💌
Separe mentalmente (ou em potes!) dinheiro pra cada meta.

### Automação 🤖
Se possível, programe transferência automática assim que cair a grana.

### Visualização 👀
Cole uma foto da sua meta onde você veja todo dia!

### Celebre as Pequenas Vitórias 🎉
Juntou o primeiro mês? Comemora! Isso te motiva.

## Obstáculos Comuns

❌ "Ah, só esse mês eu gasto..."
✅ Solução: Lembre da meta antes de gastar

❌ "Tá demorando muito..."
✅ Solução: Divida em metas menores

❌ "Surgiu um imprevisto..."
✅ Solução: Tenha uma reserva separada

## Dica Final

> 💡 **Progress, not perfection!** (Progresso, não perfeição)

Se um mês não conseguir guardar tudo, guarde o que der. Melhor pouco que nada!

**Você consegue! 💪**"""
                }
            ],
            "quiz": {
                "id": "quiz_phase_4",
                "title": "Quiz: Metas Financeiras",
                "description": "Teste seus conhecimentos sobre metas financeiras",
                "passing_score": 34,
                "xp_reward": 30,
                "coins_reward": 15,
                "lives_cost": 1,
                "questions": [
                    {
                        "id": "q4_1",
                        "question": "O que significa o 'M' no método SMART?",
                        "options": [
                            "Motivador",
                            "Mensurável",
                            "Maior",
                            "Moderno"
                        ],
                        "correct_answer": 1,
                        "explanation": "O 'M' significa Mensurável - sua meta precisa ter um valor ou quantidade específica que você possa medir."
                    },
                    {
                        "id": "q4_2",
                        "question": "Qual é uma meta de CURTO prazo?",
                        "options": [
                            "Comprar uma casa",
                            "Fazer faculdade",
                            "Comprar um tênis novo",
                            "Ter um carro"
                        ],
                        "correct_answer": 2,
                        "explanation": "Metas de curto prazo são aquelas que podem ser alcançadas em até 1 ano, como comprar itens menores."
                    },
                    {
                        "id": "q4_3",
                        "question": "Se você quer juntar R$ 600 em 6 meses, quanto deve guardar por mês?",
                        "options": [
                            "R$ 50",
                            "R$ 100",
                            "R$ 200",
                            "R$ 60"
                        ],
                        "correct_answer": 1,
                        "explanation": "R$ 600 dividido por 6 meses = R$ 100 por mês. Dividir a meta em parcelas mensais facilita alcançá-la!"
                    }
                ]
            },
            "rewards": {
                "xp": 30,
                "coins": 15
            }
        }
    ]
}

# =============================================================================
# CURSO 2: INVESTIMENTOS BÁSICOS (Bloqueado)
# =============================================================================

COURSE_2 = {
    "id": "course_investimentos_basicos",
    "title": "Investimentos Básicos",
    "description": "Descubra como fazer seu dinheiro trabalhar pra você",
    "icon": "TrendingUp",
    "color": "#8B5CF6",
    "gradient": "from-violet-500 to-purple-500",
    "order": 2,
    "total_modules": 4,
    "estimated_hours": 3,
    "difficulty": "intermediate",
    "locked": True,
    "locked_message": "Complete o curso 'Início Financeiro' primeiro!"
}

# =============================================================================
# CURSO 3: EMPREENDEDORISMO JOVEM (Bloqueado)
# =============================================================================

COURSE_3 = {
    "id": "course_empreendedorismo",
    "title": "Empreendedorismo Jovem",
    "description": "Aprenda a criar seu próprio negócio desde cedo",
    "icon": "Rocket",
    "color": "#F59E0B",
    "gradient": "from-amber-500 to-orange-500",
    "order": 3,
    "total_modules": 5,
    "estimated_hours": 4,
    "difficulty": "intermediate",
    "locked": True,
    "locked_message": "Complete o curso 'Investimentos Básicos' primeiro!"
}

# =============================================================================
# MÓDULO 2: ORÇAMENTO PESSOAL (para futuro)
# =============================================================================

MODULE_2 = {
    "id": "mod_orcamento_pessoal",
    "course_id": "course_inicio_financeiro",
    "title": "Orçamento Pessoal",
    "description": "Aprenda a criar e seguir um orçamento",
    "icon": "Calculator",
    "order": 2,
    "difficulty": "beginner",
    "estimated_duration_minutes": 35,
    "xp_reward": 120,
    "coins_reward": 60,
    "phases": []  # Será preenchido depois
}

# =============================================================================
# MÓDULO 3: ECONOMIA INTELIGENTE (para futuro)
# =============================================================================

MODULE_3 = {
    "id": "mod_economia_inteligente",
    "course_id": "course_inicio_financeiro",
    "title": "Economia Inteligente",
    "description": "Técnicas para economizar sem sofrer",
    "icon": "PiggyBank",
    "order": 3,
    "difficulty": "beginner",
    "estimated_duration_minutes": 30,
    "xp_reward": 100,
    "coins_reward": 50,
    "phases": []  # Será preenchido depois
}

# =============================================================================
# LISTA DE TODOS OS CURSOS E MÓDULOS
# =============================================================================

ALL_COURSES = [COURSE_1, COURSE_2, COURSE_3]

ALL_MODULES = [MODULE_1, MODULE_2, MODULE_3]

# Módulos completos (com fases)
COMPLETE_MODULES = [MODULE_1]
