import numpy as np;

#
# Usage: python3 srtm2stl.py > terrain.stl
#

SAMPLES=1201
hgt_file='hgt/N43E076.hgt'

x=np.arange(0,SAMPLES-1,1)
y=np.arange(0,SAMPLES-1,1)

with open(hgt_file) as hgt_data:
    Z = np.fromfile(hgt_data, np.dtype('>i2'), SAMPLES*SAMPLES).reshape((SAMPLES, SAMPLES))

print("solid AlmatyTerrain")
for i in range(1, SAMPLES-1):
    x=i*90
    for j in range(1, SAMPLES-1):
        y=j*90
        a=np.array([x,y,Z[i,j]])
        b=np.array([x+90,y,Z[i+1,j]])
        c=np.array([x,y+90,Z[i,j+1]])
        d=np.array([x+90,y+90,Z[i+1,j+1]])
        nabc=np.cross(b-a, c-a)
        ncbd=np.cross(c-d,b-d)
        nabc=nabc/np.sqrt(nabc.dot(nabc))
        ncbd=ncbd/np.sqrt(ncbd.dot(ncbd))

        # first triangle
        print("facet normal ", nabc[0], " ", nabc[1], " ", nabc[2])
        print("outer loop")
        print("vertex ", a[0], " ", a[1], " ", a[2])
        print("vertex ", b[0], " ", b[1], " ", b[2])
        print("vertex ", c[0], " ", c[1], " ", c[2])
        print("endloop")
        print("endfacet")

        # second triangle
        print("facet normal ", ncbd[0], " ", ncbd[1], " ", ncbd[2])
        print("outer loop")
        print("vertex ", b[0], " ", b[1], " ", b[2])
        print("vertex ", d[0], " ", d[1], " ", d[2])
        print("vertex ", c[0], " ", c[1], " ", c[2])
        print("endloop")
        print("endfacet")
