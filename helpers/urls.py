import json

class URLs():
    def __init__(self, platform: str):
        self.__dict__ = json.load(open('./helpers/urls.json'))[platform]
