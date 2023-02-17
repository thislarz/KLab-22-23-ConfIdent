import pathlib
import unittest
from kgl_event_prediction.db_util import DbUtil


class TestDbUtil(unittest.TestCase):

    def test_get_events_by_series_id(self):
        db = DbUtil('event_wikidata')
        res = db.get_events_by_series_id('Q18353514')
        self.assertEqual(res[0].title, 'The 2021 Conference on Empirical Methods in Natural Language Processing')

    def test_convert_to_event(self):
        test_event_dict = {
            "title": "TestTitle",
            "homepage": "TestHomepage",
            "acronym": "TestAcronym"
        }
        converted = DbUtil.convert_to_event(test_event_dict)

        self.assertEqual(converted.title, test_event_dict['title'])
        self.assertEqual(converted.homepage, test_event_dict['homepage'])
        self.assertEqual(converted.year, 0)

    def test_query_corpus_db(self):
        test_query = "SELECT title FROM event_wikidata WHERE title IS 'ESWC 2021'"
        res = DbUtil.query_corpus_db(test_query)
        self.assertEqual(res, [{'title': 'ESWC 2021'}])

    def test_get_event_by_acronym(self):
        db = DbUtil('event_orclone')
        res = db.get_event_by_acronym("AAMAS 2016")
        self.assertEqual(res.title, "International Conference on Autonomous Agents & Multiagent Systems")

        res2 = db.get_event_by_acronym("ESWC 2021")
        self.assertEqual('ESWC 2021', res2.acronym)


if __name__ == '__main__':
    unittest.main()