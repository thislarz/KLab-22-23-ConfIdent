from logging import Logger, DEBUG, StreamHandler
from tabulate import tabulate
import sys

from kgl_event_prediction.eventEvaluator import EventEvaluator
from kgl_event_prediction.eventPredictor import EventPredictor
from kgl_event_prediction.simpleEventPredictor import SimpleEventPredictor
from utils import *


class SeriesAnalysis(object):
    def __init__(self):
        self.logger = Logger(name="Steve")
        self.logger.setLevel(DEBUG)
        self.logger.addHandler(StreamHandler(sys.stdout))

        self.id_list = []
        self.series_list = []

    def load_series(self):
        """
        runs queries to load all series entries (takes some time)
        """
        self.id_list = get_all_unique_series_ids()

        for i in self.id_list:
            temp = get_events_by_series_id(i)
            temp = [i] + temp
            self.series_list.append(temp)

    def all_series_analytics(self):
        """
        :print: analytic data for the series in the console
        """
        count_total_entries = 0
        count_len_max3 = 0
        count_len_min10 = 0
        count_homepage = 0
        for i in self.series_list:
            print(len(i) - 1, " : ", i)
            count_total_entries += len(i) - 1
            if len(i) - 1 <= 3:
                count_len_max3 += 1
            elif len(i) - 1 >= 10:
                count_len_min10 += 1

            if len(i) > 1 and i[1].homepage is not None:
                count_homepage += 1

        avg_series_length = count_total_entries / len(self.series_list)
        print("avg_series_length", avg_series_length)
        print("series with 3 or less: ", count_len_max3, str(count_len_max3 / len(self.series_list) * 100) + "%")
        print("series with 10 or more: ", count_len_min10, str(count_len_min10 / len(self.series_list) * 100) + "%")
        print("number of series: ", len(self.series_list))
        print("series with homepage: ", count_homepage, str(count_homepage / len(self.series_list) * 100) + "%")

    def predict_event(self, event_predictor: EventPredictor, series_id: str):
        """
        :event_predictor: EventPredictor: any subclass of EventPredictor to be used in predicting Event
        :series_id: str: the id of the series where the next event should be predicted

        :print: prints the next event and some additional information
        """
        event_predictor.initialize(series_id)
        next_event = event_predictor.get_next_event()
        conf_event = EventEvaluator(next_event).is_title_valid()
        self.logger.debug(tabulate([next_event], headers="keys"))
        print(EventEvaluator.get_title_from_url(next_event.homepage), "<-> web title")
        print(conf_event, "<-> is title valid? ")

    def rate_event_prediction(self, event_predictor: EventPredictor):
        """
        - input: EventPredictor
        - output: IDs, predicted event, and summary (title, homepage, acronym, confidence...)
        """

        count_events = 0
        count_events_not_null = 0
        count_success = 0
        for i in self.id_list:
            count_events += 1
            # event_predictor = SimpleEventPredictor(i)
            event_predictor.initialize(i)
            next_event = event_predictor.get_next_event()
            if next_event is None:
                continue
            else:
                count_events_not_null += 1
                print("ID: ", i)
                self.logger.debug(tabulate([next_event], headers="keys"))
                event_success = event_predictor.get_summary()
                print("Title confirmation worked? ", event_success)
                if event_success:
                    count_success += 1

        print("-------------------- Summary:")
        print("Events: ", count_events)
        print("Events not null: ", count_events_not_null)
        print("Successes: ", count_success)
        print("Success rate: ", count_success/count_events_not_null)
