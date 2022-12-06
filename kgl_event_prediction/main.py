#
# Use this file to run code
#
#
from logging import Logger, DEBUG, StreamHandler
from tabulate import tabulate
import sys
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

# code of interest
event_predictor = SimpleEventPredictor(seriesId_2)
event = event_predictor.get_next_event()

logger.debug(tabulate([event], headers="keys"))

confEvent = EventEvaluator(event).is_title_valid()
print(EventEvaluator.get_title_from_url(event.homepage), "<-> web title")
print(confEvent, "<-> is title valid? ")
