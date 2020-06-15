from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
db = SQLAlchemy()

@dataclass
class FakeBinWeight(db.Model):
    id: int
    bin_id : str
    weight : int
    created_at : str
    updated_at : str

    __tablename__ = 'fake_bins_weight'
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    bin_id = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    weight = db.Column(
        db.Integer
    )

    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def __repr__(self):
        return '<FakeBinWeight {}>'.format(self.bin_id)