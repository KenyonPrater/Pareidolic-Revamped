
import numpy as np

class Path():
    """A thing that defines a path"""
    def __init__(self):
        pass

    def sample(self, t):
        """
        Returns the value of the Path at t in [0,1]
        """
        return np.array([0])

    def getDimension(self):
        """
        Returns the length of the vector returned by a call to Path.sample()
        """
        return 0

    def toArr(self, n):
        """
        Returns a numpy array of n values of the Path evenly spaced from 0 to 1
        """
        a = np.arange(n)
        vals = a / (n-1)
        arr = np.zeros((n,self.getDimension()))
        for i in range(n):
            arr[i] = self.sample(vals[i])
        return arr

class Bezier(Path):
    """A bezier curve in arbitrary dimensions"""
    def __init__(self, points):
        """
        Create a new bezier curve from points
        @param points - a 2d numpy array. dimension 1 is seperate points,
                        dimenison 2 is the coordinates in different dimensions for each point.
        """
        super().__init__()
        self._points = points

    def addPoint(self, point, index=-1):
        self._points = np.insert(self._points, index, point, axis=0)
        print(self._points)

    def getDimension(self):
        """
        Returns the length of the vector returned by a call to Path.sample()
        """
        return self._points.shape[1]

    def sample(self, t):
        """For a given t in [0,1], find the coordinates of the Bezier curve at that t"""
        arr = self._points
        while(arr.shape[0] > 1):
            newarr = np.zeros((arr.shape[0]-1, arr.shape[1]))
            for i in range(arr.shape[0]-1):
                newarr[i] = lerp(arr[i],arr[i+1], t)
            arr=newarr
        return arr

class ControlPoint():
    def __init__(self, center, handle1, handle2 = None):
        self._center = center
        self._handle1 = handle1
        self._handle2 = handle2 if handle2 else handle1 # If handle2 specified, sharp corner

    def makeBezier(self, next):
        return Bezier(np.array((self._center, self._handle2, next._handle1, next._center)))

class CompositeBezier(Bezier):
    def __init__(self, control_points):
        self._control_points = control_points
        self._beziers = []
        self.generateBeziers()

    def generateBeziers(self):
        self._beziers = []
        for i in range(len(self._control_points)-1):
            self._beziers += [self._control_points[i].makeBezier(self._control_points[i+1])]
        self._maxT = len(self._beziers)

    def sample(self, t):
        choice = int(t-1) if t==self.getMaxT() else int(t)
        t = 1 if t ==self.getMaxT() else t%1
        return self._beziers[choice].sample(t)


def lerp(a, b, t):
    return b*t + a*(1-t)

if __name__ == '__main__':
    a = Bezier(np.array([[0,0],[1,0]]))
    a.addPoint([.5,1], 1)
    print(a.toArr(20))
