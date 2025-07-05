import os
import random
from pygame import image, transform
from func import round_corners

# Get the base path where this file resides
base_path = os.path.dirname(__file__)


class Countries:
    def __init__(self, data):
        self.countryData = data
        self.colorsToCountries = {tuple(v[0]): k for k, v in self.countryData.items()}
        self.countriesToFlags = {}

        for k in self.countryData:
            # print(f'''"{k}": "{k.replace("_", " ")}",''')
            try:
                flag_path = os.path.join(base_path, "flags", f"{k.lower()}_flag.png")
                raw_flag = image.load(flag_path)
            except FileNotFoundError:
                raw_flag = image.load(os.path.join(base_path, "unknown.jpg"))

            scaled = transform.scale_by(raw_flag, 475 / raw_flag.get_width())
            rounded = round_corners(scaled, 16)
            self.countriesToFlags[k] = rounded

    def getCountryType(self, culture, ideology=None):
        if ideology is not None:
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
        return list(self.countryData.keys())

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
        val = self.countryData.get(country)[-1]
        return 60 if isinstance(val, str) else val

    def getIdeologyName(self, country):
        ideologies = {
            "liberal": [-0.5, 0.5],
            "communist": [-0.5, -0.5],
            "monarchist": [0.5, 0.5],
            "nationalist": [0.5, -0.5],
        }
        return ideologies.get(str(self.countryData.get(country)[3]), [0, 0])

    def getCultures(self):
        return list({data[2] for data in self.countryData.values()})
