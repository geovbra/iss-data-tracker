from flask import Flask, jsonify
import xmltodict
import logging
import socket
format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=format_str)

app = Flask(__name__)

iss_epoch_data = {}
iss_sighting_data = {}

def is_data_loaded() -> bool:
    '''
    Checks if the global variables iss_epoch_data and iss_sighting_data are populated with data (not empty).

    Returns:
        A boolean representing whether both variables contain information. Only returns true when both (not one) of
        the variables have data.
    '''

    return iss_epoch_data and iss_sighting_data 

def all_key_values(list_of_dicts: list, key: str) -> str:
    '''
    Finds all of the unique values for a given key inside a list of dictionaries. Handles option listing for routes
    in this project.

    Args:
        list_of_dicts: A list of data dictionaries.
        key: A string representing the keyword to use to find values in each data dictionary.

    Returns:
        A string (representing a list formatted in JSON) of all of the unique values found in the data dictionaries.
    '''

    values = []
    for curr_dict in list_of_dicts:
        if curr_dict[key] not in values:
            values.append(curr_dict[key])
    return jsonify(values)

def all_key_value_data(list_of_dicts: list, key: str , value: str) -> str:
    '''
    Finds all of the dictionaries in a list of dictionaries that contain a specific key/value pair. Handles data
    listing for routes in this project.

    Args:
        list_of_dicts: A list of data dictionaries.
        key: A string representing the keyword to use in each data dictionary.
        value: A string representing the value to check each data dictionary for.

    Returns:
        A string (representing a list formatted in JSON) of all of the data dictionaries that contain the key/value
        pair.
    '''

    data = []
    for curr_dict in list_of_dicts:
        if curr_dict[key] == value:
            data.append(curr_dict)
    return jsonify(data)

@app.route('/', methods = ['GET'])
def help() -> str:
    '''
    Provides all of the routes that can be used to interact with the ISS data in this project.

    Returns:
        A string representing the routes used to load and navigate through the positional and sighting data.
    '''

    logging.info('returning all routes')

    return '\n    ISS TRACKER\n\n\
    Informational and management routes:\n\n\
    /                                                            (GET) print this information\n\
    /load                                                        (POST) load data in from files to memory\n\n\
    Routes for querying positional and velocity data:\n\n\
    /epochs                                                      (GET) list all epochs\n\
    /epochs/<epoch>                                              (GET) all data on a specific epoch\n\n\
    Routes for querying sighting data:\n\n\
    /countries                                                   (GET) list all countries\n\
    /countries/<country>                                         (GET) all data on sightings in country\n\
    /countries/<country>/regions                                 (GET) list all regions in country\n\
    /countries/<country>/regions/<region>                        (GET) all data on sightings in region\n\
    /countries/<country>/regions/<region>/cities                 (GET) list all cities in region\n\
    /countries/<country>/regions/<region>/cities/<city>          (GET) all data on sightings in city\n\n'

