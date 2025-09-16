"""
Blueprint for progressive guide endpoints.

Allows clients to list guides, retrieve a single guide, check user progress
and mark steps as completed. In this implementation the user ID must be
supplied via query parameters or request body since there is no
authentication layer.
"""

from flask import Blueprint, request, jsonify

import datetime

from ..models import db, Guide, UserGuideProgress


guide_bp = Blueprint('guide', __name__)


@guide_bp.route('/guides', methods=['GET'])
def list_guides() -> tuple:
    """Return a list of all guides."""
    guides = Guide.query.all()
    return jsonify([guide.to_dict() for guide in guides]), 200


@guide_bp.route('/guides/<int:guide_id>', methods=['GET'])
def get_guide(guide_id: int) -> tuple:
    """Return details of a specific guide."""
    guide = Guide.query.get(guide_id)
    if not guide:
        return jsonify({'error': 'Guide not found'}), 404
    return jsonify(guide.to_dict()), 200


@guide_bp.route('/guides/progress', methods=['GET'])
def get_progress() -> tuple:
    """Return progress for a user across all guides."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id query parameter is required'}), 400
    progress_records = UserGuideProgress.query.filter_by(user_id=user_id).all()
    return jsonify([record.to_dict() for record in progress_records]), 200


@guide_bp.route('/guides/<int:guide_id>/steps/<int:step_index>/complete', methods=['POST'])
def complete_step(guide_id: int, step_index: int) -> tuple:
    """Mark a specific step in a guide as completed for a user."""
    data = request.get_json() or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required in request body'}), 400
    guide = Guide.query.get(guide_id)
    if not guide:
        return jsonify({'error': 'Guide not found'}), 404
    # Find or create progress record
    progress = UserGuideProgress.query.filter_by(user_id=user_id, guide_id=guide_id).first()
    if not progress:
        progress = UserGuideProgress(user_id=user_id, guide_id=guide_id, completed_steps=[])
        db.session.add(progress)
    # Convert to int to ensure indexing
    steps_list = guide.steps or []
    if step_index < 0 or step_index >= len(steps_list):
        return jsonify({'error': 'Invalid step index'}), 400
    # Mark step as completed if not already
    completed_steps = progress.completed_steps or []
    if step_index not in completed_steps:
        completed_steps.append(step_index)
        progress.completed_steps = completed_steps
        # Mark as completed if all steps are done
        if len(completed_steps) == len(steps_list):
            progress.completed = True
            progress.completed_at = progress.completed_at or datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(progress.to_dict()), 200