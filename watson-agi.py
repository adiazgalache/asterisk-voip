#!/usr/bin/python
# Overall import
import sys,os
import requests
import json

## Watson Parameters
# Credentials
username = "db885c28-0c00-4e32-ac3d-f788f8877054"
password = "N7U8r5pSkkJQ"
# Model language
model_name = "es-ES_NarrowbandModel"
# API Url Endpoint
url = "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?continuous=true&model=" + model_name
# Timeout API
timeout = 5

## Audio Parameters
path_audio = "/var/lib/asterisk/sounds"
ext_audio = "wav"

## Init VariablesA
# Default event
event = "SOPORTE"

# Obtain audio file
data = open(path_audio + "/" + sys.argv[1] + "." + ext_audio)

# Send Data 
def send(data):
    sys.stdout.write(str(data))
    sys.stdout.flush()

# Call Watson API
def call_watson(url, data, username, password, timeout):
    try:
    	headers = {'content-type': 'audio/' + ext_audio}
    	r = requests.post(url=url,auth=(username, password),data=data,headers=headers,timeout=timeout)
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
    # Handler Exception
	return "ERROR" 
    # Return Error    
    return json.dumps(r.json())

# Call API Watson
res = call_watson(url, data, username, password, timeout)

if res != "ERROR":
    a = json.loads(res)
    # Return transcript
    text = a["results"][0]["alternatives"][0]["transcript"]
    msg = text.encode('ascii', 'ignore').decode('ascii')
    ## AQUI EMPIEZA NLP

    ## AQUI TERMINA NLP
    # Send Event (VENTAS|FACTURACION|SOPORTE
    event = "XXXX"
else:
    event = "ERROR"
    

## Asterisk AGI
# Send Event (VENTAS|FACTURACION|SOPORTE|ERROR)
send("SET VARIABLE SPEECH_TO_TEXT " + event)