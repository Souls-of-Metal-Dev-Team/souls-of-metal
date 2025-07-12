from PIL import Image
import json
import sys

def get_neighboring_colors(pixels, x, y):
    neighbors = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Skip center
            if i == 0 and j == 0:
                continue

            try:
                neighbors.add(pixels[x+i, y+j])
            except IndexError:
                pass

    return neighbors


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: country_neighbors.py input [output]")
        return

    image = Image.open(sys.argv[1]).convert("RGB")
    pixels = image.load()
    if not pixels:
        return

    width, height = image.size

    BLACK = (0,0,0)

    # TODO: Could update an existing json for speed
    regions_neighbors: dict[tuple[int, int, int], set[tuple[int, int, int]]] = {}
    for y in range(height):
        for x in range(width):
            if pixels[x, y] != BLACK:
                continue

            neighboring_colors = get_neighboring_colors(pixels, x, y)
            neighboring_colors.discard(BLACK)
            for region in neighboring_colors:
                regions_neighbors.setdefault(region, set())
                for n_region in neighboring_colors:
                    if  n_region == region:
                        continue
                    regions_neighbors[region].add(n_region)

    json_out = {}
    for key, value in regions_neighbors.items():
        json_out[str(key)] = list(value)

    path_out = ""
    if len(sys.argv) == 3:
        path_out = sys.argv[2]
    else:
        path_out = "neighbors.json"

    with open(path_out, "w") as f:
        json.dump(json_out, f, indent=2)

    print("Wrote output to:", path_out)

if __name__  == "__main__":
    main()
