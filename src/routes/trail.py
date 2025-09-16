"""
Blueprint for trail management endpoints.

Exposes CRUD operations for the ``Trail`` model. Users can create new
trails, list all trails, retrieve a specific trail by ID, update and
delete existing trails. For simplicity, this implementation does not
include authentication; the ``created_by`` field should be supplied by the
client with a valid user ID.
"""

from flask import Blueprint, request, jsonify

from ..models import db, Trail


trail_bp = Blueprint('trail', __name__)


@trail_bp.route('/trails', methods=['GET'])
def list_trails() -> tuple:
    """Return a list of all trails."""
    trails = Trail.query.all()
    return jsonify([trail.to_dict() for trail in trails]), 200


@trail_bp.route('/trails/<trail_id>', methods=['GET'])
def get_trail(trail_id: str) -> tuple:
    """Return details for a specific trail."""
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({'error': 'Trail not found'}), 404
    return jsonify(trail.to_dict()), 200


@trail_bp.route('/trails', methods=['POST'])
def create_trail() -> tuple:
    """Create a new trail."""
    data = request.get_json() or {}
    name = data.get('name')
    difficulty = data.get('difficulty')
    created_by = data.get('created_by')
    if not name or not difficulty or not created_by:
        return jsonify({'error': 'name, difficulty and created_by are required'}), 400
    trail = Trail(
        name=name,
        description=data.get('description'),
        difficulty=difficulty,
        distance_km=data.get('distance_km'),
        elevation_gain_m=data.get('elevation_gain_m'),
        estimated_duration_hours=data.get('estimated_duration_hours'),
        gpx_file_url=data.get('gpx_file_url'),
        region=data.get('region'),
        season_availability=data.get('season_availability'),
        created_by=created_by,
    )
    db.session.add(trail)
    db.session.commit()
    return jsonify(trail.to_dict()), 201


@trail_bp.route('/trails/<trail_id>', methods=['PUT', 'PATCH'])
def update_trail(trail_id: str) -> tuple:
    """Update an existing trail."""
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({'error': 'Trail not found'}), 404
    data = request.get_json() or {}
    for attr in [
        'name', 'description', 'difficulty', 'distance_km', 'elevation_gain_m',
        'estimated_duration_hours', 'gpx_file_url', 'region', 'season_availability',
    ]:
        if attr in data:
            setattr(trail, attr, data[attr])
    db.session.commit()
    return jsonify(trail.to_dict()), 200


@trail_bp.route('/trails/<trail_id>', methods=['DELETE'])
def delete_trail(trail_id: str) -> tuple:
    """Delete a trail by ID."""
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({'error': 'Trail not found'}), 404
    db.session.delete(trail)
    db.session.commit()
    return jsonify({'message': 'Trail deleted'}), 200