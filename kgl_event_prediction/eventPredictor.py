
class EventPredictor(object):
    """
    superclass for different event predictors
    """
    def __init__(self, series_id: str):
        self.series_id = series_id

    def get_next_event(self):
        pass

    def get_anticipated_next_year(self):
        pass
