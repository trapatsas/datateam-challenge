# travel audience Data Engineer Challenge

## The Objective

To build an efficient script that uses geoip information (provided) to find the
closest airport to a given user based on their IP address.

## Data-sets

You will be provided with three data sets to consume:

    * `maxmind-sample-20161201.csv.gz` - A simplified version of a larger data set provided for free by geolocation provider Maxmind Inc., containing the following:
        * IPv4 range block in CIDR notation (first column)
        * Latitude and Longitude in floating point format (second and third columns, respectively)
        * The coordinates represent an approximate location of any device with an IP address belonging to the given range.

    * `optd-sample-20161201.csv.gz` - A simplified version of a data set from Open Travel Data, containing geo-coordinates of major airports:
        * IATA airport code - a three-character identifier of global airports (first column)
        * Latitude and Longitude in floating point format (second and third columns, respectively)
        * The coordinates represent the location of the airport represented by the IATA code.

    * `sample_data.csv.gz` - Some sample input data for your script, containing:
        * A universally unique identifier (uuid) which identifies some end-user
        * An IPv4 ip address belonging to this user. 
        * For this challenge you need not concern yourself with the precice details of the uuid data and can simply treat it as a unique string key.

All data samples are provided in gzip format for the purposes of efficient data-storage, however it is beyond the scope of this excercise to build gzip decoding/encoding into your script. In other words it is perfectly acceptable for your script to read and write uncompressed csvs.

## Input

Your script is expected to parse a csv file in the same format as sample_data.csv.gz described above.

## Output

Your script is expected to generate an output csv file containing one line of output for each line of input. The output line is to contain the uuid from the input file and a corresponding IATA code for output. If no match can be found, an empty string should be returned in place of the IATA code. (This should only happen if the ip address is invalid or otherwise does not correspond to a range available in the database csv).

# Task.

Your script will need to do the following. Use of open-source, third-party libraries is highly encouraged:

    * Perform the basic core functionality:

        * Parse and understand the input csv.

        * Load the ip- and airport-geolocation data into some internal, in-memory data structure.

        * IP block matching. For each incoming row (user and ip address) you will need to first match an IP address to an IP block. For example 12.34.56.78 belongs to block 12.34.0.0/16. 

        * Geodistance calculation. Having identified the IP block, you will have an approximation of the user coordinates. You must now compare this with the set of airport coordinates to identify the airport and IATA code with the closest geodistance.

        * Write out the uuid of the user and IATA code of the airport.

    * Be capable of performing large batch-jobs efficiently.

    * Be easily adaptable for parllelisation (though you do not need to implement parallelisation for the purposes of this task)

    * Contain good test coverage.

    * Include basic documentation.

# Delvierables 

The purpose of this task is to provide code which satisfies the task above whilst at the same time demonstrating your coding style and engineering skills. 

# Environment

You have a free hand in choosing the environment in which this code is developed and demonstrated

# Languages

Must be in Scala, Python, Java, Golang or Perl.

# Licencing 

* `maxmind-sample-20161201.csv.gz`

This work is licensed under the Creative Commons
Attribution-ShareAlike 4.0 International License. To view a copy of
this license, visit http://creativecommons.org/licenses/by-sa/4.0/.

This database incorporates GeoNames [http://www.geonames.org]
geographical data, which is made available under the Creative Commons
Attribution 3.0 License. To view a copy of this license, visit
http://www.creativecommons.org/licenses/by/3.0/us/.

* `optd-sample-20161201.csv.gz`

Licensed under Creative Commons - for more information see 
https://github.com/opentraveldata/optd/blob/trunk/LICENSE

* All other data

All other data in this repository is Copyright travel audience GmbH. 


