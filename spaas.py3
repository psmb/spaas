#!/usr/bin/env python3
import urllib.request, json, os, filecmp, subprocess

cacheDir = '/var/cache/spaas/'
os.makedirs(cacheDir, exist_ok=True)

def deploy(name):
    filename = cacheDir + name + '.yml'
    subprocess.call(["docker", "stack", "deploy", name, "--compose-file=" + filename])

users = ['psmb', 'dimaip']
userQuery = ''.join(map(lambda user: "+user:" + user, users))
topic = 'psmb-server'

header={'Pragma': 'no-cache', 'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url="https://api.github.com/search/repositories?q=topic:" + topic + userQuery, headers=header)
with urllib.request.urlopen(req) as url:
    data = json.loads(url.read().decode())
    for repo in data['items']:
        name = repo['name']
        fullName = repo['full_name']
        print("Downloading " + fullName)
        url = 'https://raw.githubusercontent.com/' + fullName + '/master/docker-compose.yml'
        filename = cacheDir + name + '.yml'

        if os.path.isfile(filename):
            cachedFile = open(filename, 'r')
            cachedFileContets = cachedFile.read()
            cachedFile.close()
            urllib.request.urlretrieve(url, filename)
            newFile = open(filename, 'r')
            newFileContents = newFile.read()
            if newFileContents == cachedFileContets:
                print ("docker-compose.yml file hasn't been changed, skipping")
            else:
                print ("changed, deploying")
                deploy(name)
        else:
            urllib.request.urlretrieve(url, filename)
            print ("init, deploying")
            deploy(name)
