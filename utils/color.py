from PIL import Image, ImageDraw

def wrap(value, max):
    return value % max

def main():
    image = Image.open("map.png").convert("RGB")
    pixels = image.load()
    if not pixels:
        return

    width, height = image.size

    BLACK = (0,0,0)
    colors = set()

    r = 1
    g = 0
    b = 0

    for y in range(height):
        for x in range(width):
            c = pixels[x, y]
            if c == BLACK or c in colors:
                continue

            new_color = (g, r, b)
            colors.add(new_color)

            ImageDraw.floodfill(image, (x, y), new_color)

            r = wrap(r+1, 256)
            if r == 0:
                g = wrap(g+1, 256)
                if g == 0:
                    b = wrap(b+1, 256)
                    if b == 256:
                        print("Ran out of unique colors !!!")
 
    print("Saved image to 'provinces.png'")
    image.save("provinces.png")

main()
