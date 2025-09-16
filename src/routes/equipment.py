"""
Blueprint for equipment endpoints.

Provides endpoints to list equipment categories, retrieve equipment items with
filtering and generate personalised gear configurations. The actual
equipment data is stored in the database via the ``Equipment`` model and
additional recommendation logic lives in ``src.services.equipment_configurator``.
"""

from flask import Blueprint, request, jsonify

from ..models import db, Equipment
from ..services.equipment_configurator import EquipmentConfiguratorService


equipment_bp = Blueprint('equipment', __name__)

_configurator = EquipmentConfiguratorService()


@equipment_bp.route('/equipment/categories', methods=['GET'])
def list_equipment_categories() -> tuple:
    """Return a list of available equipment categories."""
    categories = ['clothing', 'footwear', 'safety', 'navigation', 'camping']
    return jsonify(categories), 200


@equipment_bp.route('/equipment', methods=['GET'])
def list_equipment() -> tuple:
    """Return equipment items with optional filters."""
    query = Equipment.query
    category = request.args.get('category')
    brand = request.args.get('brand')
    min_rating = request.args.get('min_rating', type=float)
    max_price = request.args.get('max_price', type=float)
    if category:
        query = query.filter_by(category=category)
    if brand:
        query = query.filter_by(brand=brand)
    if min_rating is not None:
        query = query.filter(Equipment.rating >= min_rating)
    results = query.all()
    # Filter by max_price by inspecting price_range JSON field
    items = []
    for item in results:
        if max_price is not None:
            price_range = item.price_range or {}
            if 'min' in price_range and price_range['min'] > max_price:
                continue
        items.append(item.to_dict())
    return jsonify(items), 200


@equipment_bp.route('/equipment/configure', methods=['POST'])
def configure_equipment() -> tuple:
    """Generate a personalised equipment configuration based on user parameters."""
    params = request.get_json() or {}
    try:
        config = _configurator.generate_configuration(params)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    return jsonify(config), 200