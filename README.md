# ISS Positional and Sighting Data

## Overview

This repository contains instructions and resources to use a containerized Flask program which allows the user to navigate two databases: one containing positional data for the International Space Station, and the other containing ground sighting data of the ISS from a subset of countries.

The data used in this project can be found here:

https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq

The databases taken from here are the `Public Distribution File` and `XMLsightingData_citiesINT05`

## File Explanation

The repository consists of two python scripts, a Dockerfile, and a Makefile.

The first python script, app.py, sets up a REST API using Flask along with multiple routes to interact with the two ISS databases. The second script, test_app.py, is simply a unit test suite for the functions inside app.py.

The Dockerfile provides a quick method to build and run the containerized application, but a pre-containerized copy of the app can also be pulled from DockerHub. Both methods will be discussed below.

The Makefile provides shortcuts to many Docker commands, allowing the application to be built with greater ease if desired. The corresponding Makefile shortcut command will be provided as an alternative to each of the Docker commands moving forward.

## Requirements

To start, it is necessary to either use the included Dockerfile or pull a copy from DockerHub. For the second option, simply enter one of the two following commands into the terminal:

```
   make pull

   docker pull geovbra/flask_iss_tracker:1.0
```

This retrieves the container image from DockerHub and allows you to begin running the program.

Alternatively, you can use the Dockerfile included in this folder to build an image yourself, provided you have the two python scripts in the same directory:

```
   make build

   docker build -t geovbra/flask_iss_tracker:1.0 .
```

## Running the Program

When you are ready to run the containerized project, use one of the following commands:

```
   make run

   docker run --name "geovbra_iss" -d -p 5005:5000 geovbra/flask_iss_tracker:1.0
```

This will start the API and allow you to begin interacting with the databases. To check, use one of the following commands:

```
   make ps

   docker ps -a | grep geovbra
```

Something resembling the following should be returned:

```
<numbers&letters>   geovbra/flask_iss_tracker:1.0           "python app.py"          6 seconds ago   Up 4 seconds              0.0.0.0:5005->5000/tcp, :::5005->5000/tcp   geovbra_iss
```

## Interacting with ISS Data

To send requests to the API, use the `curl localhost:5005/<route here>` command. We can get a list of useful routes with the following command:

```
   curl localhost:5005/
```

This gives us the following message:

```
    ISS TRACKER

    Informational and management routes:

    /                                                            (GET) print this information
    /load                                                        (POST) load data in from files to memory

    Routes for querying positional and velocity data:

    /epochs                                                      (GET) list all epochs
    /epochs/<epoch>                                              (GET) all data on a specific epoch

    Routes for querying sighting data:

    /countries                                                   (GET) list all countries
    /countries/<country>                                         (GET) all data on sightings in country
    /countries/<country>/regions                                 (GET) list all regions in country
    /countries/<country>/regions/<region>                        (GET) all data on sightings in region
    /countries/<country>/regions/<region>/cities                 (GET) list all cities in region
    /countries/<country>/regions/<region>/cities/<city>          (GET) all data on sightings in city
```

In order to interact with the data, it must first be loaded using the following command:

```
   curl localhost:5005/load -X POST
```
Note that this is the only route requiring the request type POST, so the `-X POST` must be included at the end. If not added, you will be prompted by the API to correct your mistake. Additionally, every other route will not function before you load the data and will prompt you to do this step before moving on.

Sample commands and outputs:

```
[geovbra]$ curl localhost:5005/countries
[
  "Turkey",
  "UAE",
  "Uganda",
  "Ukraine",
  "United_Kingdom",
  "Uruguay",
  "Uzbekistan",
  "Venezuela",
  "Vietnam",
  "Yemen",
  "Zambia",
  "Zimbabwe"
]
[geovbra]$ curl localhost:5005/countries/United_Kingdom/regions
[
  "Ascension_Island",
  "England",
  "Gibraltar",
  "Grand_Cayman",
  "Guernsey",
  "Indian_Ocean_Terr",
  "Isle_of_Man",
  "Northern_Ireland",
  "Scotland",
  "Virgin_Islands",
  "Wales"
]
[geovbra]$ curl localhost:5005/countries/United_Kingdom/regions/Wales/cities
[
  "Aberystwyth",
  "Barmouth",
  "Beaumaris",
  "Cardiff",
  "Denbigh",
  "Holyhead",
  "Llandudno",
  "Newport",
  "Saundersfoot",
  "Swansea",
  "Wrexham"
]
[geovbra]$ curl localhost:5005/countries/United_Kingdom/regions/Wales/cities/Swansea
[
  {
    "city": "Swansea",
    "country": "United_Kingdom",
    "duration_minutes": "3",
    "enters": "10 above SSE",
    "exits": "10 above ESE",
    "max_elevation": "12",
    "region": "Wales",
    "sighting_date": "Sat Feb 19/06:05 AM",
    "spacecraft": "ISS",
    "utc_date": "Feb 19, 2022",
    "utc_offset": "0.0",
    "utc_time": "06:05"
  },
# etc.
```

## Closing the Program

Make sure to end the application when you're finished with it via the following two commands:

```
   make stop
   make rm

   docker stop geovbra_iss
   docker rm geovbra_iss
```