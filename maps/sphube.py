#!/usr/bin/env python
import math
import numpy

'''
Sphube: or Sphere-Cube, the world map-geometry system.

-- Varying area and length scale over surface of sphube --

Eqn 1)
    phi = (sqrt3 / d) * (atan(c + d) - atan(c))
Where:
    d = length of a short line segment on 2x2x2 cube surface
    phi*d = length of said segment when projected onto the
        circumscribed sphere
    c = distance between said segment and the center of the
        face which the segment is on

When we take the limit as d -> 0,

Eqn 2)
    lim d -> 0: phi = sqrt3 / (1 + c^2)

This is much more useful. Let's call this k.

Since k is the multiplier that converts a length on the cube
to the projected length on a sphere, then k^2 is the matching
ratio for an area.
'''

sqrt2 = 2 ** 0.5

sqrt3 = 3 ** 0.5

# Where c measures distance from center of cube face, c=1 for any cube vertex
def length_factor(c):
    sqrt3 / (1 + c * c)

def area_factor(c):
    lfc = length_factor(c)
    return lfc * lfc

def precompute_factors():
    # Using intervals of 0.01
    length_lut = numpy.arange(0.00, 2.88, 0.02)

    numpy.multiply(length_lut, length_lut, length_lut)
    numpy.add(length_lut, 1, length_lut)
    numpy.divide(sqrt3, length_lut, length_lut)

    area_lut = length_lut ** 2
    return length_lut, area_lut

length_lut, area_lut = precompute_factors()

# print length_lut
# print area_lut

def lerp(x, ar):
    # given that each array indexes by centiunits:
    x *= 100
    i = int(x)
    if 0 > i or i >= len(ar) - 1: return None
    j = x - i
    ar_i = ar[i]
    return ar_i + j * (ar[i+1] - ar_i)

# to get the area of a small zone around coords (x,y)
# lerp(hypot(x,y), area_lut) * area-on-face-surface



'''
A single Face of a sphube.

A sphube has 6 faces: A, B, C, D, E, F;
arranged such that when unfolded like so (looking on 
the outer surface):
    A
    BCDE
    F
  the +x direction on each face points rightwards, and
  the +y direction on each points upwards.

The faces of the sphube don't worry about this edges
stitching, that's the sphube's job.


'''
class Face:
    def __init__(self, orientation, dim = 30):
        assert orientation in 'ABCDEF'
        self.orientation = orientation
        self.dim = dim/2 # == max_x == max_y == (-min_x) == (-min_y)
        self.data = numpy.zeros((self.dim*2, self.dim*2)) # indexed in [x][y] order

    def length_metric(self, length, position):
        '''
        Given a short distance on the cube, returns the same distance when projected
        to the sphere
        '''
        hyp = math.hypot(position[0], position[1])
        hyp /= self.dim
        assert hyp <= sqrt2
        return length * lerp(hyp, length_lut)

    def area_metric(self, area, position):
        hyp = math.hypot(position[0], position[1])
        hyp /= self.dim
        assert hyp <= sqrt2
        return area * lerp(hyp, area_lut)

    def latitude(self, position):
        assert -self.dim <= position[0] <= self.dim
        assert -self.dim <= position[1] <= self.dim
        if self.orientation in 'AF':
            # calculate from pole
            lat = math.pi/2 - math.atan(
                math.hypot(position[0], position[1]) / self.dim)
            return lat if self.orientation == 'A' else -lat
        # calculate from equator
        lat = math.atan(position[1] / math.hypot(self.dim, position[0]))
        return lat

    def longitude(self, position):
        assert -self.dim <= position[0] <= self.dim
        assert -self.dim <= position[1] <= self.dim
        x = position[0]
        y = position[1]
        if self.orientation in 'AF':
            # polar
            if x is 0 and y is 0: return 0
            if self.orientation is 'A': y = -y # switch to F if weird
            l = math.atan2(x, y)
            if x < 0:
                l += 2 * math.pi
        elif self.orientation is 'B':
            l = math.atan2(self.dim, -x) - math.pi / 2
        elif self.orientation is 'C':
            l = math.atan2(self.dim, -x)
        elif self.orientation is 'D':
            l = math.atan2(self.dim, -x) + math.pi/2
        elif self.orientation is 'E':
            l = math.atan2(self.dim, -x) + math.pi
        #l -= 7*math.pi/4 # this shifts the prime meridian to avoid a seam within a face
        if l < 0: l += 2*math.pi
        return l



class Sphube:
    def __init__(self, r = 45, face_side = None):
        if face_side is None:
            face_side = r / sqrt3
            self.r = r
        else:
            self.r = face_side * sqrt3
        self.faces = {
            "A": Face("A", face_side),
            "B": Face("B", face_side),
            "C": Face("C", face_side),
            "D": Face("D", face_side),
            "E": Face("E", face_side),
            "F": Face("F", face_side),
        }
