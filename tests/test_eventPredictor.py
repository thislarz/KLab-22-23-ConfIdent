import unittest

from kgl_event_prediction.Predictors.multiGuessEventPredictor import MultiGuessEventPredictor
from kgl_event_prediction.Predictors.simpleEventPredictor import SimpleEventPredictor
from kgl_event_prediction.db_util import DbUtil


class TestEventPredictor(unittest.TestCase):

    # @unittest.skip("Queries not yet runnable in test environment")
    def test_class_initialisation(self):
        ep = MultiGuessEventPredictor()
        elist = DbUtil('event_orclone').get_series_by_acronym("AAAI")
        ep.initialize(elist)
        self.assertEqual("AAAI 2022", ep.get_last_event().acronym)


if __name__ == '__main__':
    unittest.main()