#!/usr/bin/env python

import requests
import json

#importing custom functions
from aaa import aaa_login, aaa_logout
from json_func import switch_get, switch_post
from bgp_func import get_bgp_config, set_bgp_config
from common import get_interfaces, get_boot_img, get_device_info, write_to_file

# ARE there YDK models for NXOS? Can I use them?
#from ydk.models.bgp import bgp

#################
'''
This first checks to see if the list of interfaces is empty, if not it loops through each interface and creates
the JSON data in order to modify the description of each interface.
'''

def set_intf_desc(switch, token, intf_list) :
    if len(intf_list) == 0:
        return 0

    interfaces = { 
        "topSystem": {
            "children": [
                {
                    "interfaceEntity": {
                    "children": []
                    }   
                }
            ]
        }
    }


    #Loop creates a new dictionary to set each interface description, it is appended to a list 
    for i in range(len(intf_list)):
        intf_num = intf_list[i].split('/')
        new_int = {
            "l1PhysIf": {
                "attributes": {
                    "descr": "Nicks interface, number: " + intf_num[1], 
                    "id": intf_list[i]
                }           
            }
        }
        interfaces['topSystem']['children'][0]['interfaceEntity']['children'].append(new_int)

    #sets the interface descriptions
    url = '/api/mo/sys.json'
    rx_code, rx_text = switch_post(switch, url, interfaces, token)

    #Check to see if the request was successful (i.e. returned a 20x code)
    if rx_code != requests.codes.ok:
        print 'Failed to change interface descriptions. Error Code: ' + str(rx_code)
        rx_json = json.loads(rx_text)
        print '\tError msg:\t' + rx_json['imdata'][0]['error']['attributes']['text']
        return 0
    else:
        return 1

#######################
'''
Sets the Loopback IP address
'''
def set_loopback(switch, token):

    
    body = {
    "topSystem": {
        "children": [
        {
            "ipv4Entity": {
            "children": [
                {
                    "ipv4Inst": {
                    "children": [
                        {
                            "ipv4Dom": {
                                "attributes": {
                                    "name": "default"
                                },
                                    "children": [
                                        {          
                                            "ipv4If": {
                                                "attributes": {
                                                    "id": "lo100"
                                                },
                                                "children": [
                                                    {
                                                        "ipv4Addr": {
                                                            "attributes": {
                                                                "addr": "192.168.1.1/24"
                                                            }
                                                        }
                                                    }
                                                ]       
                                            }       
                                        }
                                    ]
                            }              
                        }
                    ]
                    }
                }
            ]
            }
        },
        {
            "interfaceEntity": {
                "children": [
                    {
                        "l3LbRtdIf": {
                            "attributes": {
                                "adminSt": "up",
                                "id": "lo100"
                            }
                        }
                    }
                ]
            }
        }
        ]
    }
    }   

    url = '/api/mo/sys.json'
    
    rx_code, rx_text = switch_post(switch, url, body, token)
    
    if rx_code != requests.codes.ok:
        print 'Error, unable to POST Loopback config. Error Code: ' + str(rx_code)
        rx_json = json.loads(rx_text)
        print '\tError msg:\t' + rx_json['imdata'][0]['error']['attributes']['text']
        return 0
    else:
        return 1

###############

if __name__ == "__main__":
    
    user = 'vagrant'
    passwd = 'vagrant'
    switch = 'http://127.0.0.1:8080'

    rx_code, token =  aaa_login(user, passwd, switch)
    if rx_code != requests.codes.ok :
        print "Closing Application. Error Code" + str(rx_code)
        exit()
    else:
        print "Successfully logged in!"
        
        #TASK 1 - Change interface descriptions
        if set_intf_desc(switch, token, get_interfaces(switch, token, 'l1PhysIf')):
            print "Successfully updated interface descritions"

        #TASK 2 - Configure a Loopback and BGP
        #first create the loopback
        set_loopback(switch, token)
        #Ensure the BGP configuration has succeeded, otherwise dont try to get the BGP config
        if set_bgp_config(switch, token):
            print "Successfully modified BGP configuration"
            get_bgp_config(switch, token)
        else:
            print "Failed to modify BGP configuration"

        #TASK 3 - Write device information to a file
        fname = 'nxsov.txt'
        write_to_file(fname, get_boot_img(switch, token) + get_device_info(switch,token) + get_bgp_config(switch, token))
        print 'Wrote device information to ' + fname +'\n'     

        if aaa_logout(user, switch, token) == requests.codes.ok:
			print "Successfully logged out!"
        else:
            print "Logout Unsuccessful"

