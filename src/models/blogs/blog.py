import uuid
import datetime
from src.models.blogs.post import Post
from src.common.database import Database
import src.models.blogs.constants as BlogsConstant

class Blog(object):
    def __init__(self, author, title, description, author_id,  _id=None, secret=0):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id
        self.secret = secret

    def new_post(self,title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    date=date)
        post.save_to_mongo()

    def get_post(self):
        return Post.from_blog(self._id)

    def json(self):
        return {
            "author": self.author,
            "title": self.title,
            "description": self.description,
            "author_id": self.author_id,
            "_id": self._id,
            "secret": self.secret
        }

    def save_to_mongo(self):
        Database.update(collection=BlogsConstant.COLLECTION, criteria={'_id':self._id},objNew=self.json())

    @classmethod
    def get_from_mongo(cls, _id):
        blog_data = Database.find_one(collection=BlogsConstant.COLLECTION, query={"_id": _id})
        if blog_data is not None:
            return cls(**blog_data)
        else:
            return None

    @classmethod
    def get_by_id(cls, _id):
        blog_data = Database.find_one(collection=BlogsConstant.COLLECTION, query={"_id": _id})
        if blog_data is not None:
            return cls(**blog_data)
        else:
            return None

    @classmethod
    def find_by_author_id(cls, author_id):
        blog_data = Database.find(collection=BlogsConstant.COLLECTION, query={"author_id": author_id})
        return [cls(**blog) for blog in blog_data]


