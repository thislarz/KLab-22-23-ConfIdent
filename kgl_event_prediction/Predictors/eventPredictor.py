from kgl_event_prediction.Evaluator.eventEvaluator import EventEvaluator


class EventPredictor(object):
    """
    superclass for different event predictors
    """
    def __init__(self, series_list=[]):
        self.series_list = series_list

    def initialize(self, series_list):
        """
        :params series_list: list of Events from a series
        """
        self.series_list = series_list

    def get_predicted_event(self):
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

    def get_summery(self, threshold : float = 0.8):
        """
        is supposed to evaluate the guess and return the prediction results as dictionary

        return {
            "title_similarity": [0.0 : 1.0],
            "year_check": True / False
            "acronym_check": True / False
            "verdict": good / okay / bad / not_found
        }
        """

        event_evaluator = EventEvaluator(self.get_predicted_event())
        summary = event_evaluator.summarize_event(threshold=threshold)
        return summary
