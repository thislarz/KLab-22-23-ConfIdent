from bs4 import BeautifulSoup
import requests
from kgl_event_prediction.event import Event


class EventEvaluator(object):

    def __init__(self, event: Event):
        self.event = event

    @staticmethod
    def get_element_content_from_url(url, html_element):
        try:
            res = requests.get(url, timeout=10.0)
        except:
            return None
        event_page = BeautifulSoup(res.text, "html.parser")

        element_content = None

        if html_element == "title":
            element_content = event_page.title  # returns first element with the tag title
        elif html_element == "h1":
            element_content = event_page.h1
        elif html_element == "h2":
            element_content = event_page.h2

        if element_content is None:
            return None

        element_content = element_content.string

        if element_content is None:
            return None

        return element_content.lower()

    def is_element_valid(self, html_element):
        if self.event.homepage is None or self.event.homepage == "":
            return False

        element_content = self.get_element_content_from_url(self.event.homepage, html_element)

        if element_content is None or element_content == "":
            return False

        if self.event.title.lower().find(element_content) != -1 or element_content.find(self.event.title) != -1:
            return True

        if self.event.acronym.lower().find(element_content) != -1 or element_content.find(self.event.acronym) != -1:
            return True
