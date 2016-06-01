import numpy as np;

#
# Usage: python3 srtm2stl.py > terrain.stl
#

SAMPLES=1201
NODATA=-32768
A00='hgt/N42E076.hgt'
A10='hgt/N42E077.hgt'
A01='hgt/N43E076.hgt'
A11='hgt/N43E077.hgt'

#x=np.arange(0,SAMPLES-1,1)
#y=np.arange(0,SAMPLES-1,1)

with open(A00) as A00_data:
    Zx = np.fromfile(A00_data, np.dtype('>i2'), SAMPLES*SAMPLES).reshape((SAMPLES, SAMPLES))

with open(A10) as A10_data:
    tempx = np.fromfile(A10_data, np.dtype('>i2'), SAMPLES*SAMPLES).reshape((SAMPLES, SAMPLES))
    ZZx=np.concatenate((Zx, tempx), axis=1)

with open(A01) as A01_data:
    Zy = np.fromfile(A01_data, np.dtype('>i2'), SAMPLES*SAMPLES).reshape((SAMPLES, SAMPLES))

with open(A11) as A11_data:
    tempy = np.fromfile(A11_data, np.dtype('>i2'), SAMPLES*SAMPLES).reshape((SAMPLES, SAMPLES))
    ZZy=np.concatenate((Zy, tempy), axis=1)

Z=np.concatenate((ZZy, ZZx), axis=0)

# Remove NODATA values
for i in range(1, 2*SAMPLES-1):
    for j in range(1, 2*SAMPLES-1):
        if Z[i,j] == NODATA:
            Z[i,j] = Z[i-1,j]

# Get City subzone
coordx=76.895833
coordy=43.2775

CI=int((2400//2)*(coordx-76))
CJ=int((2400//2)*(coordy-42))

CI=2402-CI
CJ=2402-CJ

deltaI=300
deltaJ=300

print(CI)
print(CJ)

Zsmall=Z[CI-deltaI:CI+deltaI, CJ-deltaJ:CJ+deltaJ]

dims=np.shape(Zsmall)

print(dims[0])
print(dims[1])

print("solid AlmatyTerrain")

for i in range(1, dims[0]-1):
    x=i*90
    for j in range(1, dims[1]-1):
        y=j*90

        a=np.array([x,y,Zsmall[i,j]])
        b=np.array([x+90,y,Zsmall[i+1,j]])
        c=np.array([x,y+90,Zsmall[i,j+1]])
        d=np.array([x+90,y+90,Zsmall[i+1,j+1]])
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
