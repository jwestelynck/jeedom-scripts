import requests
import json

class Jeedom:

    def __init__(self, protocol,hostname, apikey):
        self.protocol = protocol
        self.hostname = hostname
        self.apikey = apikey

    def get_call(self,uri):
        url = '{protocol}://{hostname}{uri}'.format(
            protocol = self.protocol,
            hostname = self.hostname,
            uri = uri
        )
        try:
            result = requests.get(url,verify=False).json()
        except:
            result = None
        return result

    def get_objects(self):
        uri = "/core/api/jeeApi.php?apikey={apikey}&type=object".format(
                apikey = self.apikey
            )
        return self.get_call(uri)

    def get_all_equipements(self):
        uri = "/core/api/jeeApi.php?apikey={apikey}&type=eqLogic".format(
                apikey = self.apikey
            )
        return self.get_call(uri)

    def get_all_data(self):
        uri = "/core/api/jeeApi.php?apikey={apikey}&type=fullData".format(
                apikey = self.apikey
            )
        return self.get_call(uri)