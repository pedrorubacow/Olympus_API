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