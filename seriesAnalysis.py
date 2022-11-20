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


def get_entries_for_series_id(series_id):
    res = []

    temp_query = open("./Queries/query02.sql").read()
    temp_query = replace_var_in_sql(temp_query, "var2", i)

    res = query_corpus_db(temp_query)

    res = remove_duplicates(res)
    res = [series_id] + res

    return res


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


# retrieves the eventInSeriesId's (unique) from wikidata
query = open("./Queries/getEventInSeriesId.sql").read()
eventSeriesId_list = query_corpus_db(query)

# convert query results from dict with one entry to strings
for i in range(0, len(eventSeriesId_list)):
    eventSeriesId_list[i] = eventSeriesId_list[i]['eventInSeriesId']


seriesList = []
# for every SeriesId all events with that id are returned and saved in a corresponding list
for i in eventSeriesId_list:

    if type(i) == str:
        seriesList.append(get_entries_for_series_id(i))
    else:
        eventSeriesId_list.remove(i)

# logger.debug(tabulate(seriesList, headers="keys"))


# count number of events per series
count_total_entries = 0
count_len_max3 = 0
count_len_min10 = 0
count_homepage = 0
for i in seriesList:
    print(len(i)-1, " : ", i)
    count_total_entries += len(i)-1
    if len(i)-1 <= 3:
        count_len_max3 += 1
    elif len(i)-1 >= 10:
        count_len_min10 += 1

    if i[1]['homepage'] is not None:
        count_homepage += 1

avg_series_length = count_total_entries / len(seriesList)
print("avg_series_length", avg_series_length)
print("series with 3 or less: ", count_len_max3, str(count_len_max3/len(seriesList)*100)+"%")
print("series with 10 or more: ", count_len_min10,  str(count_len_min10/len(seriesList)*100)+"%")
print("number of series: ", len(seriesList))
print("series with homepage: ", count_homepage, str(count_homepage/len(seriesList)*100)+"%")
