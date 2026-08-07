from flask import Blueprint, request, jsonify
from app import db
from app.models import Creature

creatures_bp = Blueprint('creatures', __name__)

@creatures_bp.route('/creatures', methods=['GET'])
def list_creatures():
    creatures = Creature.query.all()
    return jsonify([c.to_dict() for c in creatures])

@creatures_bp.route('/creatures/<int:creature_id>', methods=['GET'])
def get_creature(creature_id):
    creature = Creature.query.get_or_404(creature_id)
    return jsonify(creature.to_dict())

@creatures_bp.route('/creatures', methods=['POST'])
def create_creature():
    data = request.get_json()
    creature = Creature(
        name=data['name'],
        type=data.get('type'),
        powers=data.get('powers'),
        defeated_by=data.get('defeated_by'),
    )
    db.session.add(creature)
    db.session.commit()
    return jsonify(creature.to_dict()), 201

@creatures_bp.route('/creatures/<int:creature_id>', methods=['PUT'])
def update_creature(creature_id):
    creature = Creature.query.get_or_404(creature_id)
    data = request.get_json()
    for field in ['name', 'type', 'powers', 'defeated_by']:
        if field in data:
            setattr(creature, field, data[field])
    db.session.commit()
    return jsonify(creature.to_dict())

@creatures_bp.route('/creatures/<int:creature_id>', methods=['DELETE'])
def delete_creature(creature_id):
    creature = Creature.query.get_or_404(creature_id)
    db.session.delete(creature)
    db.session.commit()
    return '', 204