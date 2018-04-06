import requests
import json

def switch_get (switch, url, token):
    #print 'Sending GET request to ' + switch + url
    response = requests.get(switch + url, headers=token)
    return response.status_code, response.text

#################

def switch_post (switch, url, body, token):
    #print 'Sending POST request to ' + switch + url
    response = requests.post(switch + url, headers=token, data=json.dumps(body))
    return response.status_code, response.text 

#################

