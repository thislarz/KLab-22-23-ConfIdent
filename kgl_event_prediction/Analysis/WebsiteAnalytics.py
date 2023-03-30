import pathlib
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json

from kgl_event_prediction.db_util import DbUtil


class WebsiteAnalytics(object):

    @staticmethod
    def retrieve_website_list(website_list: list, timeout: float = 1):
        """
        @param website_list: list of urls to be retrieved
        @return: list of dict with keys url and res where res contains the html content of said url
        """
        retrieved_websites = []
        forbidden_list = []
        none_existing_lsit = []
        failed_list = []
        i= 0
        t = len(website_list)
        for url in website_list:

            # status report
            if i % 20 == 0:
                print("---------------------------")
                print("Completion: ", round(i/t, 2))
                print("Forbidden: ", len(forbidden_list))
                print("Not reachable: ", len(none_existing_lsit))
                print("Failed: ", len(failed_list))
                print("Success: ", len(retrieved_websites))
            i += 1

            try:
                res = WebsiteAnalytics.retrieve_website(url, timeout)
            except:
                failed_list.append(url)
                continue
            if WebsiteAnalytics.is_forbidden(res):
                forbidden_list.append(url)
                continue
            elif WebsiteAnalytics.is_not_reachable(res):
                none_existing_lsit.append(url)
                continue
            retrieved_websites.append({
                "url": url,
                "res": res
            })
        print("---- Finished------")
        print("Forbidden: ", len(forbidden_list))
        print("Not reachable: ", len(none_existing_lsit))
        print("Failed: ", len(failed_list))
        print("Success: ", len(retrieved_websites))
        return retrieved_websites

    @staticmethod
    def retrieve_website(url: str, timeout: float = 1):
        res = requests.get(url, timeout=timeout)
        event_page = BeautifulSoup(res.text, "html.parser")
        return event_page

    @staticmethod
    def extract_head_list(html_text_list):
        for i in range(0, len(html_text_list)):
            html_text_list[i]['res'] = WebsiteAnalytics.extract_head(html_text_list[i]['res'])

        return html_text_list

    @staticmethod
    def extract_head(html_text):
        """
        @param html_text: a beautiful soup parsed website content
        @return: just the head element;
        """
        try:
            return html_text.head
        except:
            return None


    @staticmethod
    def save_to_json(data_list: list, name: str = str(datetime.now().timestamp())+".json"):
        """
        @param data_list: is a list of where every entry has key value pairs
        @param name: name under which the file should be saved
        """
        for i in range(0,len(data_list)):
            data_list[i]['res'] = str(data_list[i]['res'])

        json_object = json.dumps(data_list, indent=4)

        with open(str(pathlib.Path(__file__).parent.parent)+"/resources/analysis_results/"+name, "w") as outfile:
            outfile.write(json_object)

    @staticmethod
    def is_not_reachable(html_text):
        """
        @param html_text: a beautiful soup parsed website content
        @return: True if 404; False if title is not 404;
        """
        try:
            title = html_text.head.title.text
        except:
            return True

        if title.find("404") != -1:
            return True
        else:
            return False

    @staticmethod
    def is_forbidden(html_text):
        """
        @param html_text: a beautiful soup parsed website content
        @return: True if access forbidden or other weird stuff happend; False if title is not 403;
        """
        try:
            title = html_text.head.title.text
        except:
            # print(html_text)
            return True

        if title.find("403") != -1:
            return True
        else:
            return False

    @staticmethod
    def retrieve_headers_from_web_and_save_to_json():
        query = "Select homepage From event_orclone WHERE homepage IS NOT NULL"
        temp = DbUtil.query_corpus_db(query)
        print(len(temp))
        url_list2 = []
        for x in temp:
            url_list2.append(x['homepage'])
        print(len(url_list2), "url_list2")
        res = WebsiteAnalytics.retrieve_website_list(url_list2)

        res = WebsiteAnalytics.extract_head_list(res)
        WebsiteAnalytics.save_to_json(res)

    @staticmethod
    def load_data_from_json():
        with open(str(pathlib.Path(__file__).parent.parent) + "/resources/analysis_results/" + "or_clone_headers.json") as json_file:
            return json.load(json_file)

    @staticmethod
    def head_analytic_main(data):
        # convert to bs4 object
        for i in range(0, len(data)):
            data[i]['res'] = BeautifulSoup(data[i]['res'], "html.parser")

        num_entries = len(data)

        meta_res = {
            'total_count': len(data),
            'has_meta_count': 0,
            'has_generator': 0
        }
        for el in data:
            has_meta = WebsiteAnalytics.has_tag(el, 'meta')
            if has_meta:
                meta_res['has_meta_count'] += 1

        print(meta_res)

    @staticmethod
    def extract_specific_head_data_to_file(data, name: str = "head_"+str(datetime.now().timestamp())+".csv"):
        """
        Method should extract title, generator, and add url this should all be saved in a specified path
        """
        # create Dataframe
        df = pd.DataFrame(columns=["url", "title", "generator"])

        # convert to bs4 objects
        for i in range(0, len(data)):
            data[i]['res'] = BeautifulSoup(data[i]['res'], "html.parser")

        for i in range(0,len(data)):
            url = data[i]['url']
            title = ""
            generator = ""
            if WebsiteAnalytics.has_tag(data[i], 'title'):
                title = data[i]['res'].title.text
            if WebsiteAnalytics.has_tag(data[i], 'meta'):
                generator = WebsiteAnalytics.extract_generator(data[i]['res'].head)

            # create Dataframe and add it to df
            temp_df = pd.DataFrame({"url": [url], "title": [title], "generator": [generator]})
            df = pd.concat([df, temp_df], ignore_index=True)

        df.to_csv(str(pathlib.Path(__file__).parent.parent)+"/resources/analysis_results/"+name)

    @staticmethod
    def has_tag(data, tag_name: str):
        """
        @params data: is of type dict with keys: 'url' and 'res' where 'res' value is a bs4 header object
        @params tag_name: the html tag that is checked for
        """
        tag_list = [str(tag.name) for tag in data['res'].find_all()]

        try:
            has_tag = tag_list.index(tag_name) != -1
        except ValueError:
            has_tag = False

        if has_tag:
            return True
        else:
            return False


    @staticmethod
    def get_uniques(tag_list: list):
        temp = []
        for x in tag_list:
            if x not in temp:
                temp.append(x)
        return temp

    @staticmethod
    def extract_generator(head):
        """
        @params head: a bs4 html head element
        @return: string containing the name of the specified generator if none specified return empty string
        """
        generator = ""
        meta_tag_list = head.find_all('meta')
        for i in meta_tag_list:
            temp_dict = i.attrs
            if 'name' in temp_dict.keys() != -1:
                if temp_dict['name'] == 'generator':
                    generator += temp_dict['content']
        return generator


if __name__ == '__main__':
    query = """
    SELECT homepage
    FROM "event_orclone"
    WHERE homepage IS NOT NULL
    """
    web_list = DbUtil('event_orclone').query_corpus_db(query)
    print(web_list[0])
    temp = []
    for url in web_list:
        temp.append(url['homepage'])
    WebsiteAnalytics.retrieve_website_list(temp, 1)


