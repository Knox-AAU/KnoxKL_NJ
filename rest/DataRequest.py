import requests
from environment.EnvironmentConstants import EnvironmentVariables as ev
from knox_util import print
import traceback

def send_triple_to_db(triple_content: str, headers: dict = {'content-type': 'application/json'}, endpoint: str = None) -> bool:
    """
    Input:
        triple_content: str - The triple content to be stored in the database formatted as a single string
        headers: dict - A dictionary containing the headers for the post requests (default: {'content-type': 'application/json'})
        endpoint: str - The endpoint for the REST call (default: None, means check environment variables)
    Returns:
        success: bool - Indicates whether the sending of triple date to the database were successful

    Sends the triple data to the Data layer database based on the provided headers and to the endpoint defined in the environment variables.
    Handles the case when a connection could not be established to the defined endpoints, in that case the function returns False
    """
    if not endpoint: # Endpoint has not been defined, use environment variables, if exists
        endpoint = ev.instance.get_value(ev.instance.TRIPLE_DATA_ENDPOINT)

    if not endpoint:
        msg = 'Endpoint for sending triple data has not been set or configured in the environment variables, please define environment variable: <{}>'.format(ev.instance.TRIPLE_DATA_ENDPOINT)
        print(msg, 'error')
        raise EnvironmentError(msg)

    try:
        print('Sending POST request to endpoint <{}>, with headers <{}> and limited content <{}>'.format(endpoint, headers, triple_content[0:min(25, len(triple_content))]), 'debug')
        response: requests.Response = requests.post(url=endpoint, headers=headers, data=triple_content)
        if response.status_code == 200:
            print('Responded with status code <{}>, success...'.format(response.status_code), 'debug')
            return True
        else:
            print('Responded with status code <{}>'.format(response.status_code), 'warning')
            return False
    except requests.exceptions.ConnectionError as e: # Connection was refused return False
        print(f'Unable to connect to endpoint. {traceback.extract_tb()}', 'error')
        return False