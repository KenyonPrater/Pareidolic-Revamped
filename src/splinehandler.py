import numpy as np

class Bezier():
    def __init__(self, points):
        self._points = points

    def sample(self, t):
        arr = self._points
        while(arr.shape[0] > 1):
            newarr = np.zeros((arr.shape[0]-1, arr.shape[1]))
            for i in range(arr.shape[0]-1):
                newarr[i] = lerp(arr[i],arr[i+1], t)
            arr=newarr
        return arr

def lerp(a, b, t):
    return b*t + a*(1-t)

if __name__ == '__main__':
    a = [[0,0],[1,0],[1,1],[0,1]]
    a = np.array(a)
    b = Bezier(a)
    for i in range(11):
        print(b.sample(i/10.))
