 
# Flask Media Upload

## About

* Flask application that allows registered users to store their media content. 
* Upload media files with OOP alternative to flask_upload.


## Installation

* pip3 install -r /path/to/requirements.txt



## Usage

* Default folder --> [images, videos, avatars, unknown]
* Defined in upload_files/libs/upload_utils:
```
FileStoreManager --> object that allows to get properties and save werkzeug.FileStorage object.
FileLoadManager --> object that allows to load a stored media file 
```


### Content

* User register / login / logout --> flask_jwt_extended
* User model --> flask_sqlalchemy
* Serialization / Deserialization --> flask_marshmallow
* Database Migration --> flask_migrate
* RESTful implementation --> flask_restful
* Cors allowed --> flask_cors


### Future Implementation

* Frontend in pure javascript
* User profile with javascript and jwt_extended


### Testing

* Test folder: postman_collection
* Create your own jwt token, store it in a postman environment variable and test the API!!




    
    