import requests
from urllib.parse import urljoin

def get_api(drone_id: str=None):
    BASEURL = "http://localhost:8000/api/v1/"
    DRONEAPI = "drones/"
    FLIGHTAPI = "flights/"
    if drone_id:
        TESTID = drone_id
    else:
        TESTID = "6c27c6a3-455a-4c2a-872b-505f9c38f582" # DRONE ID for testing
    username = "seanhong2000"
    password = "Susksysc2"
    HEADER = {

    }
    AUTHENTICATION = {
        "method": "POST",
        "url": "auth/token/login",
        "username": username,
        "password": password,

    }

    drone_content = requests.get(urljoin(base=BASEURL, url=DRONEAPI))
    
    current_drone_data = {}
    for result in drone_content.json()['results']:
        if result['id'] == TESTID:
            current_drone_data = result
            break
        
    flight_content = requests.get(urljoin(base=BASEURL, url=FLIGHTAPI))
    flight_path = []
    for result in flight_content.json()['results']:
        if result['id'] == current_drone_data['flight']:
            flight_path = result['flight_path']
            break

    return flight_path


if '__main__' == __name__:
    get_api()
