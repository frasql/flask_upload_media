from models.user import UserModel
from ma import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password", "id")
        dump_only = ("email", "firstname", "lastname")
        load_instance = True