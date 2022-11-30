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
    logger.debug(tabulate(res, headers="keys"))
    return res


# loads the query from the Queries folder and passes it to the query_corpus_db method which executes the query
query = open("resources/Queries/getEventInSeriesId.sql").read()
data = query_corpus_db(query)
