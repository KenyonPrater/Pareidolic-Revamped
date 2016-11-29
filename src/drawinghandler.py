import PIL.Image as Image
import numpy as np
np.set_printoptions(threshold='nan')

class Drawing():
    """
    An image that can be painted in with brushes
    Serves as the backend for Pareidolic-Revamped's
    procedural images.
    """
    def __init__(self,width = 256, height = 256):
        """
        Create a new Drawing, a width x height array of RGBA pixels
        @param width - the width of the Drawing to be created
        @param height - the height of the Drawing
        """
        self._height = height
        self._width = width
        self._data = np.zeros((width, height, 4), dtype='uint8');

    def getWidth(self):
        """Returns the width of the Drawing"""
        return self._width

    def getHeight(self):
        """Returns the height of this Drawing"""
        return self._height

    def toImage(self):
        """
        Creates an RGBA image from PIL of this Drawing which can then
        be saved or displayed
        """
        img = Image.fromarray(self._data, 'RGBA')
        return img

    def applyBrush(self,pos,color,radius = 3,hardness=.75):
        """
        Applies a brush with specified attributes onto the canvas
        @param pos - 2-tuple (x, y) specifying the center pixel of the brush.
        @param color - 4-tuple (r, g, b, a), where (0,0,0,0) is transparent,
                       (255,0,0,255) is solid red, etc
        @param radius - the radius of the brush in pixels
        @param hardness - the hardness, as a scale from 1 (hardest) to 0
        """
        brush = generateBrush(radius, hardness)
        for i in range(0, int(2*radius+1)):
            for j in range(0, int(2*radius+1)):
                x = pos[0] + (i - radius)
                y = pos[1] + (j - radius)
                if x >= 0 and x < self._width and y >= 0 and y < self._height:
                    weight = brush[i,j]/255.
                    weighted_color = (color[0], color[1], color[2], int(color[3]*weight))
                    self._data[x,y] = blendRGBA(weighted_color, self._data[x,y])

    def applyBrush(self,pos,color,brush):
        """
        Alternate form of applyBrush that uses a custom brush rather
        than generating a new one on each call.
        @param pos - 2-tuple (x, y) specifying the center pixel of the brush.
        @param color - 4-tuple (r, g, b, a), where (0,0,0,0) is transparent,
                       (255,0,0,255) is solid red, etc
        @param brush - a 2d numpy array with weights normalized between 255-0.
                       opacity is multiplied by the weights prior to painting.
        """
        for i in range(0, brush.shape[0]):
            for j in range(0, brush.shape[1]):
                x = pos[0] + (i - int(brush.shape[0]/2))
                y = pos[1] + (j - int(brush.shape[0]/2))
                if x >= 0 and x < self._width and y >= 0 and y < self._height:
                    weight = brush[i,j]/255.
                    weighted_color = (color[0], color[1], color[2], int(color[3]*weight))
                    self._data[x,y] = blendRGBA(weighted_color, self._data[x,y])

def blendRGBA(rgba_new, rgba_base):
    """
    Helper function to blend two RGBA colors, one on top of the other.
    @param rgba_new - a 4-tuple (r, g, b, a) representing the foreground color
    @param rgba_base - a 4-tuple (r, g, b, a) representing the background color
    @return a 4-tuple (r, g, b, a) containing the combined color.
    """
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
    """
    Given a radius and hardness, create a 2d numpy array of values from 0-255
    that represents a circular brush with those specifications
    """
    def getWeight(x,y, rad=3, hard=0.75):
        x_cen, y_cen = x-rad, y-rad
        dist = (x_cen**2+y_cen**2)**0.5
        inner_radius = hard*rad
        t = (rad - dist) / (0.001 + rad - inner_radius) # avoid divide by 0 error, generate weight to interpolate b
        return np.clip(t*255, 0, 255)

    arr = np.fromfunction(getWeight, (radius*2+1, radius*2+1), dtype='int16', rad=radius, hard=hardness) #HACK the dtype really should get converted to u8
    return arr


if __name__ == '__main__':
    dr = Drawing()
    brush = generateBrush(100,.75)
    dr.applyBrush((100,128), (255,0,0,255),brush)
    dr.applyBrush((256-100,128), (0,255,0,255),brush)
    im = dr.toImage()
    im.save('asdf.png', "PNG")
