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

    def test_summarize_event(self):
        test_cases = [
            (
                Event(title='18th International Conference on Autonomous Agents and Multiagent Systems',
                      year='2019', acronym='AAMAS 2019', homepage='http://aamas2019.encs.concordia.ca/'),
                0.85,
                {
                    "title_similarity": 0.2,
                    "year_check": True,
                    "acronym_check": True,
                    "verdict": "okay"
                },
                "Unexpected Summary for AAMAS 2019"
            ),
            (
                Event(title='11th ACM Conference on Bioinformatics, Computational Biology, and Health Informatics',
                      year='2020', acronym='ACM-BCB 2020', homepage='https://acm-bcb.org/2020/index.php'),
                0.85,
                {
                    "title_similarity": 0.14583333333333334,
                    "year_check": True,
                    "acronym_check": True,
                    "verdict": "okay"
                },
                "Unexpected Summary for ACM-BCB 2020"
            ),
            (
                Event(title='18th Extended Semantic Web Conference', year='2022', acronym='ESWC 2022',
                      homepage='https://2022.eswc-conferences.org/', series_id=''),
                0.85,
                {
                    "title_similarity": 0.4827586206896552,
                    "year_check": True,
                    "acronym_check": True,
                    "verdict": "okay"
                },
                "Unexpected Summary for ESWC 2022"
            ),
            (
                Event(title='21th International Semantic Web Conference', year='2023', acronym='ISWC 2023',
                      homepage='https://iswc2023.semanticweb.org/', series_id=''),
                0.70,
                {
                    "title_similarity": 0.9090909090909091,
                    "year_check": True,
                    "acronym_check": True,
                    "verdict": "good"
                },
                "Unexpected Summary for ISWC 2023"
            ),
            (
                Event(title='21th International Semantic Web Conference', year='2023', acronym='ISWC 2023',
                      homepage='', series_id=''),
                0.80,
                {
                    "title_similarity": 0.0,
                    "year_check": False,
                    "acronym_check": False,
                    "verdict": "not_found"
                },
                "Unexpected Summary for ISWC 2023"
            )
        ]
        for predicted_event, threshold, expected_summary, msg in test_cases:
            event_evaluator = EventEvaluator(predicted_event)
            summary = event_evaluator.summarize_event(threshold=threshold)
            self.assertEqual(summary, expected_summary, msg)

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
