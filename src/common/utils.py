from passlib.hash import pbkdf2_sha512
import re


class Utils(object):

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile(r'^[\w-]+@([\w-]+)+\.[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def password_is_valid(password):
        if len(password)<6:
            return False
        password_address_matcher = re.compile(r'^[\w\.\!\@\#\$\%\^\&\*]+$')
        return True if password_address_matcher.match(password) else False

    @staticmethod
    def user_name_is_valid(user_name):
        user_name_matcher = re.compile(r'^[\w\_]+$')
        return True if user_name_matcher.match(user_name) else False

