import PIL.Image as Image
import numpy as np
np.set_printoptions(threshold='nan')

class Drawing():
    def __init__(self,height = 256, width = 256):
        self._height = height
        self._width = width
        self._data = np.zeros((width, height, 4), dtype='uint8');

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def toImage(self):
        img = Image.fromarray(self._data, 'RGBA')
        return img

    def applyBrush(self,pos,color,radius = 3,hardness=.75):
        brush = generateBrush(radius, hardness)
        for i in range(0, int(2*radius+1)):
            for j in range(0, int(2*radius+1)):
                x = pos[0] + (i - radius)
                y = pos[1] + (j - radius)
                if x >= 0 and x < self._width and y >= 0 and y < self._height:
                    weight = brush[i,j]/255.
                    weighted_color = (color[0], color[1], color[2], int(color[3]*weight))
                    self._data[x,y] = blendRGBA(weighted_color, self._data[x,y])

def blendRGBA(rgba_new, rgba_base):
    if (rgba_new[3] == 0 and rgba_base[3] == 0): #handle an ugly divide by 0 err
        return (0,0,0,0)
    a1 = rgba_new[3] / 255.
    a2 = rgba_base[3] / 255.
    alpha = a1 + a2 - a1*a2
    col = [0,0,0]
    for i in range(3):
        col[i] = (rgba_new[i]*a1 + rgba_base[i]*a2*(1-a1))/(alpha)
    return (col[0], col[1], col[2], alpha*255)

def generateBrush(radius, hardness):
    def getWeight(x,y, rad=3, hard=0.75):
        x_cen, y_cen = x-rad, y-rad
        dist = (x_cen**2+y_cen**2)**0.5
        inner_radius = hard*rad
        t = (rad - dist) / (0.001 + rad - inner_radius) # avoid divide by 0 error, generate weight to interpolate by
        return np.clip(t*255, 0, 255)

    arr = np.fromfunction(getWeight, (radius*2+1, radius*2+1), dtype='int16', rad=radius, hard=hardness)
    return arr


if __name__ == '__main__':
    dr = Drawing()
    dr.applyBrush((100,128), (255,0,0,255),(100),.5)
    dr.applyBrush((256-100,128), (0,255,0,255),(100),.5)
    im = dr.toImage()
    im.save('asdf.png', "PNG")
