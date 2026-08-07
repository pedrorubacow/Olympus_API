from flask import Blueprint, request, jsonify
from app import db
from app.models import Myth, God, Creature

myths_bp = Blueprint('myths', __name__)

@myths_bp.route('/myths', methods=['GET'])
def list_myths():
    myths = Myth.query.all()
    return jsonify([m.to_dict() for m in myths])

@myths_bp.route('/myths/<int:myth_id>', methods=['GET'])
def get_myth(myth_id):
    myth = Myth.query.get_or_404(myth_id)
    return jsonify(myth.to_dict())

@myths_bp.route('/myths', methods=['POST'])
def create_myth():
    data = request.get_json()
    myth = Myth(
        title=data['title'],
        summary=data.get('summary'),
        location=data.get('location'),
    )
    myth.gods = God.query.filter(God.id.in_(data.get('god_ids', []))).all()
    myth.creatures = Creature.query.filter(Creature.id.in_(data.get('creature_ids', []))).all()
    db.session.add(myth)
    db.session.commit()
    return jsonify(myth.to_dict()), 201

@myths_bp.route('/myths/<int:myth_id>', methods=['PUT'])
def update_myth(myth_id):
    myth = Myth.query.get_or_404(myth_id)
    data = request.get_json()
    for field in ['title', 'summary', 'location']:
        if field in data:
            setattr(myth, field, data[field])
    if 'god_ids' in data:
        myth.gods = God.query.filter(God.id.in_(data['god_ids'])).all()
    if 'creature_ids' in data:
        myth.creatures = Creature.query.filter(Creature.id.in_(data['creature_ids'])).all()
    db.session.commit()
    return jsonify(myth.to_dict())

@myths_bp.route('/myths/<int:myth_id>', methods=['DELETE'])
def delete_myth(myth_id):
    myth = Myth.query.get_or_404(myth_id)
    db.session.delete(myth)
    db.session.commit()
    return '', 204