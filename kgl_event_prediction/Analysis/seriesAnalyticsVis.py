from kgl_event_prediction.db_util import DbUtil
from kgl_event_prediction.Analysis.seriesAnalysis import SeriesAnalysis
import matplotlib.pyplot as plt


class SeriesAnalyticsVis(object):

    @staticmethod
    def cc_analytics_vis():

        SeriesAnalyticsVis.cc_analytics_pie_chart("event_orclone")
        SeriesAnalyticsVis.cc_analytics_pie_chart("event_wikidata")
        plt.show()

    @staticmethod
    def cc_analytics_pie_chart(table: str):
        # retrieve data
        or_clone = SeriesAnalysis.cc_analytics(table)

        # plot data
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'keine Homepage', 'Homepage'
        no_homepage = or_clone['total_events'] - or_clone['events_homepages']
        sizes = [no_homepage, or_clone['events_homepages']]
        explode = (0, 0.1)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    @staticmethod
    def cc_numeral_analysis(table: str, save: bool = False):
        print('------'+table+'----------')
        db = DbUtil(table)
        event_list = db.get_all_events()

        res = SeriesAnalysis.evaluate_dates_in_field(event_list)

        if res is None:
            raise ValueError ("results are None")
        else:
            SeriesAnalyticsVis.plot_list(res['numeral_list_title'], "title", table, save)
            SeriesAnalyticsVis.plot_list(res['numeral_list_acronym'], "acronym", table, save)
            SeriesAnalyticsVis.plot_list(res['numeral_list_homepage'], "homepage", table, save)

    @staticmethod
    def plot_list(num_list: list, title: str, datasource: str, save: bool = False):
        labels = []
        for i in range(0, len(num_list)):
            labels.append(str(i))

        fig = plt.figure(figsize=(10, 5))
        plt.bar(labels, num_list)
        plt.title("numerals in "+title+" - data from "+datasource)
        plt.ylabel("occurrences")
        plt.xlabel("count of numerals in "+title)
        if save is True:
            plt.savefig("../docs/workdoc/plots/numerals_in_" + title + "_" + datasource + ".png")
        plt.show()


if __name__ == '__main__':
    SeriesAnalyticsVis.cc_numeral_analysis('event_wikidata', save=True)
    SeriesAnalyticsVis.cc_numeral_analysis('event_orclone', save=True)