@app.route('/epochs', methods = ['GET'])
def all_epochs() -> str:
    '''
    Finds all of the epochs in iss_epoch_data.
    
    Returns:
        A string representing the list of epochs whose data can be displayed.
    '''

    logging.info('returning all epochs')

    if not is_data_loaded():
        return 'WARNING: Data not loaded into memory, use a POST request to the route /load\n'
    return all_key_values(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'], 'EPOCH')

@app.route('/epochs/<epoch>', methods = ['GET'])
def epoch_data(epoch: str) -> str:
    '''
    Finds all of the data associated with a specific epoch in iss_epoch_data.

    Args:
        epoch: A string representing the epoch used to search the data.

    Returns:
        A string representing the data dictionary associated with the epoch.
    '''

    logging.info(f'returning epoch {epoch}')

    if not is_data_loaded():
        return 'WARNING: Data not loaded into memory, use a POST request to the route /load\n'
    return all_key_value_data(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'], 'EPOCH', epoch)

@app.route('/countries', methods = ['GET'])
def all_countries() -> str:
    '''
    Finds all of the countries in iss_sighting_data.

    Returns:
        A string representing the list of countries whose data can be displayed.
    '''

    logging.info('returning all countries')

    if not is_data_loaded():
        return 'WARNING: Data not loaded into memory, use a POST request to the route /load\n'
    return all_key_values(iss_sighting_data['visible_passes']['visible_pass'], 'country')

@app.route('/countries/<country>', methods = ['GET'])
def country_data(country: str) -> str:
    '''
    Finds all of the data associated with a specific country in iss_sighting_data.

    Args:
        country: A string representing the country used to search the data.

    Returns:
        A string representing the list of data dictionaries associated with the country.
    '''

    logging.info(f'returning data for {country}')

    if not is_data_loaded():
        return 'WARNING: Data not loaded into memory, use a POST request to the route /load\n'
    return all_key_value_data(iss_sighting_data['visible_passes']['visible_pass'], 'country', country)

@app.route('/countries/<country>/regions', methods = ['GET'])
def all_regions(country: str) -> str:
    '''
    Finds all of the regions in a specific country in iss_sighting_data.

    Args:
        country: A string representing the country used to search the data.

    Returns:
        A string representing the list of regions in a country whose data can be displayed.
    '''

    logging.info(f'returning all regions in {country}')

    if not is_data_loaded():
        return 'WARNING: Data not loaded into memory, use a POST request to the route /load\n'
    country_sightings = []
    for sighting in iss_sighting_data['visible_passes']['visible_pass']:
        if sighting['country'] == country:
            country_sightings.append(sighting)
    return all_key_values(country_sightings, 'region')

@app.route('/countries/<country>/regions/<region>', methods = ['GET'])
def region_data(country: str, region: str) -> str:
    '''
    Finds all of the data associated with a specific region in iss_sighting_data.

    Args:
        country: A string representing the country used to search the data.
        region: A string representing the region used to search the data.

    Returns:
        A string representing the list of data dictionaries associated with the region.
    '''

    logging.info(f'returning data for {region}')

    if not is_data_loaded():
        return 'WARNING: Data not loaded into memory, use a POST request to the route /load\n'
    country_sightings = []
    for sighting in iss_sighting_data['visible_passes']['visible_pass']:
        if sighting['country'] == country:
            country_sightings.append(sighting)
    return all_key_value_data(country_sightings, 'region', region)

@app.route('/countries/<country>/regions/<region>/cities', methods = ['GET'])
def all_cities(country: str, region: str) -> str:
    '''
    Finds all of the cities in a specific region in iss_sighting_data.

    Args:
        country: A string representing the country used to search the data.
        region: A string representing the region used to search the data.

    Returns:
        A string representing the list of cities in a region whose data can be displayed.
    '''

    logging.info(f'returning all cities in {region}')

    if not is_data_loaded():
        return 'WARNING: Data not loaded into memory, use a POST request to the route /load\n'
    country_sightings = []
    for sighting in iss_sighting_data['visible_passes']['visible_pass']:
        if sighting['country'] == country and sighting['region'] == region:
            country_sightings.append(sighting)
    return all_key_values(country_sightings, 'city')

@app.route('/countries/<country>/regions/<region>/cities/<city>', methods = ['GET'])
def city_data(country: str, region: str, city: str) -> str:
    '''
    Finds all of the data associated with a specific city in iss_sighting_data.

    Args:
        country: A string representing the country used to search the data.
        region: A string representing the region used to search the data.
        city: A string representing the city used to search the data.

    Returns:
        A string representing the list of data dictionaries associated with the city.
    '''

    logging.info(f'returning data for {city}')

    if not is_data_loaded():
        return 'WARNING: Data not loaded into memory, use a POST request to the route /load\n'
    country_sightings = []
    for sighting in iss_sighting_data['visible_passes']['visible_pass']:
        if sighting['country'] == country and sighting['region'] == region:
            country_sightings.append(sighting)
    return all_key_value_data(country_sightings, 'city', city)

@app.route('/load', methods = ['GET'])
def no_load() -> str:
    '''
    Informs the user to perform a POST request instead of a GET request to the /load route.

    Returns:
        A string representing the necessary request correction to this route.
    '''

    return 'Please perform a POST request to this route to properly load the data\n'

@app.route('/load', methods = ['POST'])
def load() -> str:
    '''
    Loads positional and tracking data into iss_epoch_data and iss_sighting_data.

    Returns:
        A string representing the successful operation of loading data into the global variables.
    '''
    logging.info('loading data')


    global iss_epoch_data
    global iss_sighting_data
    
    with open( 'ISS.OEM_J2K_EPH.xml', 'r') as f:
        iss_epoch_data = xmltodict.parse(f.read())

    with open( 'XMLsightingData_citiesINT05.xml', 'r') as f:
        iss_sighting_data = xmltodict.parse(f.read())

    return 'Data has been read from files\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
