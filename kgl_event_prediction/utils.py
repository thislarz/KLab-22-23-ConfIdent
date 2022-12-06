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
    try:
        db_file = home + "/.conferencecorpus/EventCorpus.db"
    except:
        db_file = home + "/ConferenceCorpus/EventCorpus.db"
    sql_db = SQLDB(dbname=db_file)

    # now we can directly query the EventCorpus.db and get LoDs (List of Dicts) as result
    # Try it by writing your own query
    res = sql_db.query(sql_query)
    return res


def get_events_by_series_id(series_id: str):
    """
    :param series_id: ID of series as string
    :return: list of all events of series

    use query that takes id as an argument and returns all events of that series
    """
    series_id = str(series_id)
    query = open("resources/queries/getEventsBySeriesId.sql").read()
    query = replace_var_in_sql(query, "VARIABLE1", series_id)
    events = query_corpus_db(query)
    events = remove_duplicates(events)
    return events



def get_all_unique_series_ids():
    """
    :return: list of all wikidata events as list of strings
    """
    query = open("resources/queries/getEventInSeriesId.sql").read()
    event_series_id_list = query_corpus_db(query)

    # convert query results from dict with one entry to strings
    for i in range(0, len(event_series_id_list)):
        event_series_id_list[i] = event_series_id_list[i]['eventInSeriesId']

    return event_series_id_list


def replace_var_in_sql(sql: str, var: str, text: str):
    """
    :param sql: sql-query string that should be modified
    :param var: name of the variable that should be replaced will be surrounded by $ escape characters in SQL
    :param text: string the variable should be replaced with
    :return: modified query
    """
    temp_var = "$"+str(var)+"$"
    return sql.replace(temp_var, str(text))


def remove_duplicates(element_list: list):
    """
    :param element_list: a list
    compares two adjecent elements and removes the second if identical to first.
    Removes all dublicates if list is ordered
    """
    prev = 0
    removal_list = []
    for i in range(1, len(element_list)):
        if element_list[prev] == element_list[i]:
            removal_list.append(element_list[i])
        prev = i

    for i in removal_list:
        element_list.remove(i)

    return element_list
