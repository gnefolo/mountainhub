"""
Blueprint for external services API endpoints.

This module exposes endpoints under the ``/api/external`` prefix for
retrieving weather, trail and refuge data from third‑party services. It
delegates the heavy lifting to the service classes defined in
``src.services.external_apis``.
"""

from flask import Blueprint, request, jsonify

from ..external_apis import WeatherService, TrailService, RefugeService


external_bp = Blueprint('external', __name__)

weather_service = WeatherService()
trail_service = TrailService()
refuge_service = RefugeService()


@external_bp.route('/weather', methods=['GET'])
def get_weather() -> tuple:
    """Get weather data for a specific location."""
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    timezone = request.args.get('timezone', 'auto')
    if latitude is None or longitude is None:
        return jsonify({'error': 'Latitude and longitude are required parameters'}), 400
    weather_data = weather_service.get_weather(latitude, longitude, timezone)
    if weather_data:
        return jsonify(weather_data), 200
    return jsonify({'error': 'Failed to fetch weather data'}), 500


@external_bp.route('/trails', methods=['GET'])
def get_trails() -> tuple:
    """Get hiking trails within a bounding box."""
    south = request.args.get('south', type=float)
    west = request.args.get('west', type=float)
    north = request.args.get('north', type=float)
    east = request.args.get('east', type=float)
    if None in [south, west, north, east]:
        return jsonify({'error': 'All bounding box parameters (south, west, north, east) are required'}), 400
    trail_data = trail_service.get_trails_in_area(south, west, north, east)
    if trail_data:
        return jsonify(trail_data), 200
    return jsonify({'error': 'Failed to fetch trail data'}), 500


@external_bp.route('/trails/<osm_type>/<int:osm_id>', methods=['GET'])
def get_trail_by_id(osm_type: str, osm_id: int) -> tuple:
    """Get a specific trail by its OSM ID."""
    if osm_type not in ['way', 'relation']:
        return jsonify({'error': 'OSM type must be either "way" or "relation"'}), 400
    trail_data = trail_service.get_trail_by_id(osm_id, osm_type)
    if trail_data:
        return jsonify(trail_data), 200
    return jsonify({'error': 'Failed to fetch trail data'}), 500


@external_bp.route('/refuges', methods=['GET'])
def get_refuges() -> tuple:
    """Get mountain refuges within a bounding box."""
    south = request.args.get('south', type=float)
    west = request.args.get('west', type=float)
    north = request.args.get('north', type=float)
    east = request.args.get('east', type=float)
    if None in [south, west, north, east]:
        return jsonify({'error': 'All bounding box parameters (south, west, north, east) are required'}), 400
    refuge_data = refuge_service.get_refuges_in_area(south, west, north, east)
    if refuge_data:
        return jsonify(refuge_data), 200
    return jsonify({'error': 'Failed to fetch refuge data'}), 500