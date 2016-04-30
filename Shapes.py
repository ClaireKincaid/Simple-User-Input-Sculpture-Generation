from Geometry import *
from math import pi

hex1 = n_Sided_Polygon(6,12.35*2/sqrt(3))
hex2 = n_Sided_Polygon(6,12.35*2/sqrt(3))

rot1 = Rotation( 120,None,128*2)
rot2 = Rotation(-60,None,128*2)
di   = Inward_Harmonic_Dilation(.3,None,128*2)

anim = Animation(hex1,[rot1,di])
anim.add_shape(hex2,[rot2,di])

anim.write_to_scad('piece.scad')



rot1 = Rotation( 240,None,128*4)
rot2 = Rotation(-120,None,128*4)
di   = Cosine_Harmonic_Dilation(pi/2,None,128*4)
di2  = Dilation(1.2,None,128*4)

anim = Animation(hex1,[rot1,di,di2])
anim.add_shape(hex2,[rot2,di,di2])

anim.write_to_scad('capstone1.scad')



rot1 = Rotation(-240,None,128*4)
rot2 = Rotation( 120,None,128*4)

anim = Animation(hex1,[rot1,di,di2])
anim.add_shape(hex2,[rot2,di,di2])

anim.write_to_scad('capstone2.scad')