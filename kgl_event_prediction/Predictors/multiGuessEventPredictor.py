from kgl_event_prediction.Evaluator.eventEvaluator import EventEvaluator
from kgl_event_prediction.Predictors.eventPredictor import EventPredictor
from kgl_event_prediction.db_util import DbUtil
from kgl_event_prediction.event import Event
from kgl_event_prediction.utils import *


class MultiGuessEventPredictor(EventPredictor):

    def __init__(self):
        super().__init__()
        self.last_event = None
        self.next_event = None
        self.next_year = 0

    def initialize(self, series_id: str = "", acronym: str = ""):
        """
        is initialized by passing an acronym of a conference
        """
        # loads event by acronym
        db = DbUtil(table="event_orclone")
        event = db.get_event_by_acronym(acronym=acronym)

        # updates the class attributes
        self.last_event = event
        self.next_year = self.get_anticipated_next_year()
        self.next_event = self.predict_next_event(self.last_event, self.next_year)

    def predict_next_event(self, proceeding: Event, next_year: int):
        """
        is exactly copied from simpleEventPredictor modified with int casts
        """
        title = ""
        homepage = ""
        year = ""
        acronym = ""

        preceding_year = str(proceeding.year)
        year = str(next_year)

        try:
            title = proceeding.title.replace(preceding_year, year)
        except:
            title = ""

        try:
            homepage = proceeding.homepage.replace(preceding_year, year)
            if homepage == proceeding.homepage:
                diff = int(year) - int(preceding_year)
                for x in range(diff):
                    homepage = number_increase_in_string(proceeding.homepage)
        except ValueError:
            print(homepage, "this is homepage")
            homepage = ""

        try:
            acronym = proceeding.acronym.replace(preceding_year, year)
            if acronym == proceeding.acronym:
                diff = int(year) - int(preceding_year)
                for x in range(diff):
                    acronym = number_increase_in_string(proceeding.acronym)
        except:
            acronym = ""

        anticipated_event = Event(title=title, homepage=homepage, year=year, acronym=acronym)

        return anticipated_event

    def get_next_event(self):
        return self.next_event

    def get_last_event(self):
        return self.last_event

    def get_anticipated_next_year(self):
        # naive increment by one approach
        return self.last_event.year + 1

    def get_summery(self):
        event_evaluator = EventEvaluator(self.next_event)

        title = event_evaluator.get_element_content_from_url(self.next_event.homepage, "title")
        # find = title.find(self.next_event.title)
        print("webtitle :", title, "event_title: ", self.next_event.title.lower())

        if event_evaluator.is_element_valid("title") or event_evaluator.is_element_valid(
                "h1") or event_evaluator.is_element_valid("h2"):
            return True
        else:
            return False


if __name__ == "__main__":
    mgep = MultiGuessEventPredictor()
    mgep.initialize(acronym="AAMAS 2016")
    print(mgep.get_last_event(), "last")
    print(mgep.get_next_event(), "next")
    print(mgep.get_summery())
