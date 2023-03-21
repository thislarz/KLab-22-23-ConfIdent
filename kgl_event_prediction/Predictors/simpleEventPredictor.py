from kgl_event_prediction.Evaluator.eventEvaluator import EventEvaluator
from kgl_event_prediction.Predictors.eventPredictor import EventPredictor
from kgl_event_prediction.utils import *
from kgl_event_prediction.db_util import *
from kgl_event_prediction.event import Event


class SimpleEventPredictor(EventPredictor):
    """
    Simple Event Predictor is used to guess events of a series
    """
    def __init__(self, series_list = []):
        super().__init__()
        self.initialize(series_list)

    def initialize(self, series_list):
        """
        :param series_list: list of Events from a given Series for which the next shall be guessed;

        This method should be used when the guess should be performed on a new series
        """
        self.series_list = series_list
        try:
            self.anticipated_next_year = self.anticipate_year_of_next_event(self.series_list)
            self.predicted_next_event = self.predict_next_event(self.series_list[0], self.anticipated_next_year)
        except:
            self.anticipated_next_year = 0
            self.predicted_next_event = None

    def anticipate_year_of_next_event(self, list_of_events: list):
        year1 = list_of_events[0].year
        year2 = 0

        # TODO handle case of only one event entry
        # TODO handle case of half-yearly events ???!
        # TODO handle case of outdated database entries

        i = 0
        while i < len(list_of_events)-1 and list_of_events[i].year == year1:
            i += 1

        year2 = list_of_events[i].year

        anticipated_year = year1 + (year1 - year2)
        return anticipated_year

    #def number_increase(self, match):
     #   num = int(match.group())
      #  return str(num + 1)

    """
    Cases:
    1. year
    2. numeric enumeration (...st, ...nd, ...rd, ...th)
    3. last 2 digits of year
    4. roman numerals (very important)
    """
    def predict_next_event(self, proceeding: Event, next_year: int):
        title = ""
        homepage = ""
        year = ""
        acronym = ""

        preceding_year = str(proceeding.year)
        year = str(next_year)

        try:
            title = proceeding.title.replace(preceding_year, year)
            #if title == proceeding.title:
             #   title = self.number_increase_in_string(proceeding.title)
        except:
            title = ""

        try:
            homepage = proceeding.homepage.replace(preceding_year, year)
            if homepage == proceeding.homepage:
                diff = int(year) - int(preceding_year)
                for x in range(diff):
                    homepage = number_increase_in_string(proceeding.homepage)
        except:
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
