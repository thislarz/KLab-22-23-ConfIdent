import unittest

from kgl_event_prediction.Predictors.multiGuessEventPredictor import MultiGuessEventPredictor
from kgl_event_prediction.Predictors.simpleEventPredictor import SimpleEventPredictor


class TestEventPredictor(unittest.TestCase):

    # @unittest.skip("Queries not yet runnable in test environment")
    def test_class_initialisation(self):
        ep = MultiGuessEventPredictor()
        ep.initialize(acronym="AAAI 2017")
        self.assertEqual("AAAI 2017", ep.get_last_event().acronym)


if __name__ == '__main__':
    unittest.main()