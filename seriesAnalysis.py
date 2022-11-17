from logging import Logger, DEBUG, StreamHandler
from lodstorage.sql import SQLDB
from tabulate import tabulate
import sys
from os.path import expanduser
home = expanduser("~")

logger = Logger(name="Steve")
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler(sys.stdout))


def query_corpus_db(sql_query: str = None):
    """
    Prints the result of a direct query to the database
    """
    if sql_query is None:
        sql_query = "SELECT * FROM event LIMIT 5"

    # specifies file location of the Database
    db_file = home+"/.conferencecorpus/EventCorpus.db"
    sql_db = SQLDB(dbname=db_file)

    # now we can directly query the EventCorpus.db abd get LoDs (List of Dicts) as result
    # Try it by writing your own query
    res = sql_db.query(sql_query)
    #logger.debug(tabulate(res, headers="keys"))
    return res


def replace_var_in_sql(sql, var, text):
    """
    :param sql: sql-query string that should be modified
    :param var: name of the variable that should be replaced
    :param text: string the variable should be replaced with
    :return: modified query
    """
    temp_var = "<"+var+">"
    return sql.replace(temp_var, text)


# retrives the eventInSeriesId's (unique) from wikidata
query = open("./Queries/getEventInSeriesId.sql").read()
eventSeriesId_list = query_corpus_db(query)

# convert query results from dict with one entry to strings
for i in range(0, len(eventSeriesId_list)):
    eventSeriesId_list[i] = eventSeriesId_list[i]['eventInSeriesId']


seriesList = []
# for every SeriesId all events with that id are returned and saved in a corresponding list
for i in eventSeriesId_list:
    if type(i) == str:
        temp_query = open("./Queries/query02.sql").read()
        temp_query = replace_var_in_sql(temp_query, "var2", i)
        seriesList.append(query_corpus_db(temp_query))
    else:
        eventSeriesId_list.remove(i)

# logger.debug(tabulate(seriesList, headers="keys"))

# count number of events per series
for i in seriesList:
    print(len(i), " : ", i)
