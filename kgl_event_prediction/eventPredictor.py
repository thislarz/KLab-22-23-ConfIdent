
class EventPredictor(object):
    """
    superclass for different event predictors
    """
    def __init__(self):
        self.series_id = ""

    def initialize(self, series_id: str):
        """
        :series_id: str : the id of the series for which a new event shall be predicted

        sets all internal variables according to a specified series_id
        """
        self.series_id = series_id

    def get_next_event(self):
        """
        is supposed to return the event that logically follows the last event in the series
        """
        pass

    def get_anticipated_next_year(self):
        """
        is supposed to return the year the next anticipated event takes place in
        """
        pass
