import uuid
import src.models.stores.constants as StoreConstants
from src.common.database import Database
import src.models.stores.errors as StoreErrors


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(StoreConstants.COLLECTION, {"_id": _id})
        return cls(**data)

    def save_to_mongo(self):
        if Database.count(StoreConstants.COLLECTION, {"_id": self._id}) == 0:
            Database.insert(StoreConstants.COLLECTION, self.json())
        else:
            Database.update(StoreConstants.COLLECTION, {"_id": self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        data = Database.find_one(StoreConstants.COLLECTION, {"name": store_name})
        return cls(**data)

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        data = Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}})
        if data is not None:
            return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))
        else:
            return None

    @classmethod
    def find_by_url(cls, url):
        pre = None
        for i in range(1, len(url)+1):
            store = Store.get_by_url_prefix(url[:i])
            if store is not None:
                pre = store
            elif pre is None:
                raise StoreErrors.StoreNotFoundException("The URL prefix used to find the store didn't give us any results!")
            else:
                return pre
        return pre

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {"_id": self._id})
