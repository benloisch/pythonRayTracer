import ColorObject

#function used for tracing rays onto and beyond a reflection
def getReflectionValue(subRay, object):
    objectColor = ColorObject.Color()
    object.setOpaqueColor(subRay)
    objectColor.setRed(object.getRedFinal())
    objectColor.setGreen(object.getGreenFinal())
    objectColor.setBlue(object.getBlueFinal())
    return objectColor

def findIntersectionDepth(subRay, planeObjects, sphereObjects, nVal, mVal):
    sizeOfPlaneObjects = len(planeObjects)
    sizeOfSphereObjects = len(sphereObjects)

    globalLengthPlane = 100000
    testParticularPlane = 0

    for n in range(0, sizeOfPlaneObjects):
        if n != nVal:
            lengthTest = planeObjects[n].calculateIntersectionsDepth(subRay)#sort by what plane shows first (has the least distance from ray)
            #print("Plane ", n, " length", lengthTest)
            if lengthTest < globalLengthPlane:
                globalLengthPlane = lengthTest
                testParticularPlane = n#record this index for use later

    #draw spheres
    globalLengthSphere = 100000
    testParticularSphere = 0

    for m in range(0, sizeOfSphereObjects):
        if m != mVal:
            lengthTest = sphereObjects[m].calculateIntersectionsDepth(subRay)
            #print("Sphere ", m, " length", lengthTest)
            if lengthTest < globalLengthSphere:
                globalLengthSphere = lengthTest
                testParticularSphere = m#record this index for use later

    blackColor = ColorObject.Color()

    #test whether sphere or plane is closest and then draw that to screen
    if globalLengthPlane < globalLengthSphere:
        return getReflectionValue(subRay, planeObjects[testParticularPlane])
    elif globalLengthSphere < globalLengthPlane:
        return getReflectionValue(subRay, sphereObjects[testParticularSphere])
    else:
        return blackColor



