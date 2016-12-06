import numpy as np

class Point():
    def __init__(self, array):
        self._arr = np.array(array)

    def _setElement(self, index, val):
        self._arr[index] = val

    def _getElement(self, index):
        return self._arr[index]

    def __add__(self, other):
        return Point(self._arr + other._arr)

    def __sub__(self, other):
        return Point(self._arr - other._arr)

    def __str__(self):
        return "Point: " + str(self._arr)

    def __mul__(self, number):
        return Point(self._arr*number)

    def __truediv__(self, number):
        return Point(self._arr/number)

    def lerp(self, other, t):
        assert t >= 0 and t <= 1
        return self*(1-t) + other * t

class DrawingPoint(Point):
    def __init__(self, pos, color, size, hardness):
        self._arr = np.array(pos + color + (size,) + (hardness,), dtype='float64')

    def setX(self, x):
        self._arr[0] = x

    def setY(self, y):
        self._arr[1] = y

    def setPos(self, pos):
        self._arr[0:2] = pos

    def setRed(self, r):
        self._arr[2] = r

    def setGreen(self, g):
        self._arr[3] = g

    def setBlue(self, b):
        self._arr[4] = b

    def setAlpha(self, a):
        self._arr[5] = a

    def setColor(self, color):
        self._arr[2:6] = pos

    def setSize(self, size):
        self._arr[6] = size

    def setHardness(self, hardness):
        self._arr[7] = hardness

    def getX(self):
        return self._arr[0]

    def getY(self):
        return self._arr[1]

    def getPos(self):
        return tuple(self._arr[0:2])

    def getRed(self):
        return self._arr[2]

    def getGreen(self):
        return self._arr[3]

    def getBlue(self):
        return self._arr[4]

    def getAlpha(self):
        return self._arr[5]

    def getColor(self):
        return tuple(self._arr[2:6])

    def getSize(self):
        return self._arr[6]

    def getHardness(self):
        return self._arr[7]

    def __str__(self):
        return "DrawingPoint(x:{}, y:{}, rgba:{}, size:{}, hardness:{})".format(self.getX(), self.getY(), self.getColor(), self.getSize(), self.getHardness())

if __name__ == '__main__':
    a = DrawingPoint((1,2), (255, 0, 0, 0), 10, .75)
    b = DrawingPoint((4,3), (0, 0, 255, 0), 10, .75)
    for i in [0, .25, .5, .75, 1]:
        print(a.lerp(b, i))
