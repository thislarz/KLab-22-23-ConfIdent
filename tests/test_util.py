import unittest

from kgl_event_prediction.event import Event
from kgl_event_prediction.utils import convert_to_event


class TestEventEvaluator(unittest.TestCase):

    def test_convert_to_event(self):
        event = Event(
            title="placeholder_title",
            homepage="placeholder_homepage",
            year=1000,
            acronym="placeholder_acronym"
        )
        event_dict = {
            "title": "placeholder_title",
            "homepage": "placeholder_homepage",
            "year": 1000,
            "acronym": "placeholder_acronym"
        }
        self.assertEqual(event, convert_to_event(event_dict), "Event conversion was incorrect.")
        self.assertEqual("placeholder_title", event.title, "Event was created with wrong title.")
        self.assertEqual("placeholder_homepage", event.homepage, "Event was created with wrong homepage.")
        self.assertEqual("placeholder_acronym", event.acronym, "Event was created with wrong acronym.")
        self.assertEqual(1000, event.year, "Event was created with wrong year.")


if __name__ == '__main__':
    unittest.main()