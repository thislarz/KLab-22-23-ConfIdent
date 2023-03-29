import unittest

from kgl_event_prediction.Predictors.simpleEventPredictor import SimpleEventPredictor
from kgl_event_prediction.db_util import DbUtil
from kgl_event_prediction.event import Event


class TestEventPredictor(unittest.TestCase):

    def test_anticipate_year_of_next_event(self):
        test_cases = [
            (
                "ISWC",
                "event_orclone",
                2023,
                "Unexpected year for ISWC on event_orclone"
            ),
            (
                "CICT",
                "event_orclone",
                2017,
                "Unexpected year for CICT on event_orclone"
            ),
            (
                "UAI",
                "event_orclone",
                2021,
                "Unexpected year for UAI on event_orclone"
            ),
            (
                "RANLP",
                "event_wikidata",
                2023,
                "Unexpected year for RANLP on event_wikidata"
            ),
        ]
        ep = SimpleEventPredictor()

        for acronym, table, expected_year, msg in test_cases:
            db = DbUtil(table)
            event_list = db.get_series_by_acronym(acronym)
            # print(event_list)
            ep.initialize(event_list)
            self.assertEqual(expected_year, ep.get_predicted_event().year, msg)

    def test_simple_event_predictor_prediction(self):

        test_cases = [
            (
                "ISWC",
                "event_orclone",
                Event(title='21th International Semantic Web Conference', year=2023, acronym='ISWC 2023', homepage='https://iswc2023.semanticweb.org/', series_id=''),
                "Unexpected Result for ISWC on event_orclone"
            ),
            (
                "AAAI",
                "event_orclone",
                Event(title='Conferenece on Artificial Intelligence', year=2023, acronym='AAAI 2023', homepage='https://aaai.org/Conferences/AAAI-23/', series_id=''),
                "Unexpected Result for AAAI on event_orclone"
            ),
            (
                "RANLP",
                "event_wikidata",
                Event(title='Recent Advances in Natural Language Processing 2023', year=2023, acronym='RANLP 2023', homepage='http://ranlp.org/ranlp2023/', series_id=''),
                "Unexpected Result for RANLP on event_wikidata"
            )
        ]
        ep = SimpleEventPredictor()

        for acronym, table, expected_event, msg in test_cases:
            db = DbUtil(table)
            event_list = db.get_series_by_acronym(acronym)
            ep.initialize(event_list)
            self.assertEqual(ep.get_predicted_event(), expected_event, msg)


if __name__ == '__main__':
    unittest.main()