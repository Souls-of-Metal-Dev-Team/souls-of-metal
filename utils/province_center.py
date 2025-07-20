from PIL import Image
import statistics
import sys
from collections import defaultdict
import json

def wrap(value, max):
    return value % max

def get_center(points):
    x = round(statistics.mean(i[0] for i in points))
    y  = round(statistics.mean(i[1] for i in points))

    return (x, y)

def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: province_center.py" + __file__ + " input [output]")
        return

    image = Image.open(sys.argv[1]).convert("RGB")
    pixels = image.load()
    if not pixels:
        return

    width, height = image.size

    color_positions = defaultdict(list)

    BLACK = (0, 0, 0)

    for y in range(height):
        for x in range(width):
            c = pixels[x, y]
            if c == BLACK:
                continue
            color_positions[c].append((x, y))

    centers = {}
    for color, positions in color_positions.items():
        centers[str(color)] = list(get_center(positions))

    outpath = ""
    if len(sys.argv) == 3:
        outpath = sys.argv[2]
    else:
        outpath = "province_centers.json"

    output = json.dumps(centers)
    with open(outpath, "w") as f:
        f.write(output)

    print("Saved json to", outpath)

if __name__ == "__main__":
    main()
