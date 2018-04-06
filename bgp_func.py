import requests
import json

#importing custom functions
from json_func import switch_get, switch_post
from common import is_feature_enabled

#################
        
def get_bgp_config(switch, token):
    
    #check to see if the BGP feature is enabled
    if is_feature_enabled(switch, token, 'fmBgp'):   
        url = '/api/mo/sys/bgp/inst.json'
        rx_code, rx_text = switch_get(switch, url, token)

        # if we dont get OK code then error 
        if rx_code != requests.codes.ok :
            print 'Unable to get BGP config. Error Code: ' + str(rx_code)
        else:
            rx_json = json.loads(rx_text)
            return 'BGP ASN = ' + rx_json['imdata'][0]['bgpInst']['attributes']['asn'] + '\n'
            #print json.dumps(rx_json, indent=5)   
            #now do something clever with the data
    else:
        print "Feature BGP is not enabled, first enable it on the CLI (feature bgp) before running this script again"

################

def set_bgp_config(switch, token) :
    '''
    Function will set the BGP configuration. I've been lazy and not asked for input or used variables
    but it does what is needed to setup a basic BGP configuration
    '''

    #check to see if BGP is enabled first
    if not is_feature_enabled(switch, token, 'fmBgp'):
        print "Feature BGP is not enabled, first enable it on the CLI (feature bgp) before running this script again"
        return 0

    url = '/api/mo/sys.json'

    body = {
        "topSystem": {
            "children": [
                {
                "bgpEntity": {
                    "children": [
                        {
                        "bgpInst": {
                            "attributes": {
                                "asn": "10"
                            },
                            "children": [
                                {
                                "bgpDom": {
                                    "attributes": {
                                        "name": "default",
                                        "rtrId": "192.168.1.1"
                                    },
                                    "children": [
                                        {
                                        "bgpPeer": {
                                            "attributes": {
                                                "addr": "192.168.10.2",
                                                "asn": "11",
                                                "inheritContPeerCtrl": ""
                                            }
                                        }
                                        },
                                        {
                                            "bgpDomAf": {
                                                "attributes": {
                                                    "type": "ipv4-ucast"
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
    }

    rx_code, rx_text = switch_post(switch, url, body, token)

    if rx_code != requests.codes.ok :
        print 'Error, unable to POST BGP config. Error Code: ' + str(rx_code)
        rx_json = json.loads(rx_text)
        print '\tError msg:\t' + rx_json['imdata'][0]['error']['attributes']['text']
        return 0
    else:
        return 1

