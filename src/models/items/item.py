import uuid

import requests
from bs4 import BeautifulSoup
import re
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = float(price) if price is not None else None
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()
        pattern = re.compile("\d+\.?\d*")
        match = pattern.search(string_price).group()
        self.price = float(match)
        self.update_mongo()
        return self.price

    def save_to_mongo(self):
        Database.insert(ItemConstants.COLLECTION, self.json())

    def update_mongo(self):
        Database.update(ItemConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "price": self.price,
            "_id": self._id,
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": _id}))
