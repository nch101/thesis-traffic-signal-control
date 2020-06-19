import requests

class postData:
    def __init__(self, url, interID, accessToken):
        self.__headers = { 'access-token': accessToken }
        self.__requestURL = url + interID
    
    def postData(self, data):
        payload = data
        self.__res = requests.post(self.__requestURL, headers=self.__headers, verify=False, data=payload)
        if (self.__res.status_code == 200):
            return True
        else:
            return False