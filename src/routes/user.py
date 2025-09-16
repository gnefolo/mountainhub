"""
Blueprint for user management endpoints.

Provides CRUD operations on users. Passwords are stored as hashed strings
using Werkzeug security helpers. Note that this blueprint does not
implement full authentication/authorization logic such as JWT tokens. It is
intended as a starting point for further development.
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import db, User


user_bp = Blueprint('user', __name__)


@user_bp.route('/users', methods=['GET'])
def list_users() -> tuple:
    """Return a list of all users (summary representation)."""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id: str) -> tuple:
    """Return details for a specific user."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/users', methods=['POST'])
def create_user() -> tuple:
    """Create a new user. Expects JSON with username, email and password."""
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'error': 'username, email and password are required'}), 400
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already exists'}), 400
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        profile_data=data.get('profile_data'),
        skill_level=data.get('skill_level', 'beginner'),
        preferences=data.get('preferences'),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@user_bp.route('/users/<user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id: str) -> tuple:
    """Update an existing user."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json() or {}
    if 'username' in data:
        new_username = data['username']
        if new_username != user.username and User.query.filter_by(username=new_username).first():
            return jsonify({'error': 'Username already exists'}), 400
        user.username = new_username
    if 'email' in data:
        new_email = data['email']
        if new_email != user.email and User.query.filter_by(email=new_email).first():
            return jsonify({'error': 'Email already exists'}), 400
        user.email = new_email
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    if 'skill_level' in data:
        user.skill_level = data['skill_level']
    if 'profile_data' in data:
        user.profile_data = data['profile_data']
    if 'preferences' in data:
        user.preferences = data['preferences']
    db.session.commit()
    return jsonify(user.to_dict()), 200


@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id: str) -> tuple:
    """Delete a user by ID."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200