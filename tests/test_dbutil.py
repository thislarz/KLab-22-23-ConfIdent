import pathlib
import unittest
from kgl_event_prediction.db_util import DbUtil
from kgl_event_prediction.event import Event


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

    def test_get_series_by_acronym(self):
        test_cases = [
            (
                'ISWC',
                'event_orclone',
                Event(title='21th International Semantic Web Conference', year=2022, acronym='ISWC 2022',
                      homepage='https://iswc2022.semanticweb.org/', series_id=''),
                "Unexpexted result for ISWC on event_orclone"
            ),
            (
                'ISWC',
                'event_wikidata',
                Event(title='The 21th International Semantic Web Conference', year=2022, acronym='ISWC 2022',
                      homepage='http://iswc2022.semanticweb.org', series_id=''),
                "Unexpected result for ISWC on event_wikidata"
            ),
            (
                'DUI',
                'event_orclone',
                Event(title='IEEE Symposium on 3D User Interfaces', year=2020, acronym='3DUI 2020',
                      homepage='http://ieeevr.org/2020/', series_id=''),
                "Unexpected result for DUI on event_orclone"
            ),
            (
                'AIM',
                'event_orclone',
                Event(title='AIM  2017 : International Conference on Advanced Intelligent Mechatronics', year=2017,
                      acronym='AIM 2017', homepage='http://www.aim2017.org/', series_id=''),
                "Unexpected result for AIM on event_orclone"
            ),
            (
                'AIME',
                'event_orclone',
                Event(title='20th International Conference on Artificial Intelligence in Medicine', year=2022,
                      acronym='AIME 2022', homepage='https://aime22.aimedicine.info/', series_id=''),
                "Unexpected result for AIME on event_orclone"
            )
        ]

        for acro, tabel, expected, msg in test_cases:
            db = DbUtil(tabel)
            res = db.get_series_by_acronym(acro)
            if expected is None:
                self.assertEqual(res, [], msg)
            else:
                self.assertEqual(res[0], expected, msg)

    def test_get_all_striped_acronyms(self):
        db = DbUtil('event_orclone')
        res = db.get_all_striped_acronyms()
        self.assertEqual(res[0:8], ['DUI', 'IA', 'PGIC', 'SD', 'GU', 'GWN', 'AAAI', 'AAAIHBM'])

    def test_get_all_series_by_acronym(self):
        db = DbUtil('event_orclone')
        acro_list = db.get_all_striped_acronyms()[0:5]
        res = db.get_all_series_by_acronym(acro_list)
        expected = [
            Event(title='IEEE Symposium on 3D User Interfaces', year=2020, acronym='3DUI 2020',
                  homepage='http://ieeevr.org/2020/', series_id=''),
            Event(title='12th International Conference on Computer Graphics and Artificial Intelligence', year=2009,
                  acronym='3IA 2009', homepage='http://3ia.teiath.gr', series_id=''),
            Event(title='International Workshop on P2P, Parallel, Grid and Internet Computing', year=2010,
                  acronym='3PGIC 2010', homepage='http://www.lsi.upc.edu/~fatos/3PGIC-2010/', series_id=''),
            Event(title='2nd EAI International Conference on 5G for Ubiquitous Connectivity', year=2017,
                  acronym='5GU 2017', homepage='http://5guconference.org/2017/show/cf-papers', series_id='')
        ]
        for i in range(0, 4):
            self.assertEqual(res[i][0], expected[i])

    def test_make_sql_safe(self):
        db = DbUtil('event_orclone')
        self.assertEqual('Hello World', db.make_sql_safe('Hello Worl\'d'))

    def test_sort_events_by_year(self):
        db = DbUtil('event_orclone')
        a = [
            Event('C', year=2010),
            Event('D', year=20),
            Event('B', year=2016),
            Event('A', year=3010),
        ]
        b = [
            Event('A', year=3010),
            Event('B', year=2016),
            Event('C', year=2010),
            Event('D', year=20),
        ]
        self.assertEqual(b, db.sort_events_by_year(a))


if __name__ == '__main__':
    unittest.main()