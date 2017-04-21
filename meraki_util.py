

# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems

# !/usr/bin/env python3

# this module include common utilized functions to create applications using Meraki APIs



def meraki_get_organizations():
    """
    This function will get the Meraki Organization Id
    API call to /organizations
    :return: Meraki Organization Id
    """
    url = MERAKI_URL + '/organizations'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    org_response = requests.get(url, headers=header, verify=False)
    org_json = org_response.json()
    org_id = org_json[0]['id']
    return org_id


def meraki_get_networks(organization_id):
    """
    This function will return the list of networks associated with the Meraki Organization ID
    API call to /organizations/{organization_id]/networks
    :param organization_id: Meraki Organization ID
    :return: network ids and names
    """
    url = MERAKI_URL + '/organizations/' + str(organization_id) + '/networks'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    networks_response = requests.get(url, headers=header, verify=False)
    networks_json = networks_response.json()
    network_id = networks_json[0]['id']
    network_name = networks_json[0]['name']
    return network_id, network_name


def meraki_get_sm_devices(network_id):
    """
    This function will return the list of networks associated with the Meraki Network ID
    API call to /networks/{organization_id]/sm/devices
    :param network_id: Meraki network ID
    :return: list with all the SM devices
    """

    url = MERAKI_URL + '/networks/' + str(network_id) + '/sm/devices?fields=phoneNumber,location'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    sm_devices_response = requests.get(url, headers=header, verify=False)
    sm_devices_json = sm_devices_response.json()['devices']
    return sm_devices_json


def meraki_get_devices(network_id):
    """
    This function will return a list with all the network devices associated with the Meraki Network Id
    :param network_id: Meraki Network ID
    :return: list with all the devices
    """
    url = MERAKI_URL + '/networks/' + str(network_id) + '/devices'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    devices_response = requests.get(url, headers=header, verify=False)
    devices_json = devices_response.json()
    return devices_json


def get_user_cell(users_info, email):
    """
    This function will look up the user cell phone based on his email
    :param users_info: List of all the users info
    :param user_email: user email address
    :return: the user cell phone number
    """

    user_cell = None
    for user in users_info:
        if user['email'] == email:
            user_cell = user['cell']
    return user_cell


def get_location_cell(sm_devices_list, user_cell):
    """
    This function will locate the user based on his cell phone number
    :param sm_devices_list: the list of Meraki SM devices
    :param user_cell: user cell phone number
    :return: the user location
    """
    location = None
    for device in sm_devices_list:
        if device['phoneNumber'] == user_cell:
            pprint(device)
            location = device['location']
    return location


def meraki_get_ssids(network_id):
    """
    This function will return the Meraki Network id list of configured SSIDs
    :param network_id: Meraki Network id
    :return: list of SSIDs
    """
    url = MERAKI_URL + '/networks/' + str(network_id) + '/ssids'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    ssids_response = requests.get(url, headers=header, verify=False)
    ssids_json = ssids_response.json()

    # filter only configured SSIDs
    ssids_list = []
    for ssid in ssids_json:
        if 'Unconfigured' not in ssid['name']:
            ssids_list.append(ssid)
    return ssids_list

