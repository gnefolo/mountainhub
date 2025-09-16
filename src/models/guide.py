"""
Guide and user progress models.

This module defines two models:

* ``Guide``: Represents a progressive guide for users learning hiking or
  climbing skills. Guides contain a series of steps and may recommend
  specific trails.
* ``UserGuideProgress``: Tracks a user’s progress through a guide,
  including completed steps and timestamps.
"""

import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from .user import db


class Guide(db.Model):
    """Model for progressive guides."""

    __tablename__ = 'guides'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced, expert
    duration_days = db.Column(db.Integer, nullable=False, default=1)
    elevation_gain = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Store steps as JSON
    steps = db.Column(MutableDict.as_mutable(JSONB), default=list)

    # Store recommended trails as JSON array of trail IDs
    recommended_trails = db.Column(MutableDict.as_mutable(JSONB), default=list)

    def to_dict(self) -> dict:
        """Convert guide to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'duration_days': self.duration_days,
            'elevation_gain': self.elevation_gain,
            'image_url': self.image_url,
            'steps': self.steps,
            'recommended_trails': self.recommended_trails,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class UserGuideProgress(db.Model):
    """Model for tracking user progress through guides."""

    __tablename__ = 'user_guide_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    guide_id = db.Column(db.Integer, db.ForeignKey('guides.id'), nullable=False)
    completed_steps = db.Column(MutableDict.as_mutable(JSONB), default=list)
    completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # Relationships
    user = db.relationship('User', backref=db.backref('guide_progress', lazy=True))
    guide = db.relationship('Guide', backref=db.backref('user_progress', lazy=True))

    def to_dict(self) -> dict:
        """Convert progress to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'guide_id': self.guide_id,
            'completed_steps': self.completed_steps,
            'total_steps': len(self.guide.steps) if self.guide else 0,
            'completed': self.completed,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }