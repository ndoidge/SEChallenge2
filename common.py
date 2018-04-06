import requests
import json

#importing custom functions
from json_func import switch_get, switch_post

#########################

def get_device_info(switch, token):
    url = '/api/mo/sys.json'

    rx_code, rx_text = switch_get(switch, url, token)

    if rx_code != requests.codes.ok:
        print 'Error, unable to GET system config. Error Code: ' + str(rx_code)
        rx_json = json.loads(rx_text)
        print '\tError msg:\t' + rx_json['imdata'][0]['error']['attributes']['text']
    else:
        rx_json = json.loads(rx_text)
        hostname = rx_json['imdata'][0]['topSystem']['attributes']['name']
        serial = rx_json['imdata'][0]['topSystem']['attributes']['serial']
        return 'Hostname is = ' + hostname + '\nSerial Number = ' + serial + '\n'    

#########################
'''
This function checks to see if a particular feature is configured AND enabled, will return 1 if it is, 0 if it isnt
'''

def is_feature_enabled(switch, token, feature):
    url = '/api/mo/sys/fm.json?rsp-subtree=full&rsp-prop-include=config-only'
    rx_code, rx_text = switch_get(switch, url, token)
    rx_json = json.loads(rx_text)

    feature_enabled = 0
    #loop through each child element of the output, looking to match the feature name, if successful, check its enabled
    for i in range(len(rx_json['imdata'][0]['fmEntity']['children'])):
        if 'fmBgp' in rx_json['imdata'][0]['fmEntity']['children'][i].keys():
            if rx_json['imdata'][0]['fmEntity']['children'][i][feature]['attributes']['adminSt'] == 'enabled':
                feature_enabled = 1
                break
    return feature_enabled


#########################

"""
This function is used to find all interfaces of type 'intf_type' - a variable in which you specify which interfaces you are after
i.e. l1PhysIf, l3LbRtdIf, sviIf. It then puts all these interfaces into a list and returns the list
"""

def get_interfaces(switch, token, intf_type):

    url = '/api/mo/sys/intf.json?rsp-subtree=children'
    rx_code, rx_text = switch_get(switch, url, token)

    interfaces = []

    if rx_code != requests.codes.ok:
        print 'Error, unable to GET interface config. Error Code: ' + str(rx_code)
        rx_json = json.loads(rx_text)
        print '\tError msg:\t' + rx_json['imdata'][0]['error']['attributes']['text']
    else: 
        #load JSON into python type(dict)
        rx_json = json.loads(rx_text)

        #loop through every interface instance
        for intf in range(len(rx_json['imdata'][0]['interfaceEntity']['children'])):
            #Check every interface for the type we want, if it matches, add it to the list of interfaces
            # important it is converted into a string, because it is unicode in native format
            if intf_type in rx_json['imdata'][0]['interfaceEntity']['children'][intf].keys():
                interfaces.append(str(rx_json['imdata'][0]['interfaceEntity']['children'][intf]['l1PhysIf']['attributes']['id']))

    return interfaces


################
'''
This function queries the switch to find out what boot image it is running, and
returns it as a string
'''

def get_boot_img(switch, token):
    url = '/api/mo/sys/boot/image.json?rsp-subtree=children'

    rx_code, rx_text = switch_get(switch, url, token)

    if rx_code != requests.codes.ok:
        print 'Error, unable to GET image config. Error Code: ' + str(rx_code)
        rx_json = json.loads(rx_text)
        print '\tError msg:\t' + rx_json['imdata'][0]['error']['attributes']['text']
    else: 
        rx_json = json.loads(rx_text)
        return 'Sup1 NXOS image is: ' + rx_json['imdata'][0]['bootImage']['attributes']['sup1'] + '\n'

####################
'''
This function writes a string to a file. At present it assumes the file does
not exist, so does not "append". I could add some checks later to get it to
append instead of write new. I just have to find the motivation :-D
'''

def write_to_file(filename, text):
    with open(filename, 'w') as output:
        output.write(text) 
    return 0

