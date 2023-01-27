import unittest

from kgl_event_prediction.event import Event
from kgl_event_prediction.eventEvaluator import EventEvaluator
from kgl_event_prediction.eventPredictor import EventPredictor
from kgl_event_prediction.simpleEventPredictor import SimpleEventPredictor


class TestEventEvaluator(unittest.TestCase):

    def test_get_title_from_url(self):
        self.assertEqual(
            EventEvaluator.get_element_content_from_url("", "title"),
            None,
            "Unexpected results for Empty domain"
        )
        self.assertEqual(
            EventEvaluator.get_element_content_from_url("https://2022.emnlp.org/", "title"),
            "The 2022 Conference on Empirical Methods in Natural Language Processing - emnlp 2022",
            "Wrong title for https://2022.emnlp.org/ or title changed"
        )
        self.assertEqual(
            EventEvaluator.get_element_content_from_url(None, "title"),
            None,
            "Unexpected result for None"
        )
        self.assertEqual(
            EventEvaluator.get_element_content_from_url("Banana", "title"),
            None,
            ""
        )


if __name__ == '__main__':
    unittest.main()