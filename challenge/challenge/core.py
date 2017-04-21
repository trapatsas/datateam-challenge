# -*- coding: utf-8 -*-

import csv
import os

import pandas as pd

from challenge.log import CustomLogger


class Application:
    """
    Core Application class
    
    This class provides the functionality to:
    - Read the csv in plain text or gzip format
    - Save output to csv files as soon as it is processed
    - Query Redis using the Geo API to get the closest iata airport code
    
    Parameters:
        :settings: The Settings object from config.Settings class
        :redis_connection: The connection to Redis
    """

    def __init__(self, settings, redis_connection):
        self.settings = settings
        self.redis_conn = redis_connection
        self.logger = CustomLogger(settings).get_logger()

    @staticmethod
    def read_csv_in_chunks(filename, chunk_size):
        """Lazy function (generator) to read a file piece by piece (in chunks).
        
        This way we avoid running out of memory, in case of very large files.
        
        :filename: Path to the file containing the uuid and coordinates
        :chunk_size: Default chunk size: 100k. Change in configuration file
        """
        chunks = pd.read_csv(filename, chunksize=chunk_size, iterator=True)
        for chunk in chunks:
            chunk.reset_index(inplace=True)
            yield chunk

    @staticmethod
    def persist_output(chunk, out_dir, out_file):
        """
        
        :chunk: Pandas dataframe
        :out_dir: Directory to save output
        :out_file: The output file name. If a file with this name exists, we increase the filename by 1.
        """
        file_path = os.path.join(out_dir, out_file)
        i = 0
        while os.path.exists(file_path.format(i)):
            i += 1
        with open(file_path.format(i), 'w', newline='') as csvfile:
            set_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in chunk:
                set_writer.writerow(list(row))

    def get_closest(self, chunk, radius):
        """
        
        :chunk: Pandas dataframe
        :radius: Radius to search
        :return: A dictionary containing the pairs (uuid, closest airport code)
        """
        pipe = self.redis_conn.pipeline()

        [pipe.georadius('iata',
                        chunk['geoip_longitude'][i], chunk['geoip_latitude'][i], radius,
                        'km', count=1) for i in range(chunk.shape[0])]

        values = pipe.execute()
        result_dict = {}

        for i in range(chunk.shape[0]):
            result_dict[chunk['uuid'][i]] = {'point': [chunk['geoip_latitude'][i], chunk['geoip_longitude'][i]],
                                             'nearest': values[i][0] if values[i] else None}

        return result_dict

    def search(self, chunk, radius, max_radius, final_results):
        """
        A recursive function that tries to find the closest airport inside the given radius.
        Uuids that do not have any airport inside the radius are saved in a dataframe and additional searches are made only for them using a greater radius.
        
        The function runs recursively until all uuids find an airport *OR* until the max radius is reached.
    
        :max_radius: The maximum radius to search inside
        :chunk: Pandas Dataframe: A dataframe with the uuids and their coordinates
        :radius: Integer: The radius to search for airports
        :final_results: Set: The set that will be returned
        :return: Set: A set of uuids and their closest airport
        """
        failed = pd.DataFrame()
        partial_result = self.get_closest(chunk, radius)
        for key, val in partial_result.items():
            if not val.get('nearest'):
                failed = failed.append(
                    pd.DataFrame(
                        {'uuid': [key], 'geoip_latitude': [val['point'][0]], 'geoip_longitude': [val['point'][1]]},
                        columns=['uuid', 'geoip_latitude', 'geoip_longitude']
                    ),
                    ignore_index=True
                )
            else:
                final_results.add((key, val.get('nearest')))
        if failed.empty:
            self.logger.info('Sending {} hits in output'.format(len(final_results)))
            return final_results
        else:
            radius *= 2
            if radius > max_radius:
                self.logger.warning('Maximum radius exceeded. Please check that iata airports are inserted')
                for i in range(failed.shape[0]):
                    final_results.add((failed['uuid'][i], ""))
                return final_results
            self.logger.info('Missed {} uuids. Trying at {} km'.format(len(failed), radius))

            return self.search(failed, radius, max_radius, final_results)