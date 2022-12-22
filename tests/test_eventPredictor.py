import unittest

from kgl_event_prediction.eventPredictor import EventPredictor
from kgl_event_prediction.simpleEventPredictor import SimpleEventPredictor


class TestEventPredictor(unittest.TestCase):

    @unittest.skip("Queries not yet runnable in test environment")
    def test_class_initialisation(self):
        ep = SimpleEventPredictor()
        ep.initialize("Q1961016")
        self.assertEqual("Q1961016", ep.series_id, 'Initialized with wrong series_id')


if __name__ == '__main__':
    unittest.main()