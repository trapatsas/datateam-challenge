import os
import unittest
from collections import OrderedDict

import pandas as pd

from challenge.connection import RedisConnection
from challenge.core import Application
from configuration import config


class ApplicationSearchTest(unittest.TestCase):
    """
    This test verifies that the search function correctly returns the expected values in this demo uuid set.
    """

    def setUp(self):

        self.settings = config.Settings(environment='test')
        self.r = RedisConnection(self.settings).get_redis()

        self.app = Application(self.settings, self.r)

        self.r.flushdb()

        users = OrderedDict([
            ('uuid', ['DDEFEBEA-98ED-49EB-A4E7-9D7BFDB7AA0B', 'DAEF2221-14BE-467B-894A-F101CDCC38E4',
                      'E188A625-7B38-4FAF-A8F1-68ECE6FBB0F6', '30013CC6-E4A5-4C19-AF68-1FBA6110487F',
                      '540439C8-5B6D-4B35-80CE-37DAA20063B8', '25697C9D-958E-429B-BC83-2869867A14B9',
                      '2D7CA797-A494-42CF-8F78-E26AE2D5B2B0', 'D3012320-19DA-4FDC-8D4C-11A5A17BF060']),
            ('geoip_latitude', [-37.8333015441894, 52.5167007446289, 48.322601, 50.432598, 54.619701,
                                57.586399, 58.3353, 58.313099]),
            ('geoip_longitude', [145.050003051757, 4.66669988632202, 2.8859, 7.463, 39.740002,
                                 48.956902, 44.761902, 82.908897])
        ])

        self.usersDf = pd.DataFrame.from_dict(users)

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
        RELATIVE_DIR = os.path.relpath(BASE_DIR, os.getcwd())
        file_name = os.path.join(RELATIVE_DIR, 'tests', 'optd-sample-20161201.csv')

        airports = pd.read_csv(file_name)
        pipe = self.r.pipeline()
        [pipe.geoadd('iata', airports['longitude'][i], airports['latitude'][i], airports['iata_code'][i])
         for i in range(airports.shape[0])]
        pipe.execute()

    def tearDown(self):
        self.r.flushdb()

    def test_search_all(self):
        """
        Test that in 400 km range all uuids return result.
        """
        iata_results = self.app.search(self.usersDf, 50, 400, set())

        res_dict = {}
        for i in list(iata_results):
            res_dict[i[0]] = i[1]

        assert all(x for x in res_dict.values())

    def test_search_200(self):
        """
        Test that in 200 km range we get the expected results.
        """
        iata_results = self.app.search(self.usersDf, 50, 200, set())

        res_dict = {}
        for i in list(iata_results):
            res_dict[i[0]] = i[1]

        assert res_dict['540439C8-5B6D-4B35-80CE-37DAA20063B8'] == 'TYA'
        assert res_dict['DAEF2221-14BE-467B-894A-F101CDCC38E4'] == 'AMS'
        assert res_dict['D3012320-19DA-4FDC-8D4C-11A5A17BF060'] == ''
        assert res_dict['25697C9D-958E-429B-BC83-2869867A14B9'] == 'KVX'
        assert res_dict['DDEFEBEA-98ED-49EB-A4E7-9D7BFDB7AA0B'] == 'MBW'
        assert res_dict['2D7CA797-A494-42CF-8F78-E26AE2D5B2B0'] == ''
        assert res_dict['30013CC6-E4A5-4C19-AF68-1FBA6110487F'] == 'SGE'
        assert res_dict['E188A625-7B38-4FAF-A8F1-68ECE6FBB0F6'] == 'ORY'

    def test_search_100(self):
        """
        Test that in 100 km range we get the expected results.
        """
        iata_results = self.app.search(self.usersDf, 50, 100, set())

        res_dict = {}
        for i in list(iata_results):
            res_dict[i[0]] = i[1]

        assert res_dict['540439C8-5B6D-4B35-80CE-37DAA20063B8'] == ''
        assert res_dict['DAEF2221-14BE-467B-894A-F101CDCC38E4'] == 'AMS'
        assert res_dict['D3012320-19DA-4FDC-8D4C-11A5A17BF060'] == ''
        assert res_dict['25697C9D-958E-429B-BC83-2869867A14B9'] == ''
        assert res_dict['DDEFEBEA-98ED-49EB-A4E7-9D7BFDB7AA0B'] == 'MBW'
        assert res_dict['2D7CA797-A494-42CF-8F78-E26AE2D5B2B0'] == ''
        assert res_dict['30013CC6-E4A5-4C19-AF68-1FBA6110487F'] == 'SGE'
        assert res_dict['E188A625-7B38-4FAF-A8F1-68ECE6FBB0F6'] == 'ORY'

    def test_search_50(self):
        """
        Test that in 50 km range we get the expected results.
        """
        iata_results = self.app.search(self.usersDf, 50, 50, set())

        res_dict = {}
        for i in list(iata_results):
            res_dict[i[0]] = i[1]

        assert res_dict['540439C8-5B6D-4B35-80CE-37DAA20063B8'] == ''
        assert res_dict['DAEF2221-14BE-467B-894A-F101CDCC38E4'] == 'AMS'
        assert res_dict['D3012320-19DA-4FDC-8D4C-11A5A17BF060'] == ''
        assert res_dict['25697C9D-958E-429B-BC83-2869867A14B9'] == ''
        assert res_dict['DDEFEBEA-98ED-49EB-A4E7-9D7BFDB7AA0B'] == 'MBW'
        assert res_dict['2D7CA797-A494-42CF-8F78-E26AE2D5B2B0'] == ''
        assert res_dict['30013CC6-E4A5-4C19-AF68-1FBA6110487F'] == ''
        assert res_dict['E188A625-7B38-4FAF-A8F1-68ECE6FBB0F6'] == ''

    def test_search_1(self):
        """
        Test that in 1 km range we get the expected results.
        """
        iata_results = self.app.search(self.usersDf, 1, 1, set())

        res_dict = {}
        for i in list(iata_results):
            res_dict[i[0]] = i[1]

        assert all(x == '' for x in res_dict.values())


if __name__ == '__main__':
    unittest.main()
