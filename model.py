from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AIRecords(db.Model):
    _tablename_ = 'AIRecords'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True)
    description = db.Column(db.String)
    field = db.Column(db.String)
    expectation = db.Column(db.String)
    performance_rate = db.Column(db.Float)
    personaldata = db.Column(db.String)  ## personal data
    price = db.Column(db.String)
    task = db.Column(db.String)

    def __repr__(self):
        return '<AI tool %r>' % self.id
