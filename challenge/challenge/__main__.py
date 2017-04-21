"""
Core Application Module
=======================
"""
import argparse
import os
from time import perf_counter

import pandas as pd

from challenge.connection import RedisConnection
from challenge.core import Application
from challenge.log import CustomLogger
from configuration import config


def main():
    """
    The main routine.
    """

    parser = argparse.ArgumentParser(
        description='Script populates Redis with iata airport codes and then queries the database to find the closest airport for a given pair of lat/long coordinates'
    )
    parser.add_argument('-e', '--environment', default='production',
                        help='Sets the environment. Relevant settings file MUST exist.')

    parser.add_argument('-p', '--populate', default='yes',
                        help='Populates Redis with the available iata codes. Values: yes|no')

    args = parser.parse_args()

    settings = config.Settings(environment=vars(args).get('environment'))

    populate = vars(args).get('populate') == 'yes'

    challenge_logger = CustomLogger(settings).get_logger()

    RESULT = 'N/A'

    try:
        r = RedisConnection(settings).get_redis()

        app = Application(settings, r)

        if populate:
            BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
            RELATIVE_DIR = os.path.relpath(BASE_DIR, os.getcwd())

            file_name = os.path.join(RELATIVE_DIR, 'tests', 'optd-sample-20161201.csv')

            airports = pd.read_csv(file_name)
            pipe = r.pipeline()
            [pipe.geoadd('iata', airports['longitude'][i], airports['latitude'][i], airports['iata_code'][i])
             for i in range(airports.shape[0])]
            pipe.execute()

        start_time = perf_counter()

        for part in app.read_csv_in_chunks(settings.input_file_path, int(settings.input_chunk_size)):
            outset = app.search(part, int(settings.geo_initial_radius), int(settings.geo_max_radius), set())
            challenge_logger.info('@@@ persisting {} results'.format(len(outset)))

            app.persist_output(outset, settings.output_directory, settings.output_filename)

        end_time = perf_counter()

        RESULT = 'SUCCESS'

        challenge_logger.info("Execution time: {} seconds".format(end_time - start_time))

    except Exception as e:
        challenge_logger.error("** ERROR **: {}".format(e))
        RESULT = 'ERRORS'
        raise
    finally:
        challenge_logger.info("Script finished with: {}".format(RESULT))


if __name__ == '__main__':
    raise SystemExit(main())
