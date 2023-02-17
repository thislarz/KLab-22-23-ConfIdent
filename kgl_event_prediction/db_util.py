import pathlib
from datetime import datetime

from lodstorage.sql import SQLDB
from os.path import expanduser
from kgl_event_prediction.event import Event
from kgl_event_prediction.utils import *
from tabulate import tabulate


class DbUtil(object):

    def __init__(self, table: str):
        self.tabel = table

    def get_all_events(self):
        """
        queries all events from the initialized table and returns a list of Events (Dataclass objects)
        """
        query = open(str(pathlib.Path(__file__).parent)+"/resources/queries/getAllEvents.sql").read()
        query = replace_var_in_sql(query, "VARIABLE1", self.tabel)
        res = DbUtil.query_corpus_db(query)

        # converts dict event list to list of Events
        events = []
        for event in res:
            events.append(DbUtil.convert_to_event(event))
        return events

    def get_event_by_acronym(self, acronym: str):
        """
        :acronym : takes an acronym of an event and returns the Event if that exist in the table eles it raises Error
        """
        query_source = open(str(pathlib.Path(__file__).parent)+"/resources/queries/getEventByField.sql").read()

        # fills in the variable fields
        query_acr = replace_var_in_sql(query_source, "VARIABLE1", self.tabel)
        query_acr = replace_var_in_sql(query_acr, "VARIABLE2", 'acronym')
        query_acr = replace_var_in_sql(query_acr, "VARIABLE3", acronym)

        # runs query
        res = DbUtil.query_corpus_db(query_acr)

        # convert event to Event
        if res != []:
            converted_event = DbUtil.convert_to_event(res[0])
        else:
            return Event()

        return converted_event

    def get_last_x_events(self, last_years: int):
        """
        :param last_years: int determining how many years should be queried.
        :return: list of Events
        works on event_or (needs to be configured to work with a queries with a year field)
        """
        # loads the query
        if self.tabel == "event_or":
            query = open(str(pathlib.Path(__file__).parent)+"/resources/queries/getLastXEvents.sql").read()
        elif self.tabel == "event_orclone":
            query = open(str(pathlib.Path(__file__).parent)+"/resources/queries/getLastXEventsORCLONE.sql").read()
        else:
            query = ""
            print("WARNING - Tried running get_last_x_events on "+self.tabel+" which is not allowed.")

        # sets the table for the query (currently only event_or works or similar)
        query = replace_var_in_sql(query, "VARIABLE1", self.tabel)

        # creates query snippet that selects only the recent entries
        years = ""
        now = datetime.now().year
        for i in range(0, last_years):
            temp_year = now - i

            if self.tabel == "event_or":
                years += "    startDate LIKE '"+str(temp_year)+"%'"
                if i != last_years-1:
                    years += "OR \n"
            elif self.tabel == "event_orclone":
                years += " year LIKE "+str(temp_year)+" "
                if i != last_years-1:
                    years += "OR \n"

        # sets query snipped
        query = replace_var_in_sql(query, "VARIABLE_YEARS", years)
        # runs query
        res = DbUtil.query_corpus_db(query)

        # converts dict event list to list of Events
        events = []
        for event in res:
            events.append(DbUtil.convert_to_event(event))
        return events

    @staticmethod
    def group_by_acronym(event_list: list):

        # a high value indicates bad data. Should be kept in mind when interpreting results
        acronym_not_string = 0
        series_dict = {

        }
        for event in event_list:

            # remove years from acronyms
            acr = ""
            try:
                temp = event.acronym.split(' ')
                if len(temp) == 1:
                    temp = event.acronym.split('_')
            except:
                temp = ""
                acronym_not_string += 1

            # only focuses on the split of the acronym that is no number
            for x in temp:
                if x.isnumeric() is False:
                    acr += x

            if acr in series_dict.keys():
                series_dict[acr].append(event)
            elif acr != "":
                series_dict[acr] = [event]

        series_count = 0
        for x in series_dict.keys():
            series_count += 1
            print(x)
            print(tabulate(series_dict[x], headers="keys"))

        print(series_count, " series count")
        print(acronym_not_string, " acronym not string")
        print(len(event_list), " total events")
    @staticmethod
    def query_corpus_db(sql_query: str = None):
        """
        Returns the result of a direct query to the database
        """
        home = expanduser("~")

        if sql_query is None:
            sql_query = "SELECT * FROM event LIMIT 5"

        # specifies file location of the Database
        try:
            db_file = home + "/.conferencecorpus/EventCorpus.db"
        except:
            db_file = home + "/ConferenceCorpus/EventCorpus.db"
        sql_db = SQLDB(dbname=db_file)

        # now we can directly query the EventCorpus.db and get LoDs (List of Dicts) as result
        # Try it by writing your own query
        res = sql_db.query(sql_query)
        return res

    @staticmethod
    def get_events_by_series_id(series_id: str):
        """
        :param series_id: ID of series as string
        :return: list of all events of series

        use query that takes id as an argument and returns all events of that series
        """
        series_id = str(series_id)
        query = open(str(pathlib.Path(__file__).parent)+"/resources/queries/getEventsBySeriesId.sql").read()
        query = replace_var_in_sql(query, "VARIABLE1", series_id)
        res = DbUtil.query_corpus_db(query)
        res = remove_duplicates(res)

        # translate queried Events into python Event objects
        events = []
        for queried_event in res:
            events.append(convert_to_event(queried_event))
        return events

    @staticmethod
    def convert_to_event(queried_event: dict):
        """
        :param queried_event: is an event as queried from the database;
            required fields are homepage, title, acronym
        :return: an Event object with the same values as the queried event
        """
        year = 0
        title = queried_event['title']
        homepage = queried_event['homepage']

        # handle year as well as Date (datetime)
        if 'year' in queried_event.keys() and queried_event['year'] is not None:
            year = queried_event['year']
        elif 'startDate' in queried_event.keys() \
                and queried_event['startDate'] is not None \
                and type(queried_event['startDate']) == datetime:
            year = queried_event['startDate'].year

        acronym = queried_event['acronym']
        event = Event(title=title, homepage=homepage, year=year, acronym=acronym)
        return event
