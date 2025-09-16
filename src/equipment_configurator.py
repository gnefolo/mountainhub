"""
Service for generating equipment configurations based on user parameters.

This module provides ``EquipmentConfiguratorService``, which currently uses an
in‑memory database of sample gear to generate recommendations. In a real
application this data would come from the database and the rules would be
stored externally.
"""

from typing import Dict, List, Any


class EquipmentConfiguratorService:
    """Service for generating equipment configurations based on user parameters."""

    def __init__(self) -> None:
        self.equipment_db = self._load_equipment_database()
        self.rules = self._load_configuration_rules()

    def _load_equipment_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load equipment database from a data source.

        For now this returns a static in‑memory representation. Each entry
        contains basic metadata and suitability tags used for matching.
        """
        equipment_db: Dict[str, List[Dict[str, Any]]] = {
            # Sample footwear entries
            "footwear": [
                {
                    "id": "fw001",
                    "name": "Scarponi da trekking",
                    "brand": "La Sportiva",
                    "model": "TX4",
                    "description": "Scarponi robusti per escursionismo su terreni misti",
                    "price_range": {"min": 120, "max": 160},
                    "weight": 850,  # grams
                    "rating": 4.7,
                    "suitable_for": ["hiking", "alpinism"],
                    "seasons": ["spring", "summer", "autumn"],
                    "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/tx4.jpg",
                },
                {
                    "id": "fw002",
                    "name": "Scarponi da alpinismo",
                    "brand": "Scarpa",
                    "model": "Mont Blanc Pro GTX",
                    "description": "Scarponi tecnici per alpinismo e vie ferrate",
                    "price_range": {"min": 350, "max": 420},
                    "weight": 1200,
                    "rating": 4.8,
                    "suitable_for": ["alpinism"],
                    "seasons": ["spring", "summer", "autumn"],
                    "skill_levels": ["intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/mont_blanc.jpg",
                },
                {
                    "id": "fw003",
                    "name": "Scarponi invernali",
                    "brand": "Salomon",
                    "model": "X Ultra Winter CS WP 2",
                    "description": "Scarponi isolati per escursionismo invernale",
                    "price_range": {"min": 180, "max": 220},
                    "weight": 950,
                    "rating": 4.5,
                    "suitable_for": ["winter_hiking"],
                    "seasons": ["winter"],
                    "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/x_ultra_winter.jpg",
                },
            ],
            # Sample clothing entries
            "clothing": [
                {
                    "id": "cl001",
                    "name": "Giacca impermeabile",
                    "brand": "The North Face",
                    "model": "Dryzzle FUTURELIGHT",
                    "description": "Giacca impermeabile e traspirante per tutte le stagioni",
                    "price_range": {"min": 180, "max": 250},
                    "weight": 350,
                    "rating": 4.6,
                    "suitable_for": ["hiking", "alpinism", "winter_hiking"],
                    "seasons": ["spring", "summer", "autumn", "winter"],
                    "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/dryzzle.jpg",
                },
                {
                    "id": "cl002",
                    "name": "Pile tecnico",
                    "brand": "Patagonia",
                    "model": "R1",
                    "description": "Pile tecnico per isolamento termico",
                    "price_range": {"min": 100, "max": 140},
                    "weight": 280,
                    "rating": 4.9,
                    "suitable_for": ["hiking", "alpinism", "winter_hiking"],
                    "seasons": ["spring", "autumn", "winter"],
                    "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/r1.jpg",
                },
                {
                    "id": "cl003",
                    "name": "Piumino",
                    "brand": "Mountain Equipment",
                    "model": "Lightline",
                    "description": "Piumino caldo e leggero per temperature fredde",
                    "price_range": {"min": 220, "max": 280},
                    "weight": 500,
                    "rating": 4.7,
                    "suitable_for": ["alpinism", "winter_hiking"],
                    "seasons": ["autumn", "winter"],
                    "skill_levels": ["intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/lightline.jpg",
                },
            ],
            # Sample safety entries
            "safety": [
                {
                    "id": "sf001",
                    "name": "Kit di primo soccorso",
                    "brand": "Lifesystems",
                    "model": "Mountain Leader",
                    "description": "Kit di primo soccorso compatto per escursioni",
                    "price_range": {"min": 25, "max": 40},
                    "weight": 150,
                    "rating": 4.5,
                    "suitable_for": ["hiking", "alpinism", "winter_hiking"],
                    "seasons": ["spring", "summer", "autumn", "winter"],
                    "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/first_aid.jpg",
                },
                {
                    "id": "sf002",
                    "name": "Casco da alpinismo",
                    "brand": "Petzl",
                    "model": "Meteor",
                    "description": "Casco leggero per alpinismo e arrampicata",
                    "price_range": {"min": 80, "max": 110},
                    "weight": 240,
                    "rating": 4.8,
                    "suitable_for": ["alpinism"],
                    "seasons": ["spring", "summer", "autumn", "winter"],
                    "skill_levels": ["intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/meteor.jpg",
                },
                {
                    "id": "sf003",
                    "name": "ARTVA",
                    "brand": "Mammut",
                    "model": "Barryvox S",
                    "description": "Dispositivo di ricerca in valanga",
                    "price_range": {"min": 300, "max": 350},
                    "weight": 210,
                    "rating": 4.9,
                    "suitable_for": ["winter_hiking"],
                    "seasons": ["winter"],
                    "skill_levels": ["intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/barryvox.jpg",
                },
            ],
            # Sample navigation entries
            "navigation": [
                {
                    "id": "nv001",
                    "name": "GPS escursionistico",
                    "brand": "Garmin",
                    "model": "GPSMAP 66i",
                    "description": "GPS con messaggistica satellitare integrata",
                    "price_range": {"min": 450, "max": 500},
                    "weight": 230,
                    "rating": 4.7,
                    "suitable_for": ["hiking", "alpinism", "winter_hiking"],
                    "seasons": ["spring", "summer", "autumn", "winter"],
                    "skill_levels": ["intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/gpsmap.jpg",
                },
                {
                    "id": "nv002",
                    "name": "Bussola",
                    "brand": "Silva",
                    "model": "Expedition 4",
                    "description": "Bussola professionale con clinometro",
                    "price_range": {"min": 30, "max": 50},
                    "weight": 50,
                    "rating": 4.6,
                    "suitable_for": ["hiking", "alpinism", "winter_hiking"],
                    "seasons": ["spring", "summer", "autumn", "winter"],
                    "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/compass.jpg",
                },
                {
                    "id": "nv003",
                    "name": "Altimetro",
                    "brand": "Suunto",
                    "model": "Core",
                    "description": "Orologio con altimetro, barometro e bussola",
                    "price_range": {"min": 180, "max": 220},
                    "weight": 85,
                    "rating": 4.5,
                    "suitable_for": ["hiking", "alpinism", "winter_hiking"],
                    "seasons": ["spring", "summer", "autumn", "winter"],
                    "skill_levels": ["intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/core.jpg",
                },
            ],
            # Sample camping entries
            "camping": [
                {
                    "id": "cp001",
                    "name": "Tenda",
                    "brand": "MSR",
                    "model": "Hubba Hubba NX",
                    "description": "Tenda leggera a 2 posti per 3 stagioni",
                    "price_range": {"min": 380, "max": 450},
                    "weight": 1700,
                    "rating": 4.8,
                    "suitable_for": ["hiking", "alpinism"],
                    "seasons": ["spring", "summer", "autumn"],
                    "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/hubba.jpg",
                },
                {
                    "id": "cp002",
                    "name": "Sacco a pelo",
                    "brand": "Marmot",
                    "model": "Trestles Elite Eco 20",
                    "description": "Sacco a pelo sintetico per 3 stagioni",
                    "price_range": {"min": 150, "max": 200},
                    "weight": 1100,
                    "rating": 4.6,
                    "suitable_for": ["hiking", "alpinism"],
                    "seasons": ["spring", "summer", "autumn"],
                    "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/trestles.jpg",
                },
                {
                    "id": "cp003",
                    "name": "Materassino",
                    "brand": "Therm-a-Rest",
                    "model": "NeoAir XLite",
                    "description": "Materassino ultraleggero e isolante",
                    "price_range": {"min": 160, "max": 200},
                    "weight": 350,
                    "rating": 4.7,
                    "suitable_for": ["hiking", "alpinism"],
                    "seasons": ["spring", "summer", "autumn"],
                    "skill_levels": ["intermediate", "advanced", "expert"],
                    "image_url": "https://example.com/images/neoair.jpg",
                },
            ],
        }
        return equipment_db

    def _load_configuration_rules(self) -> Dict[str, Any]:
        """Load configuration rules.

        These rules specify which equipment categories are required or optional
        depending on the type of activity and season. They also include
        textual recommendations based on the user’s skill level.
        """
        rules: Dict[str, Any] = {
            "required_categories": {
                "hiking": {
                    "summer": ["footwear", "clothing", "safety", "navigation"],
                    "spring": ["footwear", "clothing", "safety", "navigation"],
                    "autumn": ["footwear", "clothing", "safety", "navigation"],
                    "winter": ["footwear", "clothing", "safety", "navigation"],
                },
                "alpinism": {
                    "summer": ["footwear", "clothing", "safety", "navigation"],
                    "spring": ["footwear", "clothing", "safety", "navigation"],
                    "autumn": ["footwear", "clothing", "safety", "navigation"],
                    "winter": ["footwear", "clothing", "safety", "navigation"],
                },
                "winter_hiking": {
                    "winter": ["footwear", "clothing", "safety", "navigation"],
                },
            },
            "optional_categories": {
                "hiking": {
                    "summer": ["camping"],
                    "spring": ["camping"],
                    "autumn": ["camping"],
                    "winter": ["camping"],
                },
                "alpinism": {
                    "summer": ["camping"],
                    "spring": ["camping"],
                    "autumn": ["camping"],
                    "winter": ["camping"],
                },
                "winter_hiking": {
                    "winter": ["camping"],
                },
            },
            "recommendations": {
                "hiking": {
                    "beginner": [
                        "Per escursioni di un giorno, porta almeno 1.5 litri d'acqua per persona",
                        "Controlla sempre le previsioni meteo prima di partire",
                    ],
                    "intermediate": [
                        "Considera l'uso di bastoncini da trekking per ridurre l'impatto sulle ginocchia",
                    ],
                    "advanced": [
                        "Per escursioni di più giorni, pianifica attentamente il peso dello zaino",
                    ],
                    "expert": [
                        "Considera l'uso di attrezzatura ultraleggera per ridurre il peso complessivo",
                    ],
                },
                "alpinism": {
                    "intermediate": [
                        "Assicurati di avere l'attrezzatura di sicurezza adeguata per il tipo di terreno",
                    ],
                    "advanced": [
                        "Considera un corso di alpinismo avanzato per migliorare le tue tecniche",
                    ],
                    "expert": [
                        "Valuta l'uso di attrezzatura tecnica specializzata per le condizioni specifiche",
                    ],
                },
                "winter_hiking": {
                    "beginner": [
                        "Porta sempre indumenti extra per le emergenze",
                        "Informati sul rischio valanghe prima di partire",
                    ],
                    "intermediate": [
                        "Considera un corso base di sicurezza in ambiente innevato",
                    ],
                    "advanced": [
                        "Porta sempre con te ARTVA, pala e sonda in zone a rischio valanghe",
                    ],
                    "expert": [
                        "Valuta l'uso di attrezzatura specializzata per le condizioni specifiche",
                    ],
                },
            },
        }
        return rules

    def generate_configuration(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an equipment configuration based on user parameters."""
        activity_type = params.get('activity_type', 'hiking')
        season = params.get('season', 'summer')
        duration_days = params.get('duration_days', 1)
        skill_level = params.get('skill_level', 'beginner')
        budget_max = params.get('budget_max', 1000)
        weather_conditions = params.get('weather_conditions', 'good')  # unused for now
        group_size = params.get('group_size', 1)  # unused for now

        # Validate parameters
        if activity_type not in ['hiking', 'alpinism', 'winter_hiking']:
            raise ValueError("Invalid activity type")
        if season not in ['spring', 'summer', 'autumn', 'winter']:
            raise ValueError("Invalid season")
        if skill_level not in ['beginner', 'intermediate', 'advanced', 'expert']:
            raise ValueError("Invalid skill level")

        required_categories = self.rules['required_categories'].get(activity_type, {}).get(season, [])
        optional_categories = self.rules['optional_categories'].get(activity_type, {}).get(season, [])
        # For multi‑day trips, add camping gear if not already included
        if duration_days > 1 and 'camping' not in required_categories and 'camping' in optional_categories:
            required_categories.append('camping')

        configuration: Dict[str, Any] = {}
        total_cost = 0.0

        # Generate configuration for each required category
        for category in required_categories:
            category_items = self.equipment_db.get(category, [])
            # Filter items by suitability
            suitable_items = [
                item
                for item in category_items
                if activity_type in item['suitable_for']
                and season in item['seasons']
                and skill_level in item['skill_levels']
            ]
            if not suitable_items:
                # Fallback: match on activity and season only
                suitable_items = [
                    item
                    for item in category_items
                    if activity_type in item['suitable_for'] and season in item['seasons']
                ]
            if not suitable_items:
                continue  # skip category if no matches
            # Sort by rating descending and price ascending
            suitable_items.sort(key=lambda x: (-x['rating'], x['price_range']['min']))
            selected = suitable_items[0]
            configuration[category] = selected
            total_cost += selected['price_range']['max']  # assume upper bound for safety

        # Determine if we exceed budget; if so, provide a warning
        budget_warning = total_cost > budget_max

        return {
            'config': configuration,
            'total_cost': total_cost,
            'over_budget': budget_warning,
            'recommendations': self.rules['recommendations'].get(activity_type, {}).get(skill_level, []),
        }