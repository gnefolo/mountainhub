"""
Trail model definition.

This module defines the ``Trail`` class representing hiking or climbing routes.
Trails are created by users and can be associated with trip logs. See the
README for details on the API endpoints available for this model.
"""

from datetime import datetime
import uuid

from .user import db  # Import the shared db instance from the user model


class Trail(db.Model):
    """Represents a trail or path suitable for hiking or climbing."""

    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # Basic metadata
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(
        db.Enum('easy', 'moderate', 'hard', 'extreme', name='difficulty_levels'), nullable=False
    )
    # Distances and elevation
    distance_km = db.Column(db.Float)  # distance in kilometres
    length_km = db.Column(db.Float)  # alias for distance_km used in tests
    elevation_gain_m = db.Column(db.Integer)  # elevation gain in metres
    elevation_gain = db.Column(db.Integer)  # alias for elevation_gain_m used in tests
    # Duration
    estimated_duration_hours = db.Column(db.Float)  # estimated duration in hours
    estimated_time_hours = db.Column(db.Float)  # alias for estimated_duration_hours used in tests
    # GPX file URL (optional)
    gpx_file_url = db.Column(db.String(500))
    # Start/end points and region/country
    start_point = db.Column(db.String(200))
    end_point = db.Column(db.String(200))
    region = db.Column(db.String(100))
    country = db.Column(db.String(100))
    # JSON fields
    season_availability = db.Column(db.JSON)  # e.g., ["spring", "summer"]
    coordinates = db.Column(db.JSON)  # start/end coordinates as dict
    # Foreign keys / relationships
    created_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trip_logs = db.relationship('TripLog', backref='trail', lazy=True)

    def __repr__(self) -> str:  # pragma: no cover
        return f'<Trail {self.name}>'

    def to_dict(self) -> dict:
        """Serialize the trail to a dictionary for JSON responses."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty,
            'distance_km': self.distance_km,
            'length_km': self.length_km,
            'elevation_gain_m': self.elevation_gain_m,
            'elevation_gain': self.elevation_gain,
            'estimated_duration_hours': self.estimated_duration_hours,
            'estimated_time_hours': self.estimated_time_hours,
            'gpx_file_url': self.gpx_file_url,
            'start_point': self.start_point,
            'end_point': self.end_point,
            'region': self.region,
            'country': self.country,
            'season_availability': self.season_availability,
            'coordinates': self.coordinates,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
