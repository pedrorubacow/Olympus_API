from app import db

class God(db.Model):
    __tablename__ = 'gods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100))
    symbol = db.Column(db.String(100))
    parent_id = db.Column(db.Integer, db.ForeignKey('gods.id'), nullable=True)
    spouse_id = db.Column(db.Integer, db.ForeignKey('gods.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'symbol': self.symbol,
            'parent_id': self.parent_id,
            'spouse_id': self.spouse_id,
        }


class Creature(db.Model):
    __tablename__ = 'creatures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    powers = db.Column(db.Text)
    defeated_by = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'powers': self.powers,
            'defeated_by': self.defeated_by,
        }
myth_gods = db.Table('myth_gods',
    db.Column('myth_id', db.Integer, db.ForeignKey('myths.id'), primary_key=True),
    db.Column('god_id', db.Integer, db.ForeignKey('gods.id'), primary_key=True)
)

myth_creatures = db.Table('myth_creatures',
    db.Column('myth_id', db.Integer, db.ForeignKey('myths.id'), primary_key=True),
    db.Column('creature_id', db.Integer, db.ForeignKey('creatures.id'), primary_key=True)
)

class Myth(db.Model):
    __tablename__ = 'myths'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text)
    location = db.Column(db.String(100))

    gods = db.relationship('God', secondary=myth_gods, backref='myths')
    creatures = db.relationship('Creature', secondary=myth_creatures, backref='myths')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'location': self.location,
            'god_ids': [g.id for g in self.gods],
            'creature_ids': [c.id for c in self.creatures],
        }    