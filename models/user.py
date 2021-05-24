from db import db
from ma import ma



class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column("username", db.String(100), nullable=False, unique=True)
    firstname = db.Column("firstname", db.String(100), nullable=False)
    lastname = db.Column("lastname", db.String(100), nullable=False)
    email = db.Column("email", db.String(100), nullable=False, unique=True)
    password = db.Column("password", db.String(100), nullable=False)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.remove(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, value):
        return cls.query.filter_by(id=value).first()

    @classmethod
    def find_by_username(cls, value):
        return cls.query.filter_by(username=value).first()