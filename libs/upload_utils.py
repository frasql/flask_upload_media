import re
import os
from werkzeug.datastructures import FileStorage
from pathlib import Path
from typing import Union


# Application base directory 
BASEDIR = Path(__name__).resolve().parent


class FileNameError(Exception):
    """ Specific exception for filename error """


class FileTypeError(Exception):
    """ Specific exception for file_type error """


class UploadNotAllowed(Exception):
    """ Specific exception for not allowed file error """


class FileStoreManager(object):
    """ Object Manager for werkzeug.datastructures.FileStorage """

    
    """ Path stores images """
    
    
    path_upload_image = "static/images/user_{}"
    # absolute path store images
    UPLOAD_IMAGE = os.path.join(BASEDIR, path_upload_image)

    
    """ Path stores videos """
    
    
    path_upload_video = "static/videos/user_{}"
    # absolute path store videos
    UPLOAD_VIDEO = os.path.join(BASEDIR, path_upload_video)

    
    """ Path stores avatars """
    
    
    path_upload_avatar = "static/avatars/user_{}"
    # absolute path store avatars
    UPLOAD_AVATAR = os.path.join(BASEDIR, path_upload_avatar)


    """ Path stores unknown file """
    
    
    path_upload_unknown = "static/unknown/user_{}"
    # absolute path store avatars
    UPLOAD_UNKNOWN = os.path.join(BASEDIR, path_upload_unknown)


    """ Allowed formats """


    # allowed format for images
    IMAGE_FORMAT = tuple("jpg png".split())
    # allowed format for videos
    VIDEO_FORMAT = tuple("mp4 avi".split())
    # each format allowed
    ALL_FORMAT = tuple("txt csv xlsx json jpg png mp3 mp4 pdf".split())

    """ Allowed file_type """

    allowed_file_type = tuple("image video avatar".split())


    def __init__(self, file_obj: FileStorage):
        assert isinstance(file_obj, FileStorage)
        try:
            FileStoreManager.is_filename_safe(file_obj.filename)
            self.file_obj = file_obj
        except:
            raise FileNameError("File not allowed")
        


    @staticmethod
    def is_filename_safe(filename: str) -> bool:
        """ Check regex and return if the string matches or not """
        allowed_format = "|".join(FileStoreManager.ALL_FORMAT) # png|svg|jpg
        regex = f"[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
        return re.match(regex, filename) is not None

    """
    Property of a FileStorage: filename, basename, file extension
    """


    @property
    def obj_name(self) -> Union[str, None]:
        if isinstance(self.file_obj, FileStorage):
            return self.file_obj.filename
        return self.file_obj

    @property
    def basename(self) -> str:
        filename = self.obj_name
        return os.path.splitext(filename)[0]

    @property
    def extension(self) -> str:
        extension = self.obj_name
        return os.path.splitext(extension)[1]
        

    @staticmethod
    def get_path(filename: str, folder: str=None) -> str:
        assert folder is not None
        return os.path.join(folder, filename)


    def _build_abs_path_image(self, user_id):
        image_path = os.path.join(self.UPLOAD_IMAGE.format(user_id))
        if os.path.isdir(image_path):
            return image_path
        else:
            image_path = os.makedirs(image_path)
            return image_path

    def _build_abs_path_video(self, user_id):
        video_path = os.path.join(self.UPLOAD_VIDEO.format(user_id))
        if os.path.isdir(video_path):
            return video_path
        else:
            video_path = os.makedirs(video_path)
            return video_path

    def _build_abs_path_avatar(self, user_id):
        avatar_path = os.path.join(self.UPLOAD_AVATAR.format(user_id))
        if os.path.isdir(avatar_path):
            return avatar_path
        else:
            avatar_path = os.makedirs(avatar_path)
            return avatar_path

    def _build_abs_path_unknown(self, user_id):
        unknown_path = os.path.join(self.UPLOAD_AVATAR.format(user_id))
        if os.path.isdir(unknown_path):
            return unknown_path
        else:
            unknown_path = os.makedirs(unknown_path)
            return unknown_path


    def choose_filetype_path(self, user_id, filetype):
        if filetype == "image":
            return self._build_abs_path_image(user_id)
        elif filetype == "video":
            return self._build_abs_path_video(user_id) 
        elif filetype == "avatar":
            return self._build_abs_path_avatar(user_id) 
        elif filetype == "unknown":
            return self._build_abs_path_unknown(user_id) 
        else:
            raise FileTypeError


    def save_file(self, user_id: int, file_type: str="unknown") -> str:
        
        file_type = file_type.lower()

        store_file_path = self.choose_filetype_path(user_id, file_type)
        # save method FileStorage
        return self.file_obj.save(os.path.join(store_file_path, self.obj_name))


    def get_file_storage(self) -> FileStorage:
        return self.file_obj


    def __repr__(self) -> str:
        return f"{self.file_obj}"



class FileLoadManager(object):

    """ Object Manager for loading files """

    
    """ Path stores images """
    
    
    path_dir_image = "static/images/user_{}"
    # absolute path store images
    #IMAGE_DIR = os.path.join(BASEDIR, path_dir_image)

    
    """ Path stores videos """
    
    
    path_dir_video = "static/videos/user_{}"
    # absolute path store videos
    #VIDEO_DIR = os.path.join(BASEDIR, path_dir_video)

    
    """ Path stores avatars """
    
    
    path_dir_avatar = "static/avatars/user_{}"
    # absolute path store avatars
    #AVATAR_DIR = os.path.join(BASEDIR, path_dir_avatar)


    """ Path stores unknown file """
    
    
    path_dir_unknown = "static/unknown/user_{}"
    # absolute path store avatars
    #UNKNOWON_DIR = os.path.join(BASEDIR, path_upload_unknown)

    filename = None

    def __init__(self, user_id: int, filetype: str, filename: str= None) -> None:
        self.user_id = user_id
        self.filetype = filetype
        
        if filename != None:
            self.filename = filename

    
    def _retireve_directory(self):
        if self.filetype == "image":
            return self.path_dir_image.format(self.user_id)
        elif self.filetype == "video":
            return self.path_dir_video.format(self.user_id)
        elif self.filetype == 'avatar':
            return self.path_dir_avatar.format(self.user_id)
        else:
            return self.path_dir_unknown.format(self.user_id)

    def _build_path_loader(self):
        path_to_load = self._retireve_directory()
        if self.filename is not None:
            return os.path.join(path_to_load, self.filename)
        else:
            files = os.listdir(path_to_load)
            return files
        

    def load_file(self):
        try:
            return self._build_path_loader()
        except:
            raise FileNotFoundError()

