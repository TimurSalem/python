def makevignette(im=None, filename='', degree=3, intensity=90, color=[1, 1, 1]):
    """
    The function is responsible for creating darkening at the edges of the image

    :param im: if the path to the file is not specified, you can use image file
    :param filename: path to file
    :param degree: degree of darkening |Need to adjust differently for each image|
    :param intensity: responsible for the intensity of the color specified by the {color} parameter
    :param color: responsible for color |configured by palette type [1, 1, 1] == [3, 3, 3]| (in proportion)
    :return: returns an object of type {Image}
    """

    from PIL import Image

    if filename != '':
        im = Image.open(filename)

    x, y = im.size

    degree /= (x * y) ** 0.4

    pixels = im.load()
    al = color[0] + color[1] + color[2]

    centerx, centery = x // 2, y // 2

    d1 = color[0] * intensity / al
    d2 = color[1] * intensity / al
    d3 = color[2] * intensity / al

    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pls = int(abs(i - centerx) ** 2 + abs(j - centery) ** 2 * (x / y))
            pls = int(pls / 1000) * (degree ** 0.5)

            rm = pls - d1 if pls - d1 > 0 else 0
            gm = pls - d2 if pls - d2 > 0 else 0
            bm = pls - d3 if pls - d3 > 0 else 0

            pixels[i, j] = int(r - rm), int(g - gm), int(b - bm)

    return im
