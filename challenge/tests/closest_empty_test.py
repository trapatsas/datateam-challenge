import unittest
from collections import OrderedDict

import pandas as pd

from challenge.connection import RedisConnection
from challenge.core import Application
from configuration import config


class ApplicationCloseEmptyTest(unittest.TestCase):
    """
    Verify that with an empty Redis, all uuid queries return None    
    """

    def setUp(self):

        self.settings = config.Settings(environment='test')
        self.r = RedisConnection(self.settings).get_redis()

        self.app = Application(self.settings, self.r)

        self.r.flushdb()

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


    def tearDown(self):
        self.r.flushdb()


    def test_get_closest(self):
        iata_results = self.app.get_closest(self.usersDf, int(self.settings.geo_max_radius))

        assert any(not point.get('nearest') for point in iata_results.values())


if __name__ == '__main__':
    unittest.main()