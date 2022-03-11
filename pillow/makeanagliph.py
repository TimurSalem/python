
def makeanagliph(filename, delta, savename='res.jpg'):

    """
    this function is responsible for creating a 3D effect using anaglyph <https://en.wikipedia.org/wiki/Anaglyph_3D>
    in which you can adjust the degree of shift of the red channel (to the right)

    :param savename: saved file name
    :param filename: filename to open
    :param delta: degree of shear
    """

    from PIL import Image

    im = Image.open(filename)
    x, y = im.size
    res = Image.new('RGB', (x, y), (0, 0, 0))

    pixels_first = res.load()
    pixels_second = im.load()

    for i in range(x):
        for j in range(y):

            if i >= delta:
                r, g, b = pixels_second[i - delta, j]
                r2, g2, b2 = pixels_second[i, j]
                pixels_first[i, j] = r, g2, b2
            else:
                r, g, b = pixels_second[i, j]
                pixels_first[i, j] = 0, g, b

    res.save(savename)
