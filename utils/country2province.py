from PIL import Image, ImageDraw
from json import dump, load


def wrap(value, max):
    return value % max


def main():
    with open("CountryData.json") as f:
        uhh = load(f)
        provincedata = {k: [] for k in uhh.keys()}
        coloredata = {tuple(v[0]): k for k, v in uhh.items()}
    cmap = Image.open("map.png").convert("RGB")
    pmap = Image.open("provinces.png").convert("RGB")
    cpixels = cmap.load()
    ppixels = pmap.load()

    width, height = cmap.size

    BLACK = (0, 0, 0)

    for y in range(height):
        for x in range(width):
            c = tuple(cpixels[x, y])
            p = list(ppixels[x, y])
            if c != BLACK:
                if c in coloredata:
                    if p not in provincedata[coloredata[c]]:
                        provincedata[coloredata[c]].append(p)

    for k in uhh.copy():
        uhh[k][1] = provincedata[k]
    print(uhh)


main()
