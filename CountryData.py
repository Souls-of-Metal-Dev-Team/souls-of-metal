import random

class Countries:

    def __init__(self):
        # i manually did the country example
        self.countryData = {"Japan": [(195, 92, 109),
                    (52, 62, 105, 115, 117, 119, 169, 176, 192, 193, 258, 270, 305, 310, 311, 312, 313, 314, 417, 440, 441, 480, 501, 508, 538, 575, 581, 582, 583, 597, 608, 618, 638, 664, 676, 677, 709, 716, 737, 738, 773, 787, 797, 809, 810, 826, 882, 895, 896, 907, 922, 938, 958, 961, 977, 1028, 1075)
                    , "Japanese",
                    "liberal", 69]}

        self.colorsToCountries = {v[0]: k for k, v in self.countryData.items()}

    def getCountryType(self, culture, ideology=None):
        if not ideology == None:
            for country in self.countryData.keys():
                if self.getCulture(country) == culture and self.getIdeology(country) == ideology:
                    return country
        else:
            countries = [i for i in self.countryData.keys()]
            random.shuffle(countries)
            for country in countries:
                if self.getCulture(country) == culture:
                    return country
        return None

    def getAllCountries(self, culture):
        return [i for i in self.countryData.keys() if self.countryData[i][2] == culture]

    def getEveryCountry(self):
        return [i for i in self.countryData.keys()]

    def colorToCountry(self, color):
        return self.colorsToCountries.get(color)

    def getCountryData(self, country):
        return self.countryData.get(country)

    def getColor(self, country):
        return self.countryData.get(country)[0]

    def getClaims(self, country):
        return self.countryData.get(country)[1]

    def getCulture(self, country):
        return self.countryData.get(country)[2]

    def getIdeology(self, country):
        return self.countryData.get(country)[3]

    def getBaseStability(self, country):
        if type(self.countryData.get(country)[-1]) == str:
            return 60
        return self.countryData.get(country)[-1]

    def getIdeologyName(self, country):
        ideologies = {'liberal': [-0.5, 0.5], 'communist': [-0.5, -0.5], 'monarchist': [0.5, 0.5], 'nationalist': [0.5, -0.5]}
        return ideologies.get(str(self.countryData.get(country)[3]), [0, 0])

    def getCultures(self):
        cultureList = []
        for data in self.countryData.values():
            if data[2] not in cultureList:
                cultureList.append(data[2])
        return cultureList
a = Countries()
print(a.getCultures())
