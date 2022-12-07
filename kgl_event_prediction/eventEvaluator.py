from bs4 import BeautifulSoup
import requests
from kgl_event_prediction.event import Event


class EventEvaluator(object):

    def __init__(self, event: Event):
        self.event = event

    @staticmethod
    def get_title_from_url(url):
        res = requests.get(url)
        event_page = BeautifulSoup(res.text, "html.parser")
        event_name = event_page.title  # returns first element with the tag title
        return event_name.string

    def is_title_valid(self):
        if self.event.homepage is None or self.event.homepage == "":
            return False
        else:
            try:
                web_title = self.get_title_from_url(self.event.homepage)
            except:
                return False
            if web_title is None or web_title == "":
                return False
            elif self.event.title.find(web_title) != -1 or web_title.find(self.event.title) != -1:
                return True
