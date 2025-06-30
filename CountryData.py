import random
from pygame import image, transform
from func import round_corners


class Countries:
    def __init__(self, data):
        self.countryData = data
        self.colorsToCountries = {tuple(v[0]): k for k, v in self.countryData.items()}
        self.countriesToFlags = {
            k: round_corners(
                transform.scale_by(
                    image.load(f"flags/{k.lower()}_flag.png"),
                    (300 / image.load(f"flags/{k.lower()}_flag.png").get_width()),
                ),
                16,
            )
            for k in self.countryData
        }

    def getCountryType(self, culture, ideology=None):
        if not ideology == None:
            for country in self.countryData.keys():
                if (
                    self.getCulture(country) == culture
                    and self.getIdeology(country) == ideology
                ):
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
        ideologies = {
            "liberal": [-0.5, 0.5],
            "communist": [-0.5, -0.5],
            "monarchist": [0.5, 0.5],
            "nationalist": [0.5, -0.5],
        }
        return ideologies.get(str(self.countryData.get(country)[3]), [0, 0])

    def getCultures(self):
        cultureList = []
        for data in self.countryData.values():
            if data[2] not in cultureList:
                cultureList.append(data[2])
        return cultureList
