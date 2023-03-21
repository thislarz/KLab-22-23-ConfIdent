from bs4 import BeautifulSoup
import requests
from kgl_event_prediction.event import Event
from difflib import SequenceMatcher
import kgl_event_prediction.utils as ut

class EventEvaluator(object):
    """
    evaluator for Events
    """

    def __init__(self, event: Event):
        self.event = event

    @staticmethod
    def get_element_content_from_url(url: str, html_element: str, timeout: float = 5.0) -> str:
        """
        get the element content from the given url

        Args:
            url(str): the url to get the element content from
            html_element(str): the element to extract e.g. "title,h1,h2"

        Returns:
            Optional[str]: None or the element content
        """
        try:
            res = requests.get(url, timeout=timeout)
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

    @staticmethod
    def get_title_and_h2_from_url(url: str, timeout: float = 5.0):
        try:
            res = requests.get(url, timeout=timeout)
        except:
            return None, None
        event_page = BeautifulSoup(res.text, "html.parser")

        content = [event_page.title, event_page.h1]

        for i in range(0,len(content)):
            if content[i] is not None:
                content[i] = content[i].string
        return content

    def summarize_event(self, threshold : float = 0.80):
        title_threshold = threshold

        title_diff = 0
        year_check = False
        acronym_check = False
        verdict = "bad"

        acronym_stripped = ut.strip_acronym(self.event.acronym).lower()

        title, h1 = EventEvaluator.get_title_and_h2_from_url(self.event.homepage)
        title_diff = EventEvaluator.similarity(title, self.event.title)
        h1_diff = EventEvaluator.similarity(h1, self.event.title)

        if title is None and h1 is None or title == "" and h1 == "":
            return {
                "title_similarity": 0.0,
                "year_check": False,
                "acronym_check": False,
                "verdict": "not_found"
            }
        if title is None:
            title = ""
        if h1 is None:
            h1 = ""
        # check for acronym
        if title.lower().find(acronym_stripped) != -1 or h1.lower().find(acronym_stripped) != 1:
            acronym_check = True

        # check for year
        if title.find(str(self.event.year)) != -1 or h1.find(str(self.event.year)) != -1:
            year_check = True

        # choose entry that matches title more closely
        if title_diff < h1_diff:
            title = h1
            title_diff = h1_diff

        # choose action depending on title similarity
        if title_diff > title_threshold:
            verdict = "good"
        else:
            if acronym_check:
                verdict = "okay"
            elif year_check and acronym_check:
                verdict = "okay"
            else:
                verdict = "bad"

        # print("title: ", title)
        # print("pred_title:", self.event.title)
        summary = {
            "title_similarity": title_diff,
            "year_check": year_check,
            "acronym_check": acronym_check,
            "verdict": verdict
        }
        return summary

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

    @staticmethod
    def similarity(a: str, b: str):
        """
        :params a str: input that shall be compared to b
        :params b str: what a shall be compared against
        :return: The similarity between test and truth
        """
        if a is None or b is None:
            return 0
        diff = SequenceMatcher(a=a.lower(), b=b.lower()).ratio()
        return diff
