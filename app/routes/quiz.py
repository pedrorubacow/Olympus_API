import random
from flask import Blueprint, jsonify, request
from app.models import God, Creature, Myth

quiz_bp = Blueprint('quiz', __name__)

def build_god_domain_question(gods):
    god = random.choice(gods)
    distractor_pool = list({g.domain for g in gods if g.domain and g.domain != god.domain})
    distractors = random.sample(distractor_pool, min(3, len(distractor_pool)))
    options = distractors + [god.domain]
    random.shuffle(options)
    return {
        'question': f"Qual é o domínio de {god.name}?",
        'options': options,
        'answer': god.domain,
    }

def build_creature_hero_question(creatures):
    creature = random.choice(creatures)
    distractor_pool = list({c.defeated_by for c in creatures if c.defeated_by and c.defeated_by != creature.defeated_by})
    distractors = random.sample(distractor_pool, min(3, len(distractor_pool)))
    options = distractors + [creature.defeated_by]
    random.shuffle(options)
    return {
        'question': f"Quem derrotou {creature.name}?",
        'options': options,
        'answer': creature.defeated_by,
    }

def build_myth_location_question(myths):
    myth = random.choice(myths)
    distractor_pool = list({m.location for m in myths if m.location and m.location != myth.location})
    distractors = random.sample(distractor_pool, min(3, len(distractor_pool)))
    options = distractors + [myth.location]
    random.shuffle(options)
    return {
        'question': f"Onde se passa o mito '{myth.title}'?",
        'options': options,
        'answer': myth.location,
    }

@quiz_bp.route('/quiz', methods=['GET'])
def get_quiz():
    count = request.args.get('count', default=5, type=int)
    gods = God.query.filter(God.domain.isnot(None)).all()
    creatures = Creature.query.filter(Creature.defeated_by.isnot(None)).all()
    myths = Myth.query.filter(Myth.location.isnot(None)).all()

    builders = []
    if len(gods) >= 2:
        builders.append(lambda: build_god_domain_question(gods))
    if len(creatures) >= 2:
        builders.append(lambda: build_creature_hero_question(creatures))
    if len(myths) >= 2:
        builders.append(lambda: build_myth_location_question(myths))

    if not builders:
        return jsonify({'error': 'Dados insuficientes para gerar quiz. Cadastre mais registros.'}), 400

    questions = [random.choice(builders)() for _ in range(count)]
    return jsonify(questions)