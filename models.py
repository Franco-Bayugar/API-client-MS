from flask_login import UserMixin
from app import db

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False, unique=False)
    surname = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(255), nullable=True, unique=False)
    phone = db.Column(db.String(55), nullable=False, unique=False)
    address = db.Column(db.String(100), nullable=False, unique=False)
    
    def as_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'surname': self.surname,
            'email': self.email,
            'phone': self.phone,
            'address': self.address
        }