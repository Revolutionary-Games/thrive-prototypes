# python 2.7

'''
Wherein I log my work on this planetary-system idea, 
which throws physics out the window and calculates motion using epicycles,
and gravity using the Hill Sphere approximation that any small object is only 
gravitationally affected by one astronomical body at one time.

Geometric approximations are the name of the game here -- we want it to be possible
to automate path-planning, and this would be very difficult in a fully chaotic system,
so instead we'll do something based on "orbits" and "transfers".

Orbits are stable configurations that a spacecraft could occupy for a length of time.
This includes orbits around planets, moons, stars, and lagrange points. We'll likely 
only consider circular orbits as these stable configurations.

Transfers are the paths that take us from one orbit to another. These will probably 
be quite complicated. We take the total change in gravitational potential, factor in 
the starting kinetic energy, and then we know the final kinetic energy, and fuel needs.

Note: Take care when switching reference frames -- when moving in/out of Hill Spheres.

If we restrict ourselves to only motion along the ecliptic, then the coordinates of an 
object currently within a certain body's Hill Sphere can be polar wrt parent body. Orbits 
can be characterized entirely by orbital radius -- the phase angle is important in 
timing-sensitive paths, but for path-planning over the ITN this is moot, as paths are 
generally slow but cheap.

The data model should be rather simple: Every body controls the things within its 
Hill Sphere, and only those, but not within sub-spheres. No two Hill Spheres will 
ever intersect. So, we can model the whole shebang as a tree -- with every orbit being 
tied to a particular node, and every transfer being a walk of the tree.

'''

import math
from sortedcontainers import SortedSet # http://grantjenks.com/docs/sortedcontainers/

def hill(dist, m_c, m_p):
    '''
    Returns the full Hill radius of the child body.
    '''
    return dist * (m_c / (3.0 * m_p)) ** (1/3.0)

class AstroBody:
    def __init__(self, r, m, phase = 0, parent = None, isLPoint = False):
        self.parent = parent
        self.r = r # the orbital radius, not radius of the body itself
        self.m = m
        self.phase = phase
        self.hill = 0
        self.children = {}
        '''
        Records orbital lanes available for AstroBodies.
        Any radius within some range (x_{2i}, x_{2i + 1}) is available.
        Any radius within some range (x_{2i - 1}, x_{2i}) is not.
        '''
        self.available = SortedSet([0])

        if parent is not None:
            self.hill = hill(r, m, parent.m)
            
            rin = self.parent.available.bisect(r - self.hill)
            rout = self.parent.available.bisect_left(r + self.hill)
            if rin != rout or not rin % 2:
                raise Exception("Can't place within path of sibling hill sphere")

            self.parent.available ^= SortedSet([r - self.hill, r + self.hill])

            self.parent.children[r] = self
            if not isLPoint:
                '''
                add L1, L2 to self -- complicated, these must stay collinear
                if they're children of self, then positioning them at Hill radius
                will make that work, but we must still ensure alignment -- maybe 
                the better option is to force their positioning somehow
                '''
                # add L3, L4, L5 to parent
                # Todo -- assign some effective mass to the lagrange points
                AstroBody(r, 0, pi + phase, parent, True) # L3
                AstroBody(r, 0, pi * 1.0 / 3 + phase, parent, True) # L4 (or is it L5?)
                AstroBody(r, 0, pi * 5.0 / 3 + phase, parent, True) # L5 (or is it L4?)
    def addChild(self, r, m, phase = 0):
        '''
        Adds a child to this body -- tries to pack the child in as close 
        to target orbital radius as possible (since it must avoid overlapping Hills)
        '''
        massrat = (m / (3.0 * self.m)) ** (1/3.0)



class Projectile:
    def __init__(self):
        pass
    pass





