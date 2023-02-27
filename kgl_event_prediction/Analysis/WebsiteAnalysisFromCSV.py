import json
import pathlib
import pandas as pd
from tabulate import tabulate

from kgl_event_prediction.db_util import DbUtil


class WebsiteAnalysisFromCSV(object):
    def __init__(self, name: str):
        self.df = pd.read_csv(str(pathlib.Path(__file__).parent.parent) + "/resources/analysis_results/" + name + ".csv", keep_default_na=False)

    def count_field(self, field_name: str):
        temp = self.df.loc[self.df[field_name]!=""]
        out = "There are " + str(len(temp)) + " entries not null in column \"" + field_name+"\""
        print(out)

    def add_year(self):
        """
        Note this method of adding years is not perfect since it joins on url and they are not unique and thus wrong
        years can be attributed
        """
        query = "Select homepage as url, year From event_orclone WHERE homepage IS NOT NULL"
        temp = DbUtil.query_corpus_db(query)
        temp_df = pd.DataFrame(temp).drop_duplicates('url')
        self.df = pd.concat([self.df.set_index('url',drop=False), temp_df.set_index('url')], axis=1, join='inner', ignore_index=False)
        self.df.set_index('Unnamed: 0', inplace=True)

    def drop_dublicate_urls(self):
        self.df.drop_duplicates('url', inplace=True)

    def count_none_unique_urls(self):
        unique = self.df['url'].unique()
        none_unique_count = self.df.shape[0] - unique.shape[0]
        print("There are " + str(none_unique_count)+" none unique URLs")

    def infere_type(self):
        f = open(str(pathlib.Path(__file__).parent.parent) + "/resources/generator_extraction_dict.json")
        comparison_dict = json.load(f)

        self.df['generator_family'] = ""

        print(self.df['generator'][9])
        for i in range(0, self.df.shape[0]):

            generator = self.df.iloc[i]['generator']
            if generator != "":
                for x in comparison_dict:
                    if generator.find(x) != -1:
                        self.df.loc[i, 'generator_family'] = x
                        break

    def count_generator_families(self):
        f = open(str(pathlib.Path(__file__).parent.parent) + "/resources/generator_extraction_dict.json")
        comparison_dict = json.load(f)

        out = pd.DataFrame(columns=['generator_family', 'count'])

        for fam in comparison_dict:
            count = self.df.loc[self.df['generator_family'] == fam].shape[0]
            out = pd.concat([out, pd.DataFrame({'generator_family': [fam], 'count': [count]})])

        out.to_csv(str(pathlib.Path(__file__).parent.parent) + "/resources/analysis_results/generator_counts.csv")

    def most_used_in_year(self):
        f = open(str(pathlib.Path(__file__).parent.parent) + "/resources/generator_extraction_dict.json")
        comparison_dict = json.load(f)

        columns = [
                    'year',
                    "WordPress",
                    "Joomla",
                    "Drupal",
                    "TYPO3",
                    "Wix",
                    "Jekyll",
                    "Hugo",
                    "Plone",
                    "GoLive",
                    "HTML Tidy",
                    "Tiki Wiki CMS",
                    "SPIP",
                    "RapidWeaver",
                    "MediaWiki",
                    "blogger",
                    "Go Daddy",
                    "SilverStripe"
                  ]

        out = pd.DataFrame(columns=columns)
        start_year = 1960
        end_year = int(self.df['year'].max())

        for year in range(start_year, end_year):
            temp = self.df[self.df['generator_family'] != ""]
            temp = temp[temp['year'] == float(year)]
            if temp.shape[0] == 0:
                out = pd.concat([out, pd.DataFrame({'year': [year]})])
            else:
                gen = temp['generator_family'].value_counts().to_frame(name="").transpose()
                print(gen.keys())
                print(type(gen),gen)
                gen['year'] = year
                out = pd.concat([out, gen])

        out.to_csv(str(pathlib.Path(__file__).parent.parent) + "/resources/analysis_results/generator_most_common.csv")


if __name__ == "__main__":
    wa = WebsiteAnalysisFromCSV('head_01')
    wa.count_field('url')
    wa.count_field('generator')
    wa.count_field('title')
    wa.drop_dublicate_urls()
    wa.add_year()
    print(wa.df.dtypes)
    print(tabulate(wa.df[0:10:], headers="keys"))
    wa.infere_type()

    wa.most_used_in_year()
