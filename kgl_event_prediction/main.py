#
# Use this file to run code
#
#
from logging import Logger, DEBUG, StreamHandler

import sys

from kgl_event_prediction.seriesAnalysis import SeriesAnalysis

from kgl_event_prediction.simpleEventPredictor import SimpleEventPredictor
from kgl_event_prediction.eventEvaluator import EventEvaluator

# sets up the Logger
logger = Logger(name="Steve")
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler(sys.stdout))

# defined variables for easy experimenting
seriesId_1 = "Q1961016"
seriesId_2 = "Q18353514"

# creates an Event Predictor object that can be used to predict a single event or passed to seriesAnalysis to evaluate
simple_ev = SimpleEventPredictor()

# creates A seriesAnalysis object
seriesAnalysis = SeriesAnalysis()

# evaluates the event_predictor on all series
seriesAnalysis.rate_event_prediction(event_predictor=simple_ev)


# sets up the eventPredictor with a series
simple_ev.initialize(seriesId_1)
# predicts the next event
event = simple_ev.get_next_event()

confEvent = EventEvaluator(event).is_element_valid("title")
print(EventEvaluator.get_element_content_from_url(event.homepage, "title"), "<-> web title")
print(confEvent, "<-> is title valid? ")


