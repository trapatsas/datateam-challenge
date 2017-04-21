import os
import string
import unittest
import random

from challenge.connection import RedisConnection
from challenge.core import Application
from configuration import config


class ApplicationReadTest(unittest.TestCase):
    """
    Test for verifying that csv is read correctly in chunks of the right size, that contain the right uuid column.

    """

    def setUp(self):
        self.content = 'uuid,geoip_latitude,geoip_longitude\nDDEFEBEA-98ED-49EB-A4E7-9D7BFDB7AA0B,-37.8333015441'+\
        '8945,145.0500030517578\nDAEF2221-14BE-467B-894A-F101CDCC38E4,52.51670074462891,4.666699886322021\nE188A625'+\
        '-7B38-4FAF-A8F1-68ECE6FBB0F6,48.322601,2.8859\n30013CC6-E4A5-4C19-AF68-1FBA6110487F,50.432598,7.463\n54043'+\
        '9C8-5B6D-4B35-80CE-37DAA20063B8,54.619701,39.740002\n25697C9D-958E-429B-BC83-2869867A14B9,57.586399,48.956'+\
        '902\n2D7CA797-A494-42CF-8F78-E26AE2D5B2B0,58.3353,44.761902\nD3012320-19DA-4FDC-8D4C-11A5A17BF060,58.31309'
        '9,82.908897\n'
        self.filename = os.path.join('tests',
                                     'test_{}.csv'.format(
                                         ''.join(random.sample(string.ascii_uppercase + string.digits, k=5))
                                     ))
        with open(self.filename, "w") as file:
            file.write(self.content)

        self.settings = config.Settings(environment='test')
        r = RedisConnection(self.settings).get_redis()

        self.app = Application(self.settings, r)


    def tearDown(self):
        os.remove(self.filename)

    def test_read_csv_in_chunks(self):
        '''
        Assert that file is read in chunks 
        that each of them has size equal 
        to chunk_size from settings
        '''
        chunks = self.app.read_csv_in_chunks(self.filename,
                                             int(self.settings.input_chunk_size))
        cnt = 0
        for chunk in chunks:
            cnt += 1
            assert len(chunk['uuid'][0]) == 36
            assert len(chunk) == 2
        assert cnt == 4


if __name__ == '__main__':
    unittest.main()