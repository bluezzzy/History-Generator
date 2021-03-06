#Simple noise implementation
#Written by Boojum on http://gamedev.stackexchange.com/questions/23625/how-do-you-generate-tileable-perlin-noise

# from PIL import Image

import random
import math

import utility

perm = range(256)
random.shuffle(perm)
perm += perm
dirs = [(math.cos(a * 2.0 * math.pi / 256),
         math.sin(a * 2.0 * math.pi / 256))
         for a in range(256)]

def noise(x, y, per):
    def surflet(gridX, gridY):
        distX, distY = abs(x-gridX), abs(y-gridY)
        polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
        polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
        hashed = perm[perm[int(gridX)%per] + int(gridY)%per]
        grad = (x-gridX)*dirs[hashed][0] + (y-gridY)*dirs[hashed][1]
        return polyX * polyY * grad
    intX, intY = int(x), int(y)
    return (surflet(intX+0, intY+0) + surflet(intX+1, intY+0) +
            surflet(intX+0, intY+1) + surflet(intX+1, intY+1))

def fBm(x, y, per, octs):
    val = 0
    for o in range(octs):
        val += 0.5**o * noise(x*2**o, y*2**o, per*2**o)
    return val

def put_data(im, data, w, h):
    data = reduce(lambda a, b: a + b, data)
    for x in xrange(w):
        for y in xrange(h):
            im.putpixel((x, y), int(data[x * h + y] * 255))

def generate_noise(size, message=''):#, fname='noise.png'):
    freq, octs = 1/32.0, 5
    data = []
    global perm
    perm = range(256)
    random.shuffle(perm)
    perm += perm
    for y in range(size):
        data.append([])
        for x in range(size):
            utility.show_bar(y * size + x, size**2, message=message, number_limit=True)
            data[-1].append(fBm(x*freq, y*freq, int(size*freq), octs))

    # if fname != None:
    #     im = Image.new("L", (size, size))
    #     put_data(im, map(lambda i: max(0, i), data), size, size)
    #     im.save(fname)

    return data
