from kgl_event_prediction.Evaluator.eventEvaluator import EventEvaluator


class EventPredictor(object):
    """
    superclass for different event predictors
    """
    def __init__(self):
        self.series_id = ""

    def initialize(self, series_id: str = "", acronym: str = ""):
        """
        :series_id: str : the id of the series for which a new event shall be predicted
        :acronym: str : the acronym of the conference for which the next event should be guessed

        sets all internal variables according to a specified series_id
        """
        self.series_id = series_id

    def get_next_event(self):
        """
        is supposed to return the event that logically follows the last event in the series
        """
        pass

    def get_last_event(self):
        """
        is supposed to return the event to be belived the last
        """
        pass

    def get_anticipated_next_year(self):
        """
        is supposed to return the year the next anticipated event takes place in
        """
        pass

    def get_summery(self):
        """
        is supposed to evaluate the guess and return the prediction results as dictionary

        return {
            "title similarity": 0.93,
            "year check": True
            "verdict": gut / meh / trash
            "confidence": [0.0 : 1:0]
        }
        """

        event_evaluator = EventEvaluator(self.predicted_next_event)
        event_evaluator.summarize_event()