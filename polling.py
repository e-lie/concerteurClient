#!/usr/bin/python3

from urllib import request, parse
import json
import os

SERVER_URL = os.environ['SERVER_URL']

def get_sound_list(txtFile = 'last_file_name.txt'):
    #Local POST request to the flask app using a custom port
    url = SERVER_URL + '/get-sound-list'
    with open(txtFile, 'r') as f:
        filename = f.readline()
        params = {'lastFilename':filename}

        # Encode the query string
        querystring = parse.urlencode(params)

        # Make a POST request and read the response
        resp = request.urlopen(url, querystring.encode('utf-8'))
        #read bytes from the JSON response and convert it to string (decode) then dictionnary (json.loads)
        jsondata = resp.read().decode('utf-8')
        return json.loads(jsondata)
        
def get_sound(filename):
    url = SERVER_URL + '/get-sound'
    params = {'soundname':filename}
    with open("sounds/"+filename, 'wb') as f:
        querystring = parse.urlencode(params)
        resp = request.urlopen(url, querystring.encode('utf-8'))
        mp3 = resp.read()
        f.write(mp3)
    

if __name__ == "__main__":
    data = get_sound_list()
    soundList = data['filenames']
    lastFilename = data['lastfilename']
    for sound in soundList:
        get_sound(sound)
    with open('last_file_name.txt','w') as f:
        f.write(lastFilename)
