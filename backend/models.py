from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User model (Skeleton)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Expert model (Skeleton)
class Expert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)

# Skincare Concern model (Skeleton)
class SkincareConcern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    concern_details = db.Column(db.String(500), nullable=False)

if __name__ == "__main__":
    db.create_all()  # Creates database tables (run only once)
