import unittest

import kgl_event_prediction.utils as ut


class TestUtil(unittest.TestCase):
    def test_count_numerals(self):
        self.assertEqual(ut.count_numerals('2th Conference 2023'), 5)

    #def test_get_all_unique_series_ids(self):
    # event_wikidata has 8026 entries and 2060 DISTINCT entries
    # entry 0: Q70971474
    # entry last: Q105694587
    #   all_entries = kgl_event_prediction.utils.get_all_unique_series_ids()
    #  self.assertEqual(all_entries[0], 'Q70971474')

    def test_strip_acronym(self):
        self.assertEqual('', ut.strip_acronym(' 01265438910'))


if __name__ == '__main__':
    unittest.main()
