"""
Trip log model definition.

Trip logs (diari di viaggio) record user outings including various details
such as date, distance, elevation gain and optionally associated trail and
equipment. They can contain photos, GPX data and notes. This model also
provides a summary dictionary for lightweight listings.
"""

import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict, MutableList

from .user import db


class TripLog(db.Model):
    """Model for user trip logs (hiking/climbing diaries)."""

    __tablename__ = 'trip_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    duration_hours = db.Column(db.Float)
    distance_km = db.Column(db.Float)
    elevation_gain = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))  # easy, moderate, hard, extreme
    trail_id = db.Column(db.String(36), db.ForeignKey('trail.id'))
    location_name = db.Column(db.String(100))
    location_coords = db.Column(MutableDict.as_mutable(JSONB))  # {lat: float, lng: float}
    weather_conditions = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Store photos as JSON array of URLs
    photos = db.Column(MutableList.as_mutable(JSONB), default=list)

    # Store GPX track data as JSON
    gpx_data = db.Column(MutableDict.as_mutable(JSONB))

    # Store waypoints as JSON array
    waypoints = db.Column(MutableList.as_mutable(JSONB), default=list)

    # Store notes as JSON array of {timestamp, text, location?}
    notes = db.Column(MutableList.as_mutable(JSONB), default=list)

    # Store equipment used as JSON array of equipment IDs
    equipment_used = db.Column(MutableList.as_mutable(JSONB), default=list)

    # Store companions as JSON array of {name, user_id?}
    companions = db.Column(MutableList.as_mutable(JSONB), default=list)

    # Relationships
    user = db.relationship('User', backref=db.backref('trip_logs', lazy=True))
    trail = db.relationship('Trail', backref=db.backref('trip_logs', lazy=True))

    def to_dict(self) -> dict:
        """Serialize trip log to a detailed dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'duration_hours': self.duration_hours,
            'distance_km': self.distance_km,
            'elevation_gain': self.elevation_gain,
            'difficulty': self.difficulty,
            'trail_id': self.trail_id,
            'location_name': self.location_name,
            'location_coords': self.location_coords,
            'weather_conditions': self.weather_conditions,
            'temperature': self.temperature,
            'is_public': self.is_public,
            'photos': self.photos,
            'gpx_data': self.gpx_data,
            'waypoints': self.waypoints,
            'notes': self.notes,
            'equipment_used': self.equipment_used,
            'companions': self.companions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user': self.user.to_dict() if self.user else None,
            'trail': self.trail.to_dict() if self.trail else None,
        }

    def to_summary_dict(self) -> dict:
        """Serialize trip log to a summary dictionary (without heavy fields)."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'date': self.date.isoformat() if self.date else None,
            'duration_hours': self.duration_hours,
            'distance_km': self.distance_km,
            'elevation_gain': self.elevation_gain,
            'difficulty': self.difficulty,
            'location_name': self.location_name,
            'weather_conditions': self.weather_conditions,
            'photo_count': len(self.photos) if self.photos else 0,
            'has_gpx': self.gpx_data is not None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_name': self.user.username if self.user else None,
        }
