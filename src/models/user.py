"""
User model definition.

This module defines the ``User`` class representing registered users of
MountainHub. It also instantiates the global SQLAlchemy object ``db`` which
is used by all other models. When the Flask application initialises the
database in ``src/main.py``, this ``db`` instance will be bound to the
application context.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# Instantiate the SQLAlchemy object. This should be initialised with
# ``app.config`` in ``src/main.py`` via ``db.init_app(app)``.
db = SQLAlchemy()


class User(db.Model):
    """Represents a user account in the system."""

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_data = db.Column(db.JSON)
    skill_level = db.Column(
        db.Enum('beginner', 'intermediate', 'advanced', 'expert', name='skill_levels'),
        default='beginner'
    )
    preferences = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trip_logs = db.relationship('TripLog', backref='user', lazy=True)

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return f'<User {self.username}>'

    def to_dict(self) -> dict:
        """Serialize the user to a dictionary excluding sensitive fields."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'skill_level': self.skill_level,
            'profile_data': self.profile_data,
            'preferences': self.preferences,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
