import os
import unittest
from collections import OrderedDict

import pandas as pd

from challenge.connection import RedisConnection
from challenge.core import Application
from configuration import config


class ApplicationCloseFullTest(unittest.TestCase):
    """
    Verify that queries return the expected result in this small test set
    """

    def setUp(self):

        self.settings = config.Settings(environment='test')
        self.r = RedisConnection(self.settings).get_redis()

        self.app = Application(self.settings, self.r)

        users = OrderedDict([
        ('uuid', ['DDEFEBEA-98ED-49EB-A4E7-9D7BFDB7AA0B', 'DAEF2221-14BE-467B-894A-F101CDCC38E4',
                  'E188A625-7B38-4FAF-A8F1-68ECE6FBB0F6', '30013CC6-E4A5-4C19-AF68-1FBA6110487F',
                  '540439C8-5B6D-4B35-80CE-37DAA20063B8', 	'25697C9D-958E-429B-BC83-2869867A14B9',
                  '2D7CA797-A494-42CF-8F78-E26AE2D5B2B0', 	'D3012320-19DA-4FDC-8D4C-11A5A17BF060']),
        ('geoip_latitude', [-37.8333015441894, 	52.5167007446289, 	48.322601, 	50.432598, 	54.619701,
                            57.586399, 	58.3353, 	58.313099]),
        ('geoip_longitude', [145.050003051757, 	4.66669988632202, 	2.8859, 	7.463, 	39.740002,
                             48.956902, 	44.761902, 	82.908897])
        ] )

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


    def test_get_closest_all(self):
        """
        Verify that at 400 km radius all uuids return a value
        """
        iata_results = self.app.get_closest(self.usersDf, 400)

        assert all(point.get('nearest') for point in iata_results.values())

    def test_get_closest_200(self):
        """
        Verify that at 200 km radius all uuids return the correct values
        """
        iata_results = self.app.get_closest(self.usersDf, 200)

        assert iata_results['540439C8-5B6D-4B35-80CE-37DAA20063B8'].get('nearest') == 'TYA'
        assert iata_results['DAEF2221-14BE-467B-894A-F101CDCC38E4'].get('nearest') == 'AMS'
        assert iata_results['D3012320-19DA-4FDC-8D4C-11A5A17BF060'].get('nearest') == None
        assert iata_results['25697C9D-958E-429B-BC83-2869867A14B9'].get('nearest') == 'KVX'
        assert iata_results['DDEFEBEA-98ED-49EB-A4E7-9D7BFDB7AA0B'].get('nearest') == 'MBW'
        assert iata_results['2D7CA797-A494-42CF-8F78-E26AE2D5B2B0'].get('nearest') == None
        assert iata_results['30013CC6-E4A5-4C19-AF68-1FBA6110487F'].get('nearest') == 'SGE'
        assert iata_results['E188A625-7B38-4FAF-A8F1-68ECE6FBB0F6'].get('nearest') == 'ORY'

    def test_get_closest_100(self):
        """
        Verify that at 100 km radius all uuids return the correct values
        """
        iata_results = self.app.get_closest(self.usersDf, 100)

        assert iata_results['540439C8-5B6D-4B35-80CE-37DAA20063B8'].get('nearest') == None
        assert iata_results['DAEF2221-14BE-467B-894A-F101CDCC38E4'].get('nearest') == 'AMS'
        assert iata_results['D3012320-19DA-4FDC-8D4C-11A5A17BF060'].get('nearest') == None
        assert iata_results['25697C9D-958E-429B-BC83-2869867A14B9'].get('nearest') == None
        assert iata_results['DDEFEBEA-98ED-49EB-A4E7-9D7BFDB7AA0B'].get('nearest') == 'MBW'
        assert iata_results['2D7CA797-A494-42CF-8F78-E26AE2D5B2B0'].get('nearest') == None
        assert iata_results['30013CC6-E4A5-4C19-AF68-1FBA6110487F'].get('nearest') == 'SGE'
        assert iata_results['E188A625-7B38-4FAF-A8F1-68ECE6FBB0F6'].get('nearest') == 'ORY'

    def test_get_closest_50(self):
        """
        Verify that at 50 km radius all uuids return the correct values
        """
        iata_results = self.app.get_closest(self.usersDf, 50)

        assert iata_results['540439C8-5B6D-4B35-80CE-37DAA20063B8'].get('nearest') == None
        assert iata_results['DAEF2221-14BE-467B-894A-F101CDCC38E4'].get('nearest') == 'AMS'
        assert iata_results['D3012320-19DA-4FDC-8D4C-11A5A17BF060'].get('nearest') == None
        assert iata_results['25697C9D-958E-429B-BC83-2869867A14B9'].get('nearest') == None
        assert iata_results['DDEFEBEA-98ED-49EB-A4E7-9D7BFDB7AA0B'].get('nearest') == 'MBW'
        assert iata_results['2D7CA797-A494-42CF-8F78-E26AE2D5B2B0'].get('nearest') == None
        assert iata_results['30013CC6-E4A5-4C19-AF68-1FBA6110487F'].get('nearest') == None
        assert iata_results['E188A625-7B38-4FAF-A8F1-68ECE6FBB0F6'].get('nearest') == None

    def test_get_closest_1(self):
        """
        Verify that at 1 km radius all uuids return None
        """
        iata_results = self.app.get_closest(self.usersDf, 1)

        assert all(not point.get('nearest') for point in iata_results.values())


if __name__ == '__main__':
    unittest.main()