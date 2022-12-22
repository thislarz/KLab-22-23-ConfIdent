from kgl_event_prediction.eventEvaluator import EventEvaluator
from kgl_event_prediction.eventPredictor import EventPredictor
from kgl_event_prediction.utils import *
from kgl_event_prediction.event import Event
from search_engine_parser.core.engines.google import Search as GoogleSearch


class SearchingEventPredictor(EventPredictor):
    """
    Simple Event Predictor is used to guess events of a series
    """
    def __init__(self):
        super().__init__()
        self.series_list = []
        self.predicted_next_event = Event()
        self.last_event = Event()

    def initialize(self, series_id: str):
        self.series_id = series_id
        self.series_list = get_events_by_series_id(self.series_id)

        # can't get first entry of empty array
        if len(self.series_list) > 1:
            self.last_event = self.series_list[0]

        self.predicted_next_event = self.replace_year_all_elements(self.last_event, self.last_event.year + 1)

        print(self.predicted_next_event)
        self.search_by_acronym(self.predicted_next_event)

    @staticmethod
    def search_by_acronym(event: Event):
        """
        :return : returns the homepage of the event based on search with acronym
        """
        acronym = event.acronym
        gsearch = GoogleSearch()
        search_args = (acronym, 1)
        print(acronym, ": Acronym")
        res = gsearch.search(*search_args)
        print(res, ": Resources")
        return res

    @staticmethod
    def replace_year_all_elements(event: Event, new_year: int):
        """
        :event: Event - previous event
        :new_year: int - the year to which the texts should be changed

        replaces all occurrences of the old year with the passed new year
        """
        temp_event = Event()
        temp_event.year = new_year

        new_year = str(new_year)
        old_year = str(event.year)

        temp_event.title = event.title.replace(old_year, new_year)
        temp_event.acronym = event.acronym.replace(old_year, new_year)
        temp_event.homepage = event.homepage.replace(old_year, new_year)

        return temp_event

    def get_next_event(self):
        return self.last_event

    def get_last_event(self):
        return self.last_event

    def get_anticipated_next_year(self):
        return self.predicted_next_event.year

    def get_summary(self):
        event_evaluator = EventEvaluator(self.predicted_next_event)
        return event_evaluator.is_title_valid()
