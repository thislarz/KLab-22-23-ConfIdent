import unittest

from kgl_event_prediction.Predictors.multiGuessEventPredictor import MultiGuessEventPredictor
from kgl_event_prediction.Predictors.simpleEventPredictor import SimpleEventPredictor
from kgl_event_prediction.db_util import DbUtil
from kgl_event_prediction.event import Event


class TestEventPredictor(unittest.TestCase):

    # @unittest.skip("Queries not yet runnable in test environment")
    def test_multi_guess_event_prediction_prediction(self):

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
            )
        ]
        ep = MultiGuessEventPredictor()

        for acronym, table, expected_event, msg in test_cases:
            db = DbUtil(table)
            event_list = db.get_series_by_acronym(acronym)
            ep.initialize(event_list)
            self.assertEqual(ep.get_predicted_event(), expected_event, msg)


if __name__ == '__main__':
    unittest.main()