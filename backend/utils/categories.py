"""
Category Utilities
Automatic categorization of transactions based on keywords.
Based on MVP requirements in docs/MVP_ROADMAP.md
"""

from typing import Dict, List


# Category keywords mapping
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    'alimentação': [
        'mercado', 'supermercado', 'restaurante', 'lanche', 'almoço',
        'jantar', 'café', 'comida', 'food', 'ifood', 'rappi', 'delivery',
        'padaria', 'açougue', 'feira', 'hortifruti', 'bebida', 'pizza',
        'hamburguer', 'sushi', 'churrasco', 'lanchonete'
    ],
    'transporte': [
        'uber', '99', 'taxi', 'ônibus', 'metrô', 'combustível',
        'gasolina', 'álcool', 'etanol', 'diesel', 'estacionamento',
        'pedágio', 'moto', 'carro', 'transporte', 'mobilidade'
    ],
    'moradia': [
        'aluguel', 'condomínio', 'luz', 'água', 'gás', 'internet',
        'telefone', 'celular', 'tv', 'streaming', 'energia', 'iptu',
        'casa', 'apartamento', 'imóvel'
    ],
    'saúde': [
        'farmácia', 'remédio', 'médico', 'consulta', 'exame',
        'hospital', 'plano', 'saúde', 'dentista', 'laboratório',
        'clínica', 'medicamento', 'droga', 'vacina'
    ],
    'educação': [
        'curso', 'livro', 'faculdade', 'escola', 'universidade',
        'material', 'apostila', 'aula', 'professor', 'ensino',
        'estudo', 'educação', 'colégio', 'educacional'
    ],
    'lazer': [
        'cinema', 'netflix', 'spotify', 'jogo', 'bar', 'festa',
        'show', 'teatro', 'parque', 'diversão', 'entretenimento',
        'balada', 'pub', 'clube', 'viagem', 'turismo', 'hobby'
    ],
    'compras': [
        'roupa', 'sapato', 'presente', 'shopping', 'loja',
        'vestuário', 'calça', 'camisa', 'tênis', 'bolsa',
        'acessório', 'eletrônico', 'móvel', 'decoração'
    ],
    'outros': []  # Default category
}


# Category metadata (icon, color, budget suggestions)
CATEGORY_METADATA: Dict[str, Dict[str, str]] = {
    'alimentação': {
        'icon': '🍔',
        'color': '#FF6B6B',
        'name': 'Alimentação'
    },
    'transporte': {
        'icon': '🚗',
        'color': '#4ECDC4',
        'name': 'Transporte'
    },
    'moradia': {
        'icon': '🏠',
        'color': '#45B7D1',
        'name': 'Moradia'
    },
    'saúde': {
        'icon': '💊',
        'color': '#96CEB4',
        'name': 'Saúde'
    },
    'educação': {
        'icon': '📚',
        'color': '#FFEAA7',
        'name': 'Educação'
    },
    'lazer': {
        'icon': '🎮',
        'color': '#DFE6E9',
        'name': 'Lazer'
    },
    'compras': {
        'icon': '🛍️',
        'color': '#A29BFE',
        'name': 'Compras'
    },
    'outros': {
        'icon': '📦',
        'color': '#636E72',
        'name': 'Outros'
    },
    'receita': {
        'icon': '💰',
        'color': '#00B894',
        'name': 'Receita'
    }
}


def categorize_transaction(description: str) -> str:
    """
    Automatically categorize a transaction based on its description.

    Args:
        description: Transaction description text

    Returns:
        str: Category name (e.g., 'alimentação', 'transporte', 'outros')

    Example:
        >>> categorize_transaction("Almoço no restaurante")
        'alimentação'
        >>> categorize_transaction("Uber para o trabalho")
        'transporte'
    """
    if not description:
        return 'outros'

    description_lower = description.lower().strip()

    # Search for keywords in each category
    for category, keywords in CATEGORY_KEYWORDS.items():
        if category == 'outros':
            continue

        for keyword in keywords:
            if keyword in description_lower:
                return category

    # Default to 'outros' if no match found
    return 'outros'


def get_category_metadata(category: str) -> Dict[str, str]:
    """
    Get metadata for a category (icon, color, display name).

    Args:
        category: Category identifier

    Returns:
        Dict with icon, color, and name fields
    """
    return CATEGORY_METADATA.get(category, CATEGORY_METADATA['outros'])


def get_all_categories() -> List[Dict[str, str]]:
    """
    Get all available categories with their metadata.

    Returns:
        List of category dictionaries with id, name, icon, and color
    """
    categories = []
    for category_id, metadata in CATEGORY_METADATA.items():
        categories.append({
            'id': category_id,
            **metadata
        })
    return categories


def validate_category(category: str) -> bool:
    """
    Check if a category is valid.

    Args:
        category: Category identifier to validate

    Returns:
        bool: True if category exists, False otherwise
    """
    return category in CATEGORY_KEYWORDS
