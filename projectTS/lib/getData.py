import requests

class getData:
    """
    Get data from server including time, mode control
    using getDataURL interID and access-token, 
    """
    def __init__(self, getDataURL, interID, accessToken):
        self.__headers = { 'access-token': accessToken }
        self.__requestURL = getDataURL + interID
        pass

    def getData(self):
        self.__res = requests.get(self.__requestURL, headers=self.__headers, verify = False)
        if (self.__res.status_code == 200):
            self.timeRed = []
            self.timeYellow = []
            self.timeGreen = []
            self.priorityStreet = []
            self.__trafficLights = self.__res.json().get('trafficLights')
            self.modeControl = self.__res.json().get('modeControl')
            self.quantity = len(self.__trafficLights)
            self.deltaTime = self.__res.json().get('delta')

            for index in range(0, self.quantity):
                self.timeRed.append(self.__trafficLights[index].get('timeRed'))
                self.timeYellow.append(self.__trafficLights[index].get('timeYellow'))
                self.timeGreen.append(self.__trafficLights[index].get('timeGreen'))
                self.priorityStreet.append(self.__trafficLights[index].get('priority'))


# """
# * Test getData
# """
# getDataURL = 'https://localhost:3000/api/intersection/'
# interID = '5eb90fe69f1398273bba559a'
# accessToken = 'accessToken'

# testData = getData(getDataURL, interID, accessToken)

# print('****Testing****')
# testData.getData()
# print(testData.timeRed)
# print(testData.timeYellow)
# print(testData.timeGreen)
# print(testData.priorityStreet)
# print(testData.modeControl)
# print(testData.quantity)
# print(testData.deltaTime)