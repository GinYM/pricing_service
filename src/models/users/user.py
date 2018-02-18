import uuid

import datetime

import src.models.users.errors as UserErrors
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.constants as UserConstants
from src.models.alerts.alert import Alert
from src.models.blogs.blog import Blog


class User(object):
    def __init__(self,  email, password, _id=None, binding=None, user_name=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
        self.binding = [] if binding is None else binding
        self.user_name = "" if user_name is None else user_name

    def __repr__(self):
        return "<User {}>".format(self.email)

    def add_binding(self,binding_email):
        if binding_email not in self.binding:
            self.binding.append(binding_email)
            self.save_to_db()

    @staticmethod
    def is_login_valid(email, password):
        user_data = Database.find_one(collection=UserConstants.COLLECTION, query={'email': email})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(user_name,email,password):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if Database.find_one(UserConstants.COLLECTION,{'user_name':user_name}) is not None:
            raise UserErrors.UserAlreadyRegisteredError("The user name already exists.")
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The email already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email format is invalid.")
        if not Utils.user_name_is_valid(user_name):
            raise UserErrors.InvalidUserNameError("The user name is invalid.")
        if not Utils.password_is_valid(password):
            raise UserErrors.InvalidPasswordError("The password format is invalid.")

        User(email= email,password= Utils.hash_password(password),user_name= user_name).save_to_db()
        return True

    def save_to_db(self):
        Database.update(collection=UserConstants.COLLECTION,criteria={'_id':self._id},objNew=self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "binding": self.binding,
            "user_name": self.user_name
        }

    @classmethod
    def find_by_id(cls,_id):
        result = Database.find_one(UserConstants.COLLECTION, {'_id':_id})
        if result is None:
            return None
        else:
            return cls(**result)

    @classmethod
    def find_by_email(cls,email):
        result = Database.find_one(UserConstants.COLLECTION,{'email': email})
        if result is None:
            return None
        else:
            return cls(**result)

    def get_alerts(self):
        return Alert.find_by_email(self.email)

    def new_blog(self, title, description, secret=0):
        blog = Blog(author=self.user_name,
                    title=title,
                    description=description,
                    author_id=self._id,
                    secret=secret)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        # title, content, date=datetime.datetime.utcnow()
        blog = Blog.get_from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)
