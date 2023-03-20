import unittest

from kgl_event_prediction.Evaluator.eventEvaluator import EventEvaluator
from kgl_event_prediction.event import Event


class TestEventEvaluator(unittest.TestCase):
    """
    test for event evaluator
    """

    @unittest.skip
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

    @unittest.skip
    def test_summarize_event(self):
        predicted_event = Event(title='18th International Conference on Autonomous Agents and Multiagent Systems',
                                year='2019', acronym='AAMAS 2019', homepage='http://aamas2019.encs.concordia.ca/')
        event_evaluator = EventEvaluator(predicted_event)
        summary = event_evaluator.summarize_event()
        test_dic = {
            "title_similarity": 0.13333333333333333,
            "year_check": True,
            "acronym_check": True,
            "verdict": "okay"
        }
        self.assertEqual(summary, test_dic)

    def test_similarity(self):
        a = "The 43th Conference for Bamboo growth 2017"
        b = "The 43th Conference for Bamboo growth 2018"
        sim = EventEvaluator.similarity(a, b)
        print(sim)
        print(EventEvaluator.similarity(
            "Bamboo is often associated with Pandas",
            "The 43th Conference for Bamboo growth 2018"
        ))
        print(EventEvaluator.similarity(
            "The 3rd Conference for growth 2018",
            "The 43th Conference for Bamboo growth 2018"
        ))
        print(EventEvaluator.similarity(
            "National Conference on Artificial Intelligence -- AAAI 1983 -- Hongkong",
            "National Conference on Artificial Intelligence"
        ))
        print(EventEvaluator.similarity(
            "AAAI 1983",
            "AAAI"
        ))
        print(EventEvaluator.similarity(
            "AAAI 1983",
            "IAAU 1983"
        ))
        print(EventEvaluator.similarity(
            "18th International Conference on Autonomous Agents and Multiagent Systems",
            "AAMAS 2019 - Home"
        ))

if __name__ == '__main__':
    unittest.main()
