from models.user import UserModel
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from db import db
from ma import ma
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from resources.user import (
    UserResource,
    UserRegister,
    UserLogin,
    UserLogout
)
from resources.media import (
    ImageUpload,
    Image,
    ImageList,
    VideoUpload,
    Video,
    VideoList,
    AvatarUpload,
    Avatar
)


from marshmallow import ValidationError
from config import SimpleTestConfig


app = Flask(__name__)
app.config.from_object(SimpleTestConfig)

# enable cors
CORS(app)

# api
api = Api(app)

# sqlalchemy
db.init_app(app)

# marshmallow 
ma.init_app(app)

# migrate
migrate = Migrate(app, db)

# app.config['JWT_SECRET_KEY']
jwt = JWTManager(app) 


# create table
@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({
        'description': "Signature verification failed",
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({
        'description': "Token jwt required",
        'error': "missing_token"
    }), 401


api.add_resource(UserRegister, '/register/')
api.add_resource(UserLogin, '/login/')
api.add_resource(UserLogout, '/logout/')
api.add_resource(UserResource, '/user/<string:username>/')
api.add_resource(VideoUpload, '/upload_video/')
api.add_resource(Video, '/video/<string:filename>/')
api.add_resource(VideoList, '/videos/')
api.add_resource(ImageUpload, '/upload_image/')
api.add_resource(Image, '/image/<string:filename>/')
api.add_resource(ImageList, '/images/')
api.add_resource(AvatarUpload, '/upload_avatar/')
api.add_resource(Avatar, '/avatar/')


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile/")
def profile():
    return render_template("profile.html")
     



if __name__ == '__main__':
    app.run(port=5000, debug=True)