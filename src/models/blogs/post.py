import uuid
import datetime

import pymongo

from src.common.database import Database
import src.models.blogs.constants_post as PostConstant


class Post(object):
    def __init__(self, blog_id, title, content, author, date=datetime.datetime.utcnow(), _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.author = author
        self.blog_id = blog_id
        self.title = title
        self.content = self.replace_newline(content)
        self.date = date

    @staticmethod
    def replace_newline(content):
        #return content.replace("\r\n", "</p><p>")
        return content

    @staticmethod
    def reverse_replace_newline(content):
        #return content.replace("</p><p>","\r\n")
        return content

    def save_to_mongo(self):
        Database.update(collection=PostConstant.COLLECTION, criteria={"_id":self._id},objNew=self.json())

    def json(self):
        return {
            "_id": self._id,
            "author": self.author,
            "blog_id": self.blog_id,
            "title": self.title,
            "content": self.content,
            "date": self.date
        }

    @classmethod
    def from_mongo(cls, _id):
        post = Database.find_one(collection=PostConstant.COLLECTION, query={"_id": _id})
        return cls(**post)

    @classmethod
    def from_blog(cls,blog_id):
        posts = Database.find(collection=PostConstant.COLLECTION, query={"blog_id": blog_id}).sort('date',pymongo.ASCENDING)
        return [cls(**post) for post in posts]


