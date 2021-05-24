from flask import json, request, make_response, render_template, jsonify
from flask_jwt_extended.utils import get_jti
from blacklist import BLACKLIST
from flask_restful import Resource
from werkzeug.security import safe_str_cmp, check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jti,
    get_jwt
)

from string_const.constants import *
from marshmallow import ValidationError
from models.user import UserModel
from schemas.user import UserSchema


user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


class UserRegister(Resource):
    @classmethod
    def post(cls):
        # get data from request to schema

        user_json = request.get_json(force=True)
        # propogate exception
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return make_response(jsonify(message=NAME_ALREADY_EXISTS.format(user.username)), 400)

        try:
            # passwd_hash = generate_password_hash(user.password)
            user.save_to_db()
        except Exception as e:
            return make_response(jsonify(message=ERROR_INSERTING), 500)

        return make_response(jsonify(message=USER_CREATED), 201)


class UserResource(Resource):
    @classmethod
    @jwt_required()
    def get(cls, user_id: str):
        user = UserModel.find_by_id(value=user_id)
        if not user:
            return make_response(jsonify(message=USER_NOT_FOUND), 404)
        #return user_schema.dump(user), 200
        return user_schema.dump(user), 201


    @classmethod
    @jwt_required()
    def delete(cls, username: int):
        user = UserModel.find_by_username(username)
        if not user:
            return make_response(jsonify(message=USER_NOT_FOUND), 404)
        user.delete_from_db()
        return make_response(jsonify(message=USER_DELETED), 200)


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from request to schema
        user_json = request.get_json(force=True)
        # propogate exception
        user_data = user_schema.load(user_json)
        # find user in db
        user = UserModel.find_by_username(user_data.username)

        # check password -> `authenticate()`
        #passwd = check_password_hash(user_data.password)
        if user and safe_str_cmp(user_data.password, user.password):
            # mail confirm
            #if not user.activated:
            # add claims to jwt
            additional_claims = {"logged_in": True}
            # create access token -> `identity()`
            jwt_access_token = create_access_token(
                identity=user.id, 
                fresh=True, 
                additional_claims=additional_claims
                )
            # create refresh token
            jwt_refresh_token = create_refresh_token(user.id)
            return make_response(
                jsonify(
                    access_token=jwt_access_token,
                    refresh_token=jwt_refresh_token,
                    ), 200)
        return make_response(jsonify(message=INVALID_CREDENTIALS), 401)


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jti() # jwt id
        BLACKLIST.add(jti)
        user_id = get_jwt_identity() 
        return make_response(jsonify(message=USER_LOGOUT.format(user_id)), 200)


class UserProfile(Resource):
    @jwt_required()
    @classmethod
    def get(cls):
        user = UserModel.find_by_id(get_jwt_identity())
        if user:
            jwt_claims = get_jwt()

            if jwt_claims["logged_in"]:
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template("profile.html", user_id=user.id), 200, headers)
            else:
                return make_response(jsonify(message=LOGIN_REQUIRED))
        else:
            return make_response(jsonify(message=USER_NOT_FOUND), 200)
        
