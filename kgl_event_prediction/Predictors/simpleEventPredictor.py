from kgl_event_prediction.Evaluator.eventEvaluator import EventEvaluator
from kgl_event_prediction.Predictors.eventPredictor import EventPredictor
from kgl_event_prediction.utils import *
from kgl_event_prediction.db_util import *
from kgl_event_prediction.event import Event


class SimpleEventPredictor(EventPredictor):
    """
    Simple Event Predictor is used to guess events of a series
    """
    def __init__(self, series_list=[], earliest_year=None):
        super().__init__()
        self.earliest_year = datetime.now().year if earliest_year is None else earliest_year
        self.initialize(series_list)

    def initialize(self, series_list):
        """
        :param series_list: list of Events from a given Series for which the next shall be guessed;

        This method should be used when the guess should be performed on a new series
        """
        self.series_list = series_list
        try:
            self.anticipated_next_year, self.skipped_events = self.anticipate_year_of_next_event(self.series_list)
            self.predicted_next_event = self.predict_next_event(self.series_list[0], self.anticipated_next_year)
        except:
            self.anticipated_next_year = 0
            self.predicted_next_event = None

    def anticipate_year_of_next_event(self, list_of_events: list):

        start_year = list_of_events[0].year

        if len(list_of_events) > 1:
            year_increment = list_of_events[0].year - list_of_events[1].year
        else:
            # only 1 event? assume yearly
            year_increment = 1

        anticipated_year = start_year
        skipped_events = 0
        while True:
            anticipated_year += year_increment
            skipped_events += 1

            if anticipated_year >= self.earliest_year:
                break

        return anticipated_year, skipped_events


    """
    Cases:
    1. year
    2. numeric enumeration (...st, ...nd, ...rd, ...th)
    3. last 2 digits of year
    4. roman numerals (very important)
    """
    def predict_next_event(self, previous_event: Event, next_year: int):
        title = ""
        homepage = None
        year = ""
        acronym = ""

        previous_year = str(previous_event.year)
        year = str(next_year)

        if year in previous_event.title:
            title = previous_event.title.replace(previous_year, year)
        else:
            title = number_increase_in_string(previous_event.title, inc=self.skipped_events)

            # rewrite number idioms
            title = title.replace("1th", "1st")
            title = title.replace("1nd", "1st")
            title = title.replace("1rd", "1st")
            title = title.replace("2st", "2nd")
            title = title.replace("2th", "2nd")
            title = title.replace("2rd", "2nd")
            title = title.replace("3st", "3rd")
            title = title.replace("3th", "3rd")
            title = title.replace("3nd", "3rd")

        if previous_event.homepage is not None:
            if previous_year in previous_event.homepage:
                homepage = previous_event.homepage.replace(previous_year, year)
            else:
                homepage = number_increase_in_string(previous_event.homepage, inc=self.skipped_events)

        if previous_year in previous_event.acronym:
            acronym = previous_event.acronym.replace(previous_year, year)
        else:
            acronym = number_increase_in_string(previous_event.acronym, inc=self.skipped_events)

        anticipated_event = Event(title=title, homepage=homepage, year=int(year), acronym=acronym)

        return anticipated_event

    def get_predicted_event(self):
        return self.predicted_next_event

    def get_anticipated_next_year(self):
        return self.anticipated_next_year

    def get_last_event(self):
        return self.series_list[0]

# If you have a html file in your project
# with open("website.html", "r") as f:  # f is a file
#    doc = BeautifulSoup(f, "html.parser")

# If you have only the url
# url = "https://2021.emnlp.org/"
# res = requests.get(url)
# event_page = BeautifulSoup(res.text, "html.parser")

# event_name = event_page.title  # returns first element with the tag title
# print(event_name.string)

# print(event_page.prettify())  # very nice


if __name__ == "__main__":
    db = DbUtil('event_orclone')
    event_series = db.get_series_by_acronym('ISWC')
    sev = SimpleEventPredictor(event_series)
    next_event = sev.get_next_event()
    print(next_event)
