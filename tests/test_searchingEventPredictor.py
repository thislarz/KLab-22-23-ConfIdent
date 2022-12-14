import unittest

from kgl_event_prediction.SearchingEventPredictor import SearchingEventPredictor
from kgl_event_prediction.eventPredictor import EventPredictor
from kgl_event_prediction.event import Event


class TestSearchingEventPredictor(unittest.TestCase):

    def test_class_initialization(self):
        with self.assertRaises(Exception):
            ep = SearchingEventPredictor()
            ep.initialize("Q1961016")
        self.assertEqual("Q1961016", ep.series_id, 'Initialized with wrong series_id')

        # ep.initialize("Q1961016")

        # tests getter methods
        next = ep.get_next_event()
        last = ep.get_last_event()
        self.assertEqual(next, ep.predicted_next_event, "next_event wasn't properly initialized")
        self.assertEqual(last, ep.get_last_event(), "last_event wasn't properly initialized")
        # self.assertGreater(len(ep.series_list), 0, "somehow the series_list is empty")

    def test_replace_year_all_elements(self):
        event1 = Event(
            title="Banana old but gold 2022",
            acronym="Ban2022",
            year=2022,
            homepage="https://Ban2022.com"
        )
        event2 = Event(
            title="Banana old but gold 2023",
            acronym="Ban2023",
            year=2023,
            homepage="https://Ban2023.com"
        )
        self.assertEqual(SearchingEventPredictor.replace_year_all_elements(event1, event2.year), event2, "Not all years were correctly replaced")


if __name__ == '__main__':
    unittest.main()
    