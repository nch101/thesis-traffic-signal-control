import requests

class getData:
    """
    Get data from server including time, mode control
    using getDataURL interID and access-token, 
    """
    def __init__(self, getDataURL, interID, accessToken):
        self.__headers = {'access-token': accessToken}
        self.__res = requests.get(getDataURL + interID, headers=self.__headers)
        if (self.__res.status_code == 200):
            self.__modeControl = self.__res.json().get('modeControl')
            self.__trafficLights = self.__res.json().get('trafficLights')

    def getTimeRed(self):
        self.__timeRed = []
        for index in range(0, len(self.__trafficLights)):
            self.__timeRed.append(self.__trafficLights[index].get('timeRed'))
        return self.__timeRed

    def getTimeYellow(self):
        self.__timeYellow = []
        for index in range(0, len(self.__trafficLights)):
            self.__timeYellow.append(self.__trafficLights[index].get('timeYellow'))
        return self.__timeYellow

    def getTimeGreen(self):
        self.__timeGreen = []
        for index in range(0, len(self.__trafficLights)):
            self.__timeGreen.append(self.__trafficLights[index].get('timeGreen'))
        return self.__timeGreen

    def modeControl(self):
        return self.__modeControl


""" getDataURL = 'http://localhost:3000/intersection/get-data/'
clientID = '5e80b202ffd7df231c4f7926'
accessToken = 'accessToken'

testData = getData(getDataURL, clientID, accessToken)

print('****Testing****')
print(testData.getTimeRed())
print(testData.getTimeYellow())
print(testData.getTimeGreen())
print(testData.modeControl()) """
        


