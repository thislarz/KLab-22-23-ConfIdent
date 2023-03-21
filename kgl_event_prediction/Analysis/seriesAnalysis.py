import json
import pathlib
from datetime import time
from logging import Logger, DEBUG, StreamHandler
from tabulate import tabulate
import sys

from kgl_event_prediction.Evaluator.eventEvaluator import EventEvaluator
from kgl_event_prediction.Predictors.eventPredictor import EventPredictor
from kgl_event_prediction.Predictors.multiGuessEventPredictor import MultiGuessEventPredictor
from kgl_event_prediction.Predictors.simpleEventPredictor import SimpleEventPredictor
from kgl_event_prediction.resources.ordinalNumbers import OrdinalNumbers
from kgl_event_prediction.utils import *
from kgl_event_prediction.db_util import DbUtil


class SeriesAnalysis(object):
    def __init__(self):
        self.logger = Logger(name="Steve")
        self.logger.setLevel(DEBUG)
        self.logger.addHandler(StreamHandler(sys.stdout))

        self.id_list = []
        self.series_list = []

    def load_series(self, source: str, table: str):
        """
        runs queries to load all series entries (takes some time)
        """
        if source == "series_id" and table == "event_wikidata":
            id_list = DbUtil.get_all_unique_series_ids()

            for i in id_list:
                temp = DbUtil.get_events_by_series_id(i)
                self.series_list.append(temp)
        elif source == "acronym":
            db = DbUtil(table)
            acro_list = db.get_all_striped_acronyms()
            self.series_list = db.get_all_series_by_acronym(acro_list)

    def all_series_analytics(self):
        """
        :print: analytic data for the series in the console (configured to work on event_wikidata)
        """

        count_total_entries = 0
        count_len_max3 = 0
        count_len_min10 = 0
        count_homepage = 0
        for i in self.series_list:
            print(len(i) - 1, " : ", i)
            count_total_entries += len(i) - 1
            if len(i) - 1 <= 3:
                count_len_max3 += 1
            elif len(i) - 1 >= 10:
                count_len_min10 += 1

            if len(i) > 0 and i[0].homepage is not None:
                count_homepage += 1

        avg_series_length = count_total_entries / len(self.series_list)
        print("avg_series_length", avg_series_length)
        print("series with 3 or less: ", count_len_max3, str(count_len_max3 / len(self.series_list) * 100) + "%")
        print("series with 10 or more: ", count_len_min10, str(count_len_min10 / len(self.series_list) * 100) + "%")
        print("number of series: ", len(self.series_list))
        print("series with homepage: ", count_homepage, str(count_homepage / len(self.series_list) * 100) + "%")

    def homepage_analytics(self):
        count_series = len(self.series_list)
        url_containing_year_4dig = 0
        url_containing_year_2dig = 0
        url_containing_striped_acronym = 0
        empty_series = 0
        no_urls = 0
        for event_series in self.series_list:
            if event_series:
                url = event_series[0].homepage
                year = event_series[0].year
                short_year = int(event_series[0].year/100)
                acro_striped = strip_acronym(event_series[0].acronym)

                if type(url) is not str:
                    no_urls += 1
                    continue
                if url.find(str(year)) != -1:
                    url_containing_year_4dig += 1
                elif url.find(str(short_year)) != -1:
                    url_containing_year_2dig += 1
                if type(acro_striped) is str and url.find(acro_striped) != -1:
                    url_containing_striped_acronym += 1
            else:
                empty_series += 1
        res = {
            "count_series": count_series,
            "count_year_4dig": url_containing_year_4dig,
            "count_year_2dig": url_containing_year_2dig,
            "count_acronym": url_containing_striped_acronym,
            "empty_series": empty_series,
            "no_urls": no_urls
        }
        print(res)
        return res


    @staticmethod
    def evaluate_dates_in_field(event_list: list):
        list_init = []
        for x in range(0, 30):
            list_init.append(0)

        nums_title = list_init.copy()
        nums_accronym = list_init.copy()
        nums_homepage = list_init.copy()
        count_title_empty = 0
        count_accronym_empty = 0
        count_homepage_empty = 0

        for event in event_list:
            if event.title == "" or event.title is None:
                count_title_empty += 1
            else:
                temp_title = count_numerals(event.title)
                nums_title[temp_title] += 1

            if event.acronym == "" or event.acronym is None:
                count_accronym_empty += 1
            else:
                temp_accronym = count_numerals(event.acronym)
                nums_accronym[temp_accronym] += 1

            if event.homepage == "" or event.homepage is None:
                count_homepage_empty += 1
            else:
                temp_homepage = count_numerals(event.homepage)
                nums_homepage[temp_homepage] += 1

        print("empty_title", count_title_empty)
        print("Nums_title")
        print(nums_title)
        print("empty_accronym", count_accronym_empty)
        print("Nums_accronym")
        print(nums_accronym)
        print("empty_homepage", count_homepage_empty)
        print("Nums_homepage")
        print(nums_homepage)

        total_events = len(event_list)
        res_dict = {
            "percent_empty_title": round(count_title_empty/total_events, 4),
            "percent_empty_acronym": round(count_accronym_empty/total_events, 4),
            "percent_empty_homepage": round(count_homepage_empty / total_events, 4),
            "numeral_list_title": nums_title,
            "numeral_list_acronym": nums_accronym,
            "numeral_list_homepage": nums_homepage
        }
        return res_dict

    def predict_event(self, event_predictor: EventPredictor, series_id: str):
        """
        :event_predictor: EventPredictor: any subclass of EventPredictor to be used in predicting Event
        :series_id: str: the id of the series where the next event should be predicted

        :print: prints the next event and some additional information
        """
        event_predictor.initialize(series_id)
        next_event = event_predictor.get_next_event()
        conf_event = EventEvaluator(next_event).is_title_valid()
        self.logger.debug(tabulate([next_event], headers="keys"))
        print(EventEvaluator.get_title_from_url(next_event.homepage), "<-> web title")
        print(conf_event, "<-> is title valid? ")

    def rate_event_prediction(self, event_predictor: EventPredictor, threshold: float = 0.8):
        total_events = len(self.series_list)
        empty_series = 0
        title_similarity = []
        title_similarity_sampling_size = 20
        for i in range(0, title_similarity_sampling_size):
            title_similarity.append(0)
        year_checks = 0
        acronym_checks = 0
        verdicts = [0, 0, 0, 0]

        # run prediction on all series
        for i in range(0,len(self.series_list)):

            print(str(i)+" out of "+str(total_events)+" completed.")

            if not self.series_list[i]:
                empty_series += 1
                continue
            event_predictor.initialize(self.series_list[i])
            summary = event_predictor.get_summery(threshold=threshold)

            # updated results
            i = int(summary['title_similarity']*title_similarity_sampling_size)
            if i == len(title_similarity):
                i = i-1
            title_similarity[i] += 1

            if summary['year_check']:
                year_checks += 1

            if summary['acronym_check']:
                acronym_checks += 1

            if summary['verdict'] == "good":
                verdicts[0] += 1
            elif summary['verdict'] == "okay":
                verdicts[1] += 1
            elif summary['verdict'] == "bad":
                verdicts[2] += 1
            elif summary['verdict'] == "not_found":
                verdicts[3] += 1

            if i % 20 == 0:
                print({
                    "total_events": total_events,
                    "empty_series": empty_series,
                    "title_similarity": title_similarity,
                    "year_checks": year_checks,
                    "acronym_checks": acronym_checks,
                    "verdicts": verdicts
                })
        res = {
            "total_events": total_events,
            "empty_series": empty_series,
            "title_similarity": title_similarity,
            "year_checks": year_checks,
            "acronym_checks": acronym_checks,
            "verdicts": verdicts
        }
        SeriesAnalysis.save_to_json(res, name="rate_event_predictor", append=True)
        print(res)
        return res

    def rate_event_evaluator(self, threshold: float = 0.8):
        total_events = len(self.series_list)
        empty_series = 0
        title_similarity = []
        title_similarity_sampling_size = 20
        for i in range(0, title_similarity_sampling_size):
            title_similarity.append(0)
        year_checks = 0
        acronym_checks = 0
        verdicts = [0, 0, 0, 0]

        # run prediction on all series
        for i in range(0, len(self.series_list)):

            print(str(i) + " out of " + str(total_events) + " completed.")

            if not self.series_list[i]:
                empty_series += 1
                continue

            # gets first event
            event = self.series_list[i][0]
            event_evaluator = EventEvaluator(event)
            summary = event_evaluator.summarize_event(threshold=threshold)

            # updated results
            i = int(summary['title_similarity'] * title_similarity_sampling_size)
            if i == len(title_similarity):
                i = i - 1
            title_similarity[i] += 1

            if summary['year_check']:
                year_checks += 1

            if summary['acronym_check']:
                acronym_checks += 1

            if summary['verdict'] == "good":
                verdicts[0] += 1
            elif summary['verdict'] == "okay":
                verdicts[1] += 1
            elif summary['verdict'] == "bad":
                verdicts[2] += 1
            elif summary['verdict'] == "not_found":
                verdicts[3] += 1

            if i % 20 == 0:
                print({
                    "total_events": total_events,
                    "empty_series": empty_series,
                    "title_similarity": title_similarity,
                    "year_checks": year_checks,
                    "acronym_checks": acronym_checks,
                    "verdicts": verdicts
                })
        res = {
            "total_events": total_events,
            "empty_series": empty_series,
            "title_similarity": title_similarity,
            "year_checks": year_checks,
            "acronym_checks": acronym_checks,
            "verdicts": verdicts
        }
        SeriesAnalysis.save_to_json(res, name="rate_event_evaluator", append=True)
        print(res)
        return res

    @staticmethod
    def or_analytics(last_years: int):
        print("--------------------------")
        db = DbUtil("event_orclone")
        res = db.get_last_x_events(last_years)
        total_events = len(res)
        print(res[0])

        print(total_events, " Events in last", last_years, " years")

        # detect bad data
        fake_hp = []
        empty_title = []
        for event in res:
            if SeriesAnalysis.url_is_homepage(event.homepage) is False:
                fake_hp.append(event)
            if event.title == "" or event.title is None:
                empty_title.append(event)

        print(len(fake_hp), " fake homepages detected**", round(len(fake_hp)/total_events*100, 2), "%")
        print(len(empty_title), " events have empty titles", round(len(empty_title) / total_events * 100, 2), "%")

        # remove bad data
        for event in fake_hp+empty_title:
            try:
                res.remove(event)
            except:
                None

        acronym_doubles = len(SeriesAnalysis.count_acronym_doubles(event_list=res, ignore_years=False))
        print(acronym_doubles, " Acronyms occur at least twice")

        # count word numerals
        numeral_count = 0
        for event in res:
            if SeriesAnalysis.find_word_numerals(event.title):
                numeral_count += 1
        print(numeral_count, " at least events have a written numeral in title.", len(res), " total events")

        # will return a list of series
        db.group_by_acronym(res)

        res_dict = {
            "total_events": total_events,
            "fake_homepages": len(fake_hp),
            "empty_titles": len(empty_title),
            "acronyms_doubled": acronym_doubles,
            "numerals": numeral_count
        }
        return res_dict

    @staticmethod
    def count_acronym_doubles(event_list: list, ignore_years: bool):
        unique_list = []
        duplicate_list = []
        for event in event_list:

            # remove years from acronyms
            acr = event.acronym
            if ignore_years is False:
                acr = ""
                try:
                    temp = event.acronym.split(' ')
                except:
                    temp = ""

                for x in temp:
                    if x.isnumeric() is False:
                        acr += x

            if acr in unique_list:
                duplicate_list.append(event)

            else:
                unique_list.append(acr)

        return duplicate_list

    @staticmethod
    def find_word_numerals(text: str):
        ord_list = OrdinalNumbers().get_ordinal_list()

        # uppercase text to process
        text = text.lower()

        snippet_list = text.split(' ')
        for snippet in snippet_list:
            if snippet in ord_list:
                return True
        return False



    @staticmethod
    def url_is_homepage(url: str):
        """
        checks if the url includes terms that are associated with alternative event references
        """
        fakes = ["elsevier", "springer", "inderscience", "dblp", "wikicfp.com"]
        for f in fakes:
            if url.find(f) != -1:
                return False
        return True

    @staticmethod
    def general_cc_analytics():
        """
        provides general insight into a broad range of datasets
        """
        SeriesAnalysis.cc_analytics("event_wikidata")
        SeriesAnalysis.cc_analytics("event_orclone")
        SeriesAnalysis.cc_analytics("event_or")
        # SeriesAnalysis.cc_analytics("event_ceurws")

        SeriesAnalysis.cc_analytics("eventseries_orclone")


    @staticmethod
    def cc_analytics(table: str):
        """
        prints general information of a dataset. Configured to handle different datasets.
        Slave to general_cc_analytics
        """

        all = "title"
        url = "homepage"
        series = ""
        date = ""
        year = ""
        if table == "event_wikidata":
            series = "eventInSeriesId"
            year = "year"
        elif table == "event_orclone":
            series = "inEventSeries"
            year = "year"
        elif table == "event_or":
            series = "inEventSeries"
            date = "startDate"
            year = "year"
        elif table == "event_ceurws":
            url = "url"

        print("----------"+table+"-------------")
        total_events = SeriesAnalysis.count_column_in_table(table, all)
        events_homepages = SeriesAnalysis.count_column_in_table(table, url)
        events_series_id = SeriesAnalysis.count_column_in_table(table, series)
        try:
            events_date = SeriesAnalysis.count_column_in_table(table, date)
        except Exception:
            events_date = 0

        try:
            events_year = SeriesAnalysis.count_column_in_table(table, year)
        except Exception:
            events_year = 0

        homepage_percent = round(events_homepages / total_events*100, 3)
        series_id_percent = round(events_series_id / total_events*100, 3)
        year_percent = round(events_year / total_events*100, 3)
        date_percent = round(events_date / total_events*100, 3)

        print(total_events, " : Total number of entries")
        print(events_homepages, " : Total number of entries with Homepages", "-", homepage_percent, "% of Total")
        if series != "":
            print(events_series_id, " : Total number of entries with a linked series", "-", series_id_percent,
                  "% of Total")
        if date != "":
            print(events_date, " : Total number of entries with a date", "-", date_percent,
                  "% of Total")
        print(events_year, " : Total number of entries with a year", "-", year_percent, "% of Total")

        res_dict = {
            "total_events": total_events,
            "events_homepages": events_homepages,
            "events_series_id": events_series_id,
            "events_date": events_date,
            "events_year": events_year
        }
        return res_dict

    @staticmethod
    def count_column_in_table(table: str, column: str):
        """
        counts entries in a specific column of a dataset (where that column is not NULL)
        """
        query = open("../resources/queries/countSeriesVariable.sql").read()
        query = replace_var_in_sql(query, "VARIABLE1", column)
        query = replace_var_in_sql(query, "VARIABLE2", table)
        return DbUtil.query_corpus_db(query)[0]["COUNT("+column+")"]

    @staticmethod
    def save_to_json(res: dict, name: str, append: bool = True):
        """
        @param res: is a dict with the analysis results
        @param name: name under which the file should be saved
        """

        path = str(pathlib.Path(__file__).parent.parent) + "/resources/analysis_results/" + name+".json"

        json_object = json.dumps(res, indent=4)

        if not append:
            try:
                with open(path, "w") as outfile:
                    outfile.write(json_object)
            except FileNotFoundError:
                with open(path, "x") as outfile:
                    outfile.write(json_object)
        else:
            cur = ""
            try:
                with open(path, "r") as outfile:
                    cur = outfile.read()
            except FileNotFoundError:
                cur = ""

            if cur != "" and len(cur) > 2:
                cur = cur[:len(cur)-2]
                cur += ',\n'
            else:
                cur += "[\n"
            cur += str(json_object)
            cur += "\n]"

            try:
                with open(path, "w") as outfile:
                    outfile.write(cur)
            except FileNotFoundError:
                with open(path, "x") as outfile:
                    outfile.write(cur)


if __name__ == '__main__':
    sa = SeriesAnalysis()
    sa.load_series('acronym', 'event_wikidata')
    sa.rate_event_prediction(event_predictor=MultiGuessEventPredictor(), threshold=0.8)


