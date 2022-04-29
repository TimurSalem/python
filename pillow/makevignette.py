def makevignette(im=None, filename='', degree=3, intensity=90, color=[1, 1, 1], smooth=16):
    """
    The function is responsible for creating darkening at the edges of the image

    :param im: if the path to the file is not specified, you can use image file
    :param filename: path to file
    :param degree: degree of darkening |Need to adjust differently for each image|
    :param intensity: responsible for the intensity of the color specified by the {color} parameter
    :param color: responsible for color |configured by palette type [1, 1, 1] == [3, 3, 3]| (in proportion)
    :param smooth: responsible for how smooth the vignette will look
    :return: returns an object of type {Image}
    """

    from PIL import Image

    if not im:
        im = Image.open(filename)

    x, y = im.size

    degree /= (x * y) ** 0.4

    pixels = im.load()
    al = color[0] + color[1] + color[2]

    centerx, centery = x // 2, y // 2

    d1 = color[0] * intensity / al
    d2 = color[1] * intensity / al
    d3 = color[2] * intensity / al

    smooth **= 0.5

    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pls = (((((i - centerx) ** 2 * (y / x)) + ((j - centery) ** 2) * (x / y)) *
                    (degree ** 0.8)) ** (1 / smooth) * (smooth ** 1.5))

            rm = pls - d1 if pls - d1 > 0 else 0
            gm = pls - d2 if pls - d2 > 0 else 0
            bm = pls - d3 if pls - d3 > 0 else 0

            pixels[i, j] = int(r - rm), int(g - gm), int(b - bm)

    return im


if __name__ == '__main__':
    makevignette(filename='YOURFILENAME', degree=50, smooth=16, intensity=200, color=[1, 1, 1]).save('res.png')
