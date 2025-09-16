"""
Equipment model definition.

The ``Equipment`` class stores information about gear available in the
MountainHub database. Each piece of equipment belongs to a category such as
clothing or navigation and can be filtered by the API.
"""

from datetime import datetime
import uuid

from .user import db


class Equipment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(
        db.Enum(
            'clothing', 'footwear', 'safety', 'navigation', 'camping', name='equipment_categories'
        ),
        nullable=False,
    )
    subcategory = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    # A textual description of the item
    description = db.Column(db.Text)
    # Weight in grams (optional)
    weight = db.Column(db.Integer)
    specifications = db.Column(db.JSON)
    price_range = db.Column(db.JSON)  # {"min": 100, "max": 200, "currency": "EUR"}
    season_use = db.Column(db.JSON)  # ["spring", "summer", "autumn", "winter"]
    skill_level_required = db.Column(
        db.Enum('beginner', 'intermediate', 'advanced', 'expert', name='skill_levels')
    )
    image_url = db.Column(db.String(500))
    rating = db.Column(db.Numeric(3, 2))  # 0.00 to 5.00
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover
        return f'<Equipment {self.name}>'

    def to_dict(self) -> dict:
        """Serialize the equipment to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'subcategory': self.subcategory,
            'brand': self.brand,
            'model': self.model,
            'description': self.description,
            'weight': self.weight,
            'specifications': self.specifications,
            'price_range': self.price_range,
            'season_use': self.season_use,
            'skill_level_required': self.skill_level_required,
            'image_url': self.image_url,
            'rating': float(self.rating) if self.rating else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
