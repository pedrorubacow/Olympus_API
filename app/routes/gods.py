from flask import Blueprint, request, jsonify
from app import db
from app.models import God

gods_bp = Blueprint('gods', __name__)

@gods_bp.route('/gods', methods=['GET'])
def list_gods():
    gods = God.query.all()
    return jsonify([g.to_dict() for g in gods])

@gods_bp.route('/gods/<int:god_id>', methods=['GET'])
def get_god(god_id):
    god = God.query.get_or_404(god_id)
    return jsonify(god.to_dict())

@gods_bp.route('/gods', methods=['POST'])
def create_god():
    data = request.get_json()
    god = God(
        name=data['name'],
        domain=data.get('domain'),
        symbol=data.get('symbol'),
        parent_id=data.get('parent_id'),
        spouse_id=data.get('spouse_id'),
    )
    db.session.add(god)
    db.session.commit()
    return jsonify(god.to_dict()), 201

@gods_bp.route('/gods/<int:god_id>', methods=['PUT'])
def update_god(god_id):
    god = God.query.get_or_404(god_id)
    data = request.get_json()
    for field in ['name', 'domain', 'symbol', 'parent_id', 'spouse_id']:
        if field in data:
            setattr(god, field, data[field])
    db.session.commit()
    return jsonify(god.to_dict())

@gods_bp.route('/gods/<int:god_id>', methods=['DELETE'])
def delete_god(god_id):
    god = God.query.get_or_404(god_id)
    db.session.delete(god)
    db.session.commit()
    return '', 204