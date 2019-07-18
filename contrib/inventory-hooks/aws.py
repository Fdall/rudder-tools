

import json
try:
    import requests
except: 
    print("Install python-requests OR use python3")


def load():

    # The following url for viewing all categories of instance metadata from within a running instance.
    # The IP address 169.254.169.254 is a link-local address and is valid only from the instance.
    metaurl = 'http://169.254.169.254/latest'
    
    metadict = {'dynamic': {}, 'meta-data': {}, 'user-data': {}}

    for subsect in metadict.keys():
        dataparse('{0}/{1}/'.format(metaurl, subsect), metadict[subsect])

    newdict = metadict
    for key in newdict.keys():
        try:
            newdict['AWS-'+key] = newdict.pop(key)
        except KeyError:
            pass

    return newdict

def dataparse(url,k):

    data = requests.get(url)
    if data.status_code == 404:
        return

    for key in data.text.split('\n'): 
        if not key:
            continue

        if key in [ "rsa2048", "pkcs7", "signature", "security-credentials/" ]:
            continue

        newurl = '{0}{1}'.format(url, key)

        if key.endswith('/'):
            newkey = key.split('/')[-2]
            k[newkey] = {}
            dataparse(newurl, k[newkey], )

        else:
            data = requests.get(newurl)
            if data.status_code != 404:
                try:
                    k[key] = json.loads(data.text)
                except ValueError:
                    k[key] = data.text
            else:
                k[key] = None

if __name__ == '__main__':
    print(json.dumps(load()))