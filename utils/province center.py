from PIL import Image, ImageDraw
import statistics


def wrap(value, max):
    return value % max


def main():
    image = Image.open("map.png").convert("RGB")
    pixels = image.load()
    if not pixels:
        return

    width, height = image.size

    BLACK = (0, 0, 0)
    colors = set()
    centers = {}

    r = 1
    g = 0
    b = 0

    for y in range(height):
        for x in range(width):
            c = pixels[x, y]
            if c not in centers:
                centers[c] = [(x, y)]
            else:
                centers[c].append((x, y))

    for k, v in centers.items():
        print(
            f"{k}: ({round(statistics.mean(i[0] for i in v))},{round(statistics.mean(i[1] for i in v))}),"
        )

    print("Saved image to 'provinces.png'")
    image.save("provinces.png")


main()
