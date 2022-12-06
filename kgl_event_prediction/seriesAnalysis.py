from logging import Logger, DEBUG, StreamHandler
from tabulate import tabulate
import sys
from utils import *

logger = Logger(name="Steve")
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler(sys.stdout))


def all_series_analytics():
    """
    :print: analytic data for the series in the console
    """
    id_list = get_all_unique_series_ids()
    series_list = []

    for i in id_list:
        temp = get_events_by_series_id(i)
        temp = [i] + temp
        series_list.append(temp)

    count_total_entries = 0
    count_len_max3 = 0
    count_len_min10 = 0
    count_homepage = 0
    for i in series_list:
        print(len(i) - 1, " : ", i)
        count_total_entries += len(i) - 1
        if len(i) - 1 <= 3:
            count_len_max3 += 1
        elif len(i) - 1 >= 10:
            count_len_min10 += 1

        if len(i) > 1 and i[1]['homepage'] is not None:
            count_homepage += 1

    avg_series_length = count_total_entries / len(series_list)
    print("avg_series_length", avg_series_length)
    print("series with 3 or less: ", count_len_max3, str(count_len_max3 / len(series_list) * 100) + "%")
    print("series with 10 or more: ", count_len_min10, str(count_len_min10 / len(series_list) * 100) + "%")
    print("number of series: ", len(series_list))
    print("series with homepage: ", count_homepage, str(count_homepage / len(series_list) * 100) + "%")


all_series_analytics()
"""
# gets a specific series and prints its entries
series_Id_1 = "Q6053150"
series_Id_2 = "Q1961016"
series_Id_3 = "Q3570023"
series_Id_4 = "Q17012957"
series_Id_5 = "Q18353514"

series1 = get_events_by_series_id(series_Id_5)
for i in series1:
    print(i)
"""



