from BaseTest import Basetest
from kgl_event_prediction import utils as ut

class UtilTest(Basetest):
    """
    test the wikidata search
    """
    @staticmethod
    def test_get_all_unique_series_id():
        print(ut.get_all_unique_series_ids())