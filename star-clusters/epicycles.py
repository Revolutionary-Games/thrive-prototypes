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

'''

class AstroBody:
    pass

class Probe: # we really need a better name here
    pass





