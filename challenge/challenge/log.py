import os
from datetime import datetime

import logging.handlers

import sys

from challenge.utils import Singleton


class CustomLogger(metaclass=Singleton):
    """
    This is a singleton class that creates a logger with specific configuration.

    Please keep the respective settings file updated to reflect your actual configuration.

    Parameters:
        :settings: The Settings object from config.Settings class
    """

    def __init__(self, settings):
        self.environment = settings.info_environment
        self.logging_folder = settings.logging_folder
        self.logging_prefix = settings.logging_prefix

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
        RELATIVE_DIR = os.path.relpath(BASE_DIR, os.getcwd())
        LOGGING_DIR = os.path.join(BASE_DIR, self.logging_folder)

        if not os.path.exists(LOGGING_DIR):
            os.makedirs(LOGGING_DIR)

        self.log_filename = os.path.join(
            LOGGING_DIR, "{2}-{0}_{1}.log".format(
                self.logging_prefix,
                datetime.now().strftime('%Y-%m-%d-%H'),
                self.environment
            )
        )

        # Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
        # Give the logger a unique name (good practice)
        self.logger = logging.getLogger(__name__)
        # Set the log level to LOG_LEVEL
        self.logger.setLevel(logging.DEBUG)
        # Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
        handler = logging.handlers.TimedRotatingFileHandler(self.log_filename, when="midnight", backupCount=3)
        # Format each log message like this
        formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(module)s %(process)d %(thread)d %(message)s')
        # Attach the formatter to the handler
        handler.setFormatter(formatter)
        # Attach the handler to the logger
        self.logger.addHandler(handler)

        self.logger.info("""Initializing Logger...
         _____                   _    ___            _ _                      
        |_   _|                 | |  / _ \          | (_)                     
          | |_ __ __ ___   _____| | / /_\ \_   _  __| |_  ___ _ __   ___ ___  
          | | '__/ _` \ \ / / _ \ | |  _  | | | |/ _` | |/ _ \ '_ \ / __/ _ \ 
          | | | | (_| |\ V /  __/ | | | | | |_| | (_| | |  __/ | | | (_|  __/ 
          \_/_|  \__,_| \_/ \___|_| \_| |_/\__,_|\__,_|_|\___|_| |_|\___\___| 
                                                                              
        ______      _          _____            _                             
        |  _  \    | |        |  ___|          (_)                            
        | | | |__ _| |_ __ _  | |__ _ __   __ _ _ _ __   ___  ___ _ __        
        | | | / _` | __/ _` | |  __| '_ \ / _` | | '_ \ / _ \/ _ \ '__|       
        | |/ / (_| | || (_| | | |__| | | | (_| | | | | |  __/  __/ |          
        |___/ \__,_|\__\__,_| \____/_| |_|\__, |_|_| |_|\___|\___|_|          
                                           __/ |                              
         _____ _           _ _            |___/                               
        /  __ \ |         | | |                                               
        | /  \/ |__   __ _| | | ___ _ __   __ _  ___                          
        | |   | '_ \ / _` | | |/ _ \ '_ \ / _` |/ _ \                         
        | \__/\ | | | (_| | | |  __/ | | | (_| |  __/                         
         \____/_| |_|\__,_|_|_|\___|_| |_|\__, |\___|                         
                                           __/ |                              
                                          |___/                               
        """)

        if not (sys.version_info >= (3, 2)):
            self.logger.error('Wrong Python version: {}'.format(sys.version_info))
            raise Exception("Please use Python version 3.2 or greater.")

        self.logger.info('Project root path set at: [{}]'.format(BASE_DIR))
        self.logger.info('Current path set at: [{}]'.format(RELATIVE_DIR))

    def get_logger(self):
        """
        
        :return: The logger object
        """
        return self.logger
