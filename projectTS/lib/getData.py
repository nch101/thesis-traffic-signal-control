import requests

class getData:
    """
    Get data from server including time, mode control
    using getDataURL interID and access-token, 
    """
    def __init__(self, getDataURL, interID, accessToken):
        self.__headers = {'access-token': accessToken}
        self.__requestURL = getDataURL + interID
        pass

    def getData(self):
        self.__res = requests.get(self.__requestURL, headers=self.__headers)
        if (self.__res.status_code == 200):
            self.__modeControl = self.__res.json().get('modeControl')
            self.__trafficLights = self.__res.json().get('trafficLights')
            self.__nTrafficLights = len(self.__trafficLights)
                

    def timeRed(self):
        self.__timeRed = []
        for index in range(0, self.__quantity):
            self.__timeRed.append(self.__trafficLights[index].get('timeRed'))
        return self.__timeRed

    def timeYellow(self):
        self.__timeYellow = []
        for index in range(0, self.__quantity):
            self.__timeYellow.append(self.__trafficLights[index].get('timeYellow'))
        return self.__timeYellow

    def timeGreen(self):
        self.__timeGreen = []
        for index in range(0, self.__quantity):
            self.__timeGreen.append(self.__trafficLights[index].get('timeGreen'))
        return self.__timeGreen

    def modeControl(self):
        return self.__modeControl

    def nTrafficLights(self):
        return self.__nTrafficLights


""" getDataURL = 'http://localhost:3000/intersection/get-data/'
interID = '5e80b202ffd7df231c4f7926'
accessToken = 'accessToken'

testData = getData(getDataURL, interID, accessToken)

print('****Testing****')
testData.getData()
print(testData.timeRed())
print(testData.timeYellow())
print(testData.timeGreen())
print(testData.modeControl()) """
        


