import requests
from environment.EnvironmentConstants import EnvironmentVariables as ev
from knox_util import print
import traceback

def send_json_data_to_db(json_content: str, endpoint_name: str, headers: dict = {'content-type': 'application/json; charset=utf-8'}) -> bool:
    """
    Input:
        json_content: str - The JSON content to be sent and stored in the database as a single string
        endpoint_name: str - The name of the environment variable containing the endpoint information
        headers: dict - A dictionary containing the headers for the post requests (default: {'content-type': 'application/json'; charset=utf-8})
    Returns:
        success: bool - Indicates whether the sending of triple data to the database were successful

    Sends the JSON data to the Data layer database based on the provided headers and to the endpoint defined in the environment variables.
    Handles the case when a connection could not be established to the defined endpoints, in that case the function returns False
    """
    endpoint = ev.instance.get_value(endpoint_name)

    if not endpoint:
        msg = 'Endpoint for sending JSON data has not been set or configured in the environment variables, please define environment variable: <{}>'.format(endpoint_name)
        print(msg, 'error')
        raise EnvironmentError(msg)

    try:
        print('Sending POST request to endpoint <{}>, with headers <{}> and limited content <{}>'.format(endpoint, headers, json_content[0:min(25, len(json_content))]), 'debug')
        response: requests.Response = requests.post(url=endpoint, headers=headers, data=json_content.encode("utf-8"))
        if response.status_code == 200:
            print('Responded with status code <{}>, success...'.format(response.status_code), 'debug')
            return True
        else:
            print('Responded with status code <{}>. Message: <{}>'.format(response.status_code, response.text), 'warning')
            return False
    except requests.exceptions.ConnectionError as e: # Connection was refused return False
        print(f'Unable to connect to endpoint. {traceback.format_exc()}', 'error')
        return False
