import unittest

from kgl_event_prediction.event import Event
from kgl_event_prediction.eventEvaluator import EventEvaluator
from kgl_event_prediction.eventPredictor import EventPredictor
from kgl_event_prediction.simpleEventPredictor import SimpleEventPredictor


class TestEventEvaluator(unittest.TestCase):
    """
    test for event evaluator
    """

    def test_get_title_from_url(self):
        """
        test getting a title from an url
        """
        test_cases = [
            (
                "",
                "title",
                None,
                "Unexpected results for Empty domain"
            ),
            (
                "https://2022.emnlp.org/",
                "title",
                "The 2022 Conference on Empirical Methods in Natural Language Processing - emnlp 2022",
                "Wrong title for https://2022.emnlp.org/ or title changed"
            ),
            (
                "https://2022.emnlp.org/",
                "h2",
                "?",
                "what h2"
            ),
            (
                None,
                "title",
                None,
                "Unexpected result for None"
            ),
            (
                "Banana",
                "title",
                None,
                ""
            )
        ]
        debug = True
        debug = self.debug
        for url, html_element, expected, msg in test_cases:
            content = EventEvaluator.get_element_content_from_url(url, html_element, timeout=0.5)
            if debug:
                print(content)
            if expected is None:
                self.assertIsNone(content, msg)
            else:
                self.assertEqual(
                    content.lower(),
                    expected.lower(),
                    msg
                )


if __name__ == '__main__':
    unittest.main()