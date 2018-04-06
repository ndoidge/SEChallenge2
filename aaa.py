import requests
import json


################

def aaa_login(user, passwd, switch):
    body = {
        "aaaUser": {
            "attributes": {
                "name": user,
                "pwd": passwd
            }
        }
    }

    #append the aaaLogin.json portion to create the full URL
    url = switch + '/api/aaaLogin.json'

    #login to the switch to get the token information
    response = requests.post(url, data=json.dumps(body))
	
    if response.status_code == requests.codes.ok:
        #configure the token used for subsequent operations
        rx_object = json.loads(response.text)

        #Create the header with the token embedded to allow execution of commands etc 
        token = { 'cookie': 'APIC-Cookie=' + rx_object['imdata'][0]['aaaLogin']['attributes']['token'] }
        return response.status_code, token
    else:
        exit()

#################

def aaa_logout(user, switch, token):

    body = {
		'aaaUser' : {
			'attributes' : {
				'name' : user
			}
		}
	}

    #append the aaaLogout.json portion to create the full URL
	url = switch + '/api/aaaLogout.json'

    #logout of the switch
	response = requests.post(url, data=json.dumps(body), headers=token)

    return response.status_code


