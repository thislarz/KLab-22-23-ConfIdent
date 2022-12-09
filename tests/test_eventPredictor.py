import unittest

from kgl_event_prediction.eventPredictor import EventPredictor
from kgl_event_prediction.simpleEventPredictor import SimpleEventPredictor


class TestEventPredictor(unittest.TestCase):

    def test_classCreation(self):
        with self.assertRaises(Exception):
            ep = SimpleEventPredictor("Q18353514")


if __name__ == '__main__':
    unittest.main()