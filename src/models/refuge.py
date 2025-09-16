"""
Refuge model definition.

Represents mountain refuges, huts or shelters with associated metadata such as
location and amenities.
"""

from datetime import datetime
import uuid

from .user import db


class Refuge(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    altitude_m = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    contact_info = db.Column(db.JSON)  # {"phone": "+39...", "email": "...", "website": "..."}
    amenities = db.Column(db.JSON)  # ["restaurant", "shower", "wifi", "heating"]
    opening_periods = db.Column(db.JSON)  # [{"start": "2024-06-01", "end": "2024-09-30"}]
    booking_required = db.Column(db.Boolean, default=False)
    cai_code = db.Column(db.String(20))  # Codice CAI ufficiale
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    rating = db.Column(db.Numeric(3, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover
        return f'<Refuge {self.name}>'

    def to_dict(self) -> dict:
        """Serialize the refuge to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'altitude_m': self.altitude_m,
            'capacity': self.capacity,
            'contact_info': self.contact_info,
            'amenities': self.amenities,
            'opening_periods': self.opening_periods,
            'booking_required': self.booking_required,
            'cai_code': self.cai_code,
            'description': self.description,
            'image_url': self.image_url,
            'rating': float(self.rating) if self.rating else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
