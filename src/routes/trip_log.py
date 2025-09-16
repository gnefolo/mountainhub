"""
Blueprint for trip log (diary) endpoints.

Supports CRUD operations on trip logs. For brevity, authentication and
authorization checks are omitted; the ``user_id`` field should be
provided in the request body when creating a new trip log.
"""

from flask import Blueprint, request, jsonify

from ..models import db, TripLog


trip_log_bp = Blueprint('trip_log', __name__)


@trip_log_bp.route('/trip-logs', methods=['GET'])
def list_trip_logs() -> tuple:
    """Return a list of all trip logs in summary form."""
    user_id = request.args.get('user_id')
    query = TripLog.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    logs = query.all()
    return jsonify([log.to_summary_dict() for log in logs]), 200


@trip_log_bp.route('/trip-logs/<int:log_id>', methods=['GET'])
def get_trip_log(log_id: int) -> tuple:
    """Return a specific trip log."""
    log = TripLog.query.get(log_id)
    if not log:
        return jsonify({'error': 'Trip log not found'}), 404
    return jsonify(log.to_dict()), 200


@trip_log_bp.route('/trip-logs', methods=['POST'])
def create_trip_log() -> tuple:
    """Create a new trip log."""
    data = request.get_json() or {}
    required_fields = ['user_id', 'title', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    log = TripLog(
        user_id=data['user_id'],
        title=data['title'],
        description=data.get('description'),
        date=data['date'],
        duration_hours=data.get('duration_hours'),
        distance_km=data.get('distance_km'),
        elevation_gain=data.get('elevation_gain'),
        difficulty=data.get('difficulty'),
        trail_id=data.get('trail_id'),
        location_name=data.get('location_name'),
        location_coords=data.get('location_coords'),
        weather_conditions=data.get('weather_conditions'),
        temperature=data.get('temperature'),
        is_public=data.get('is_public', True),
        photos=data.get('photos', []),
        gpx_data=data.get('gpx_data'),
        waypoints=data.get('waypoints', []),
        notes=data.get('notes', []),
        equipment_used=data.get('equipment_used', []),
        companions=data.get('companions', []),
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(log.to_dict()), 201


@trip_log_bp.route('/trip-logs/<int:log_id>', methods=['PUT', 'PATCH'])
def update_trip_log(log_id: int) -> tuple:
    """Update an existing trip log."""
    log = TripLog.query.get(log_id)
    if not log:
        return jsonify({'error': 'Trip log not found'}), 404
    data = request.get_json() or {}
    # Update fields if provided
    for attr in [
        'title', 'description', 'date', 'duration_hours', 'distance_km', 'elevation_gain',
        'difficulty', 'trail_id', 'location_name', 'location_coords', 'weather_conditions',
        'temperature', 'is_public', 'photos', 'gpx_data', 'waypoints', 'notes',
        'equipment_used', 'companions'
    ]:
        if attr in data:
            setattr(log, attr, data[attr])
    db.session.commit()
    return jsonify(log.to_dict()), 200


@trip_log_bp.route('/trip-logs/<int:log_id>', methods=['DELETE'])
def delete_trip_log(log_id: int) -> tuple:
    """Delete a trip log by ID."""
    log = TripLog.query.get(log_id)
    if not log:
        return jsonify({'error': 'Trip log not found'}), 404
    db.session.delete(log)
    db.session.commit()
    return jsonify({'message': 'Trip log deleted'}), 200