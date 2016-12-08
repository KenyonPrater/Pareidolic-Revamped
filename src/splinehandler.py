import numpy as np
import math

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
        return Point(self._arr - other._arrapplyBrush)

    def __mul__(self, number):
        return Point(self._arr*number)

    def __mul__(self, number):
        return Point(self._arr*number)

    def __truediv__(self, number):
        return Point(self._arr/number)

    def __str__(self):
        return "Point: " + str(self._arr)

    def lerp(self, other, t):
        assert t >= 0 and t <= 1
        return self*(1-t) + other * t

class DrawingPoint(Point):

    @classmethod
    def fromColors(Class, pos, color, size, hardness):
        return Class(pos + color + (size,) + (hardness,))

    def draw(self, drawing):
        drawing.applyBrush(self.getPos(), self.getColor(), self.getSize(), self.getHardness())

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

    def __add__(self, other):
        return DrawingPoint(self._arr + other._arr)

    def __sub__(self, other):
        return DrawingPoint(self._arr - other._arr)

    def __mul__(self, number):
        return DrawingPoint(self._arr*number)

    def __rmul__(self, number):
        return DrawingPoint(self._arr*number)

    def __truediv__(self, number):
        return DrawingPoint(self._arr/number)

    def __str__(self):
        roundedColor = tuple([int(c) for c in self.getColor()])
        return "DrawingPoint(x:{:.2f}, y:{:.2f}, rgba:{}, size:{:.1f}, hardness:{:.2f})".format(self.getX(), self.getY(), roundedColor, self.getSize(), self.getHardness())

class Path():
    def __init__(self):
        pass

    def sample(self, t):
        pass

class Bezier(Path):
    def __init__(self, points):
        self._points = points

    def sample(self, t):
        a = self._points
        while len(a) > 1:
            new_a = []
            for i in range(len(a)-1):
                new_a += [a[i].lerp(a[i+1], t)]
            a = new_a
        return a[0]

class CompoundBezier(Path):
    def __init__(self):
        self._points = []
        self._beziers = []

    def appendPoint(self, center, r_tangent, l_tangent=None):
        if l_tangent == None:
            l_tangent = 2*center - r_tangent
        self._points += [[l_tangent, center, r_tangent]]
        self.generateBeziers()

    def insertPoint(self, index, center, r_tangent, l_tangent=None):
        if l_tangent == None:
            l_tangent = 2*center - r_tangent
        self._points.insert(index, [l_tangent, center, r_tangent])
        self.generateBeziers()

    def removePoint(self, index):
        self._points.pop(index)
        self.generateBeziers()

    def generateBeziers(self):
        self._beziers = []
        for i in range(len(self._points) - 1):
            arr = [self._points[i][1], self._points[i][2], self._points[i+1][0], self._points[i+1][1]]
            self._beziers += [Bezier(arr)]

    def sample(self, t):
        #determine which bezier to sample:
        bezier_t = len(self._beziers)*t
        bezier_index = min(int(bezier_t), len(self._beziers)-1)
        print(bezier_t, bezier_index)
        bezier_t = 1 if t>=1 else bezier_t%1 # Stop t=1 from making bezier_t = 0
        return self._beziers[bezier_index].sample(bezier_t)

if __name__ == '__main__':
    a = DrawingPoint.fromColors((0,0), (255, 0, 0, 0), 10, .75)
    b = DrawingPoint.fromColors((0,1), (0, 255, 0, 0), 10, .75)
    c = DrawingPoint.fromColors((.5,.5), (0, 0, 255, 0), 10, .75)
    d = DrawingPoint.fromColors((.5,0), (0, 0, 0, 255), 10, .75)
    e = DrawingPoint.fromColors((1,1), (0, 0, 255, 0), 10, .75)
    f = DrawingPoint.fromColors((1,2), (0, 0, 0, 255), 10, .75)
    g = CompoundBezier()
    g.appendPoint(a, b)
    g.appendPoint(c, d)
    g.appendPoint(e, f)
    for i in range(11):
        print(g.sample(i/10))
