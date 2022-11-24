from lodstorage.sql import SQLDB
from os.path import expanduser
home = expanduser("~")


def query_corpus_db(sql_query: str = None):
    """
    Returns the result of a direct query to the database
    """
    if sql_query is None:
        sql_query = "SELECT * FROM event LIMIT 5"

    # specifies file location of the Database
    db_file = home+"/ConferenceCorpus/EventCorpus.db"
    sql_db = SQLDB(dbname=db_file)

    # now we can directly query the EventCorpus.db and get LoDs (List of Dicts) as result
    # Try it by writing your own query
    res = sql_db.query(sql_query)
    return res


def get_events_by_series_id(id):
    """
    :param id: ID of series as string
    :return: list of all events of series

    use query that takes id as an argument and returns all events of that series
    """
    id = str(id)
    query = open("./Queries/getEventsBySeriesId.sql").read()
    query = query.replace("$VARIABLE1", id)
    events = query_corpus_db(query)
    events = remove_duplicates(events)
    return events


def remove_duplicates(element_list):
    prev = 0
    removal_list = []
    for i in range(1, len(element_list)):
        if element_list[prev] == element_list[i]:
            removal_list.append(element_list[i])
        prev = i

    for i in removal_list:
        element_list.remove(i)

    return element_list

