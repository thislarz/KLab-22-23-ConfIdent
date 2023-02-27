import unittest
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema

from kgl_event_prediction.Analysis.WebsiteAnalytics import WebsiteAnalytics
from kgl_event_prediction.db_util import DbUtil


class TestWebsiteAnalytics(unittest.TestCase):

    def test_is_forbidden(self):
        test1 = BeautifulSoup("<head><title>403 Forbidden</title></head>", "html.parser")
        self.assertEqual(True, WebsiteAnalytics.is_forbidden(test1))

        test2 = BeautifulSoup("<head><title>Access Forbidden 403</title></head>", "html.parser")
        self.assertEqual(True, WebsiteAnalytics.is_forbidden(test2))

        test3 = BeautifulSoup("", "html.parser")
        self.assertEqual(True, WebsiteAnalytics.is_forbidden(test3))

        test4 = BeautifulSoup("<head><title>My normal page</title></head>", "html.parser")
        self.assertEqual(False, WebsiteAnalytics.is_forbidden(test4))

    def test_retrieve_website(self):
        # valid url
        url = "https://en.wikipedia.org/wiki/URL"
        title = WebsiteAnalytics.retrieve_website(url).head.title.text
        self.assertEqual("URL - Wikipedia", title)


if __name__ == '__main__':
    unittest.main()