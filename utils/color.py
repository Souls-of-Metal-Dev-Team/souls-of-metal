from PIL import Image, ImageDraw

def main():
    image = Image.open("map.png").convert("RGB")
    pixels = image.load()
    if not pixels:
        return

    width, height = image.size

    colors = {(0,0,0)}

    counter = 0

    for i in range(height * width):
        c = pixels[i % width, i // width]
        if c in colors: # I assume you can't just put BLACK in colors?
            continue
        counter += 1
        new_color = (counter % 256, (counter // 256) % 256, (counter // 65536) % 256)
        colors.add(new_color)

        ImageDraw.floodfill(image, (i % width, i // width), new_color)

        # If you want just check for black here for validation or something.
 
    print("Saved image to 'provinces.png'")
    image.save("provinces.png")

if __name__ == "__main__":
    main()