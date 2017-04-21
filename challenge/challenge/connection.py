import redis
from challenge.log import CustomLogger
from challenge.utils import Singleton


class RedisConnection(metaclass=Singleton):
    """
    This is a singleton class that creates a connection to Redis using the connection information from the [Redis] section of the *.ini* configuration files.
    
    Please keep the respective settings file updated to reflect your actual configuration.
    
    Parameters:
        :settings: The Settings object from config.Settings class
    """

    def __init__(self, settings):

        self.logger = CustomLogger(settings).get_logger()

        try:
            self.connection = redis.StrictRedis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
                socket_connect_timeout=10)

            assert self.connection.echo('ping') == b'ping'

        except AssertionError as ae:
            self.logger.error('Could not connect to Redis. Check that Redis is up and your settings are updated.')
            raise ae

        except Exception as e:
            self.logger.error(e)
            raise e

    def get_redis(self):
        """
        Returns the Redis connection
        
        :return: StrictRedis object
        """
        return self.connection
