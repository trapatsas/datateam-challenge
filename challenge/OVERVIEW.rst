Solution Overview
=================

Description
~~~~~~~~~~~

The solution is a command-line Python application.

For the application to run, the user must provide the appropriate settings in the "configuration/settings-[ENVIRONMENT].ini" file.

The application requires access to a running Redis server.

After setting the configuration, the user can start the application from the command line invoking the command:
``` python -m challenge ``` from the project root directory.

The application then initializes the Redis connection and tries to read the CSV input file, specified in Settings.

The method can handle GZIPed or plain text CSV files.

Batch processing
~~~~~~~~~~~~~~~~

The file is read piece by piece (in chunks), this way we avoid running out of memory, in case of very large files.

We can change the chunk size in Settings, too.

Each chunk is then converted to a Pandas dataframe and passed to our "search" function.

The "search" function loops through the dataframes records and queries Redis for each uuid, in order to find the closest iata airport code to this uuid.

Since most uuid points return a result at a radius of 50 km or less, we initially search for the closest airport inside this area.

For the uuid points that did not have any results inside the initial radius, we duplicate the radius and repeat the search.

The function runs recursively until all uuids find an airport *OR* until the max radius is reached.

If the max radius is reached and no airport codes were found, the application saves the uuid with an empty airport code as specified in the specs.

Initial and max radius can also be changed in the Settings file.

Finally, each part is saved in the output folder, as soon as it finishes processing. So, we might get more than one output files for each input file, depending on the chunk size, we have configured in Settings.

Logging
~~~~~~~

The application creates a logger and all errors and information messages during the run are saved in the "logs" folder.

Log files can be huge after some time, so we have created a logging policy, that creates a new file per hour and keeps only files for the last 3 days, to save space and performance.

Settings
~~~~~~~~

The application provides easy access to the configuration file properties. The Settings object creates a dynamic attribute named <SECTION>_<PROPERTY> for each property of the configuration file, so it's very easy to access the configuration properties inside our code.

Errors
~~~~~~

During runtime all errors are catched and logged in the application log files.


Testing
~~~~~~~

Disclaimer: Proper unit testing would require to mock or monkey patch the Redis calls, so as to eliminate the need for external resources during the unit tests.

Unfortunately, that would require some more time than that I had available to complete the solution. So, during the tests there is a requirement that the application has access to a redis server as specified in the "settings-test.ini" file.



Other findings
~~~~~~~~~~~~~~

I noticed that many uuid points are repeated throughout the file with different coordinates.
Since there were no explicit rules on how to handle this case,
the application saves only the last closest airport code for each uuid in a batch. So, it may happen to provide an input file with N uuids but get an output file with less entries.