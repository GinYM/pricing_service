import re
import urllib2

import requests
from bs4 import BeautifulSoup
import re
import datetime
import time

from src.models.stores.store import Store
from src.models.items.item import Item
from src.common.database import Database

#Database.initialize()
#
# s = Store("Adidas", "https://www.adidas.com.cn/", "span", {"class": "goods-price price-single"})
#
# s.save_to_mongo()
#
# i = Item(s.name, "https://www.adidas.com.cn/item/CQ2475")
# p = i.load_price()
# result = Database.count("items", {"_id": "252ea1b122eb405db6efe61e88325703"})


result = time.localtime()
print time.strftime("%m-%d-%Y %H:%M:%S", result)