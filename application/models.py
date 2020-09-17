from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Asins(db.Model):
    __tablename__ = 'asins'

    id = db.Column(db.String(10), nullable=False, unique=True, primary_key=True)


class ProductInfo(db.Model):
    __tablename__ = 'product_info'

    id = db.Column(db.Integer, primary_key=True)
    asin_id = db.Column(db.ForeignKey('asins.id', ondelete='CASCADE'))
    name = db.Column(db.Text, nullable=False)
    ratings = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Numeric(1, 1), default=0)


class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    asin_id = db.Column(db.ForeignKey('asins.id', ondelete='CASCADE'))
    reviews_number = db.Column(db.Integer, nullable=False, default=0)
    positive_reviews_number = db.Column(db.Integer, nullable=False, default=0)
    answered_questions_number = db.Column(db.Text, nullable=False)
