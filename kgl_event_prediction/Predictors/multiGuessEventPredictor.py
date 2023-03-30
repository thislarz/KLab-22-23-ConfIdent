from datetime import datetime

from kgl_event_prediction.Evaluator.eventEvaluator import EventEvaluator
from kgl_event_prediction.Predictors.eventPredictor import EventPredictor
from kgl_event_prediction.db_util import DbUtil
from kgl_event_prediction.event import Event
from kgl_event_prediction.utils import *


class MultiGuessEventPredictor(EventPredictor):

    def __init__(self, series_list = [], earliest_year=None, prediction_iterations : int = 5):
        super().__init__()
        self.prediction_iterations = prediction_iterations
        self.initialize(series_list, earliest_year)

    def initialize(self, series_list, earliest_year = None):
        """
        :param series_list: list of Events from a given Series for which the next shall be guessed;
        :param earliest_year: doesn't do anything just for show so far
        This method should be used when the guess should be performed on a new series
        """
        self.earliest_year = datetime.now().year if earliest_year is None else earliest_year
        self.series_list = series_list

        # updates the class attributes
        if len(self.series_list) >= 1:
            self.last_event = series_list[0]
            self.next_year = self.get_anticipated_next_year()
            self.next_event = self.predict_next_event(self.last_event, self.next_year)
        else:
            self.last_event = Event()
            self.next_year = 0
            self.next_event = Event()

    def predict_next_event(self, proceeding: Event, first_anticipated_year: int):
        """
        @params proceeding: is the Event for which the next Event should be predicted
        """
        temp = proceeding
        if temp.homepage == '':
            return None

        iteration = 0
        res_event_list = []
        while iteration < self.prediction_iterations:
            # print("Iteration: ", iteration)
            # predict event for iteration
            predicted_event = self.predict_primitive_next_event(temp, first_anticipated_year+iteration)
            iteration += 1

            # evaluate summary of event
            summary = EventEvaluator(predicted_event).summarize_event()
            if summary['verdict'] == "good" and summary['year_check']:
                return predicted_event
            else:
                res_event_list.append((predicted_event, summary))

        largest_similarity = 0
        candidate, s = res_event_list[0]
        for pred_event, summary in res_event_list:
            if largest_similarity < summary['title_similarity']:
                largest_similarity = summary['title_similarity']
                candidate = pred_event

        return candidate

    def predict_primitive_next_event(self, proceeding: Event, next_year: int):
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
        except ValueError and AttributeError:
            # print(homepage, "this is homepage")
            homepage = ""

        try:
            acronym = proceeding.acronym.replace(preceding_year, year)
            if acronym == proceeding.acronym:
                diff = int(year) - int(preceding_year)
                for x in range(diff):
                    acronym = number_increase_in_string(proceeding.acronym)
        except:
            acronym = ""

        anticipated_event = Event(title=title, homepage=homepage, year=int(year), acronym=acronym)

        return anticipated_event

    def get_predicted_event(self):
        return self.next_event

    def get_last_event(self):
        return self.last_event

    def get_anticipated_next_year(self):
        # naive increment by one approach
        return self.last_event.year + 1

    @staticmethod
    def get_summery_of_event(event: Event):
        event_evaluator = EventEvaluator(event)

        title = event_evaluator.get_element_content_from_url(event.homepage, "title")
        # find = title.find(event.title)
        # print("webtitle :", title, "event_title: ", event.title.lower())

        if event_evaluator.is_element_valid("title") or event_evaluator.is_element_valid(
                "h1") or event_evaluator.is_element_valid("h2"):
            return True
        else:
            return False


if __name__ == "__main__":
    db = DbUtil("event_orclone")
    event_list = db.get_series_by_acronym('AAAI')
    mgep = MultiGuessEventPredictor(event_list)
    print(mgep.get_last_event(), "last")
    print(mgep.get_predicted_event(), "next")
    print(mgep.get_summery())
