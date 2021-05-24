from models.user import UserModel
from flask_restful import Resource
from flask import json, request, send_file, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os
from werkzeug.utils import secure_filename
from libs.upload_utils import FileLoadManager, FileStoreManager, UploadNotAllowed
from string_const.constants import (
    AVATAR_NOT_FOUND, 
    EXT_NOT_ALLOWED,
    GENERIC_ERROR, 
    IMAGE_DELETED, 
    IMAGE_ILLEGAL_FILENAME, 
    IMAGE_NOT_FOUND, 
    IMAGE_UPLOADED,
    USER_NOT_FOUND,
)


""" Image """

class ImageUpload(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """
        Upload image file
        """
        fm = FileStoreManager(request.files["image"])
        # FileStorage obj
        # 
        user_id = get_jwt_identity()
        try:
            fm.save_file(user_id, file_type="image")
            return make_response(jsonify(message=IMAGE_UPLOADED.format(fm.basename)), 201)
        except UploadNotAllowed as e:
            return make_response(jsonify(message=EXT_NOT_ALLOWED.format(fm.extension)), 400)



class Image(Resource):
    @classmethod
    @jwt_required()
    def get(cls, filename: str):
        """
        Return requested image for user if exists
        """
        user_id = get_jwt_identity()
        if not UserModel.find_by_id(user_id):
            return make_response(jsonify(message=USER_NOT_FOUND))

        file_loader = FileLoadManager(user_id, "image", filename)
        if not secure_filename(filename):
            return make_response(jsonify(message=IMAGE_ILLEGAL_FILENAME), 400)

        try:
            
            return make_response(jsonify(message=file_loader.load_file()))
            # return send_file(file_loader.load_file()), 200
        except FileNotFoundError:
            return make_response(jsonify(message=IMAGE_NOT_FOUND.format(filename)), 404)

    @classmethod
    @jwt_required()
    def delete(cls, filename: str):

        user_id = get_jwt_identity()
        file_loader = FileLoadManager(user_id, "image", filename)
        try: 
            path_delete = file_loader.load_file()
            os.remove(path_delete)
            return make_response(jsonify(message=IMAGE_DELETED.format(filename)), 200)
        except FileNotFoundError:
            return make_response(jsonify(message=IMAGE_NOT_FOUND.format(filename)), 404)
        except:
            traceback.print_exc()
            return make_response(jsonify(message=GENERIC_ERROR), 500)



class ImageList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        """
        Return requested image for user if exists
        """
        user_id = get_jwt_identity()
        file_loader = FileLoadManager(user_id, filetype="image")
        try:
            return make_response(jsonify(message=file_loader.load_file()), 200)
            #return send_file(file_loader.load_file())
        except FileNotFoundError:
            return make_response(jsonify(message=AVATAR_NOT_FOUND), 404)



""" Video """


class VideoUpload(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """
        Upload video file
        """
        fm = FileStoreManager(request.files["video"])
        # FileStorage obj
        # 
        user_id = get_jwt_identity()
        try:
            fm.save_file(user_id, file_type="video")
            return make_response(jsonify(message=IMAGE_UPLOADED.format(fm.basename)), 201)
        except UploadNotAllowed as e:
            return make_response(jsonify(message=EXT_NOT_ALLOWED.format(fm.extension)), 400)


class Video(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user_id = get_jwt_identity()
        file_loader = FileLoadManager(user_id, filetype="video")
        try:
            return make_response(jsonify(message=file_loader.load_file()), 200)
            #return send_file(file_loader.load_file())
        except FileNotFoundError:
            return make_response(jsonify(message=AVATAR_NOT_FOUND), 404)


class VideoList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        """
        Return each video for user if exists
        """
        user_id = get_jwt_identity()
        file_loader = FileLoadManager(user_id, filetype="video")
        try:
            return make_response(jsonify(message=file_loader.load_file()), 200)
            #return send_file(file_loader.load_file())
        except FileNotFoundError:
            return make_response(jsonify(message=AVATAR_NOT_FOUND), 404)


"""  Avatar """


class AvatarUpload(Resource):
    @classmethod
    @jwt_required()
    def put(cls):
        """
        Upload user avatar.
        Users have unique avatar.
        """
        user_id = get_jwt_identity()
        if not UserModel.find_by_id(user_id):
            return make_response(jsonify(message=USER_NOT_FOUND), 404)

        file_loader = FileLoadManager(user_id, filetype="avatar")
        
        try:
            avatar_path = file_loader.load_file()
            os.remove(avatar_path)
        except Exception:
            pass
            
        try:
            file_storage = FileStoreManager(request.files["avatar"])
            file_storage.save_file(user_id, "avatar")

            return make_response(jsonify(message=f"Uploaded {file_storage.basename}"), 200)
        except UploadNotAllowed:
            return make_response(jsonify(message=EXT_NOT_ALLOWED.format(file_storage.extension)), 400)


class Avatar(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user_id = get_jwt_identity()
        file_loader = FileLoadManager(user_id, filetype="avatar")
        try:
            return make_response(jsonify(message=file_loader.load_file()), 200)
            #return send_file(file_loader.load_file())
        except FileNotFoundError:
            return make_response(jsonify(message=AVATAR_NOT_FOUND), 404)


