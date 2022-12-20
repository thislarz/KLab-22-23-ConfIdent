#
# Use this file to run code
#
#
from logging import Logger, DEBUG, StreamHandler
from tabulate import tabulate
import sys

from kgl_event_prediction.SearchingEventPredictor import SearchingEventPredictor
from kgl_event_prediction.db_util import DbUtil
from kgl_event_prediction.seriesAnalysis import SeriesAnalysis
from kgl_event_prediction.utils import *
from kgl_event_prediction.simpleEventPredictor import SimpleEventPredictor
from kgl_event_prediction.eventEvaluator import EventEvaluator

# sets up the Logger
logger = Logger(name="Steve")
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler(sys.stdout))

# defined variables for easy experimenting
seriesId_1 = "Q1961016"
seriesId_2 = "Q18353514"

seriesAnalysis = SeriesAnalysis()
# seriesAnalysis.load_series()
simple_ev = SimpleEventPredictor()
searching_ev = SearchingEventPredictor()

ev = searching_ev
# seriesAnalysis.rate_event_prediction(event_predictor=ev)
# seriesAnalysis.predict_event(event_predictor=ev, series_id=seriesId_1)

# gives general statistics for different datasets
# SeriesAnalysis.general_cc_analytics()

SeriesAnalysis.or_analytics(last_years=2)

"""
db = DbUtil("event_or")
res = db.get_last_x_events(1)
logger.debug(tabulate(res, headers="keys"))
"""