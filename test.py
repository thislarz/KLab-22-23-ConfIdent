# Plan:
# 1. Funktion bekommt SerienID und gibt Einträge der Vorjahre zurück (gibt Liste) CHECK

# 2. Funktion bekommt Liste von Events einer Serie und gibt nächstes Event zurück CHECK

# 3. Funktion -> Gegeben ein Event, prüft ob Homepage existiert und gibt <title> zurück (noch nicht) (CHECK???)

# 4. prüfen ob <title> = event name (soll kleine Unterschiede erkennen können) CHECK
#
#
from utils import *
from logging import Logger, DEBUG, StreamHandler
from tabulate import tabulate
import sys

logger = Logger(name="Steve")
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler(sys.stdout))

# print(get_events_by_series_id("Q18353514"))
logger.debug(tabulate(get_events_by_series_id("Q18353514"), headers="keys")) #Q1961016, Q18353514
events = get_events_by_series_id("Q18353514")


def anticipated_year_of_next_event(list_of_events):
    year1 = list_of_events[0]["year"]
    year2 = 0

    # TODO handle case of only one event entry
    # TODO handle case of half-yearly events ???!
    # TODO handle case of outdated database entries

    i = 0
    while i < len(list_of_events)-1 and list_of_events[i]["year"] == year1:
        i += 1

    year2 = list_of_events[i]["year"]

    anticipated_year = year1 + (year1 - year2)
    return anticipated_year


"""
Cases:
1. year
2. numeric enumeration (...st, ...nd, ...rd, ...th)
3. last 2 digits of year
4. roman numerals (very important)
"""

def create_anticipated_event(preceding, next_year):
    title = ""
    homepage = ""
    year = ""
    acronym = ""

    preceding_year = str(preceding["year"])
    year = str(next_year)

    title = preceding["title"].replace(preceding_year, year)
    homepage = preceding["homepage"].replace(preceding_year, year)
    acronym = preceding["acronym"].replace(preceding_year, year)

    anticipated_event = {"title": title, "homepage": homepage, "year": next_year, "acronym": acronym}

    return anticipated_event


def magic():
    return "NeurIPS 2021"


def is_title_valid(title, event):
    event_title = event["title"]

    if title.find(event_title) != -1 or event_title.find(title) != -1:
        return True

    return False


next_year = anticipated_year_of_next_event(events)
next_event = create_anticipated_event(events[0], next_year)

print(next_event)
print(is_title_valid(magic(), next_event))

