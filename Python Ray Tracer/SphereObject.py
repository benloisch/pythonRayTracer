import ColorObject
import Vector
import math
import TraceRay

class Sphere:
    """Sphere object class"""
    def __init__(self):
        """assign sphere attributes"""
        self.radius = 0
        self.xOrigin = 0
        self.yOrigin = 0
        self.zOrigin = 0
        self.quadFormA = 0
        self.quadFormB = 0
        self.quadFormC = 0
        self.B4ACRoot = -1
        self.t = 0
        self.xIntersection = 0
        self.yIntersection = 0
        self.zIntersection = 0
        self.xNormal = 0
        self.yNormal = 0
        self.zNormal = 0

        self.t = 0

        #lighting variables
        self.pointLightXorigin = 0
        self.pointLightYorigin = 0
        self.pointLightZorigin = 0
        self.ambient = 0
        self.diffuse = 0
        self.specular = 0
        self.specularP = 0

        #set reflection on or off
        self.reflection = False

        #length variable
        self.length = 0

        #color variables
        self.sphereColor = ColorObject.Color()
        self.sphereColorFinal = ColorObject.Color()

    def setSphereColorRed(self, red):
        self.sphereColor.setRed(red)

    def setSphereColorGreen(self, green):
        self.sphereColor.setGreen(green)

    def setSphereColorBlue(self, blue):
        self.sphereColor.setBlue(blue)

    def getRedFinal(self):
        return self.sphereColorFinal.getRed()

    def getGreenFinal(self):
        return self.sphereColorFinal.getGreen()

    def getBlueFinal(self):
        return self.sphereColorFinal.getBlue()

    def setReflection(self, boolSet):
        self.reflection = boolSet

    def setSpecularP(self, pVal):
        self.specularP = pVal

    def setSpecular(self, lightIntense):
        self.specular = lightIntense

    def setAmbient(self, lightIntense):
        self.ambient = lightIntense

    def setDiffuse(self, lightIntense):
        self.diffuse = lightIntense

    def setPosition(self, xpos, ypos, zpos):
        self.xOrigin = xpos
        self.yOrigin = ypos
        self.zOrigin = zpos

    def setRadius(self, rad):
        self.radius = rad

    def setPointLightOrigin(self, x, y, z):
        self.pointLightXorigin = x
        self.pointLightYorigin = y
        self.pointLightZorigin = z

    def calculateIntersectionsShadow(self, lightRay):
        self.quadFormA = (lightRay.getX() * lightRay.getX()) + (lightRay.getY() * lightRay.getY()) + (lightRay.getZ() * lightRay.getZ())
        self.quadFormB = 2 * ((lightRay.getX() * (lightRay.getXorigin() - self.xOrigin)) + (lightRay.getY() * (lightRay.getYorigin() - self.yOrigin)) + (lightRay.getZ() * (lightRay.getZorigin() - self.zOrigin)))
        self.quadFormC = (((lightRay.getXorigin() - self.xOrigin) ** 2) + ((lightRay.getYorigin() - self.yOrigin) ** 2) + ((lightRay.getZorigin() - self.zOrigin) ** 2)) - (self.radius ** 2)
        self.B4ACRoot = (self.quadFormB * self.quadFormB) - (4 * self.quadFormA * self.quadFormC)

        if self.B4ACRoot >= 0:
            self.t = (-self.quadFormB - math.sqrt(self.B4ACRoot)) / 2
            if self.t <= 0:
                return False
            else:
                return True
        else:
            return False

    def calculateIntersectionsDepth(self, mainRay):

        self.quadFormA = (mainRay.getX() * mainRay.getX()) + (mainRay.getY() * mainRay.getY()) + (mainRay.getZ() * mainRay.getZ())
        self.quadFormB = 2 * ((mainRay.getX() * (mainRay.getXorigin() - self.xOrigin)) + (mainRay.getY() * (mainRay.getYorigin() - self.yOrigin)) + (mainRay.getZ() * (mainRay.getZorigin() - self.zOrigin)))
        self.quadFormC = (((mainRay.getXorigin() - self.xOrigin) ** 2) + ((mainRay.getYorigin() - self.yOrigin) ** 2) + ((mainRay.getZorigin() - self.zOrigin) ** 2)) - (self.radius ** 2)
        self.B4ACRoot = (self.quadFormB * self.quadFormB) - (4 * self.quadFormA * self.quadFormC)

        if self.B4ACRoot >= 0:
            t0 = (-self.quadFormB + math.sqrt(self.B4ACRoot)) / 2
            t1 = (-self.quadFormB - math.sqrt(self.B4ACRoot)) / 2

            if t0 > 0 and t1 > 0:
                self.t = t1

            if t0 == t1:
                self.t = t0

            if t0 < t1:
                self.t = 0

            if t0 < 0 and t1 < 0:
                self.t = 0
        else:
            self.t = 0


        self.xIntersection = mainRay.getXorigin() + (self.t * mainRay.getX())
        self.yIntersection = mainRay.getYorigin() + (self.t * mainRay.getY())
        self.zIntersection = mainRay.getZorigin() + (self.t * mainRay.getZ())

        self.length = math.sqrt(((self.xIntersection - mainRay.getXorigin()) ** 2) + ((self.yIntersection - mainRay.getYorigin()) ** 2) + ((self.zIntersection - mainRay.getZorigin()) ** 2))
        if(self.length <= 0):
            return 100000
        else:
            return self.length

    def calculateLighting(self, mainRay, sphereObjects, planeObjects, mVal):
        #calculate diffuse and ambient
        lightVec = Vector.Vector()
        lightVec.setX(self.pointLightXorigin - self.xIntersection)
        lightVec.setY(self.pointLightYorigin - self.yIntersection)
        lightVec.setZ(self.pointLightZorigin - self.zIntersection)
        lightVec.setXorigin(self.xIntersection)
        lightVec.setYorigin(self.yIntersection)
        lightVec.setZorigin(self.zIntersection)
        lightVec.normalize()
        mainRayBack = Vector.Vector()
        mainRayBack.setX(mainRay.getXorigin() - self.xIntersection)
        mainRayBack.setY(mainRay.getYorigin() - self.yIntersection)
        mainRayBack.setZ(mainRay.getZorigin() - self.zIntersection)
        mainRayBack.normalize()

        self.xNormal = (self.xIntersection - self.xOrigin) / self.radius
        self.yNormal = (self.yIntersection - self.yOrigin) / self.radius
        self.zNormal = (self.zIntersection - self.zOrigin) / self.radius

        dotProdLightNormal = (lightVec.getX() * self.xNormal) + (lightVec.getY() * self.yNormal) + (lightVec.getZ() * self.zNormal)

        if(dotProdLightNormal < 0):
            dotProdLightNormal = 0

        self.sphereColorFinal.setRed(self.sphereColor.getRed() * self.ambient)
        self.sphereColorFinal.setGreen(self.sphereColor.getGreen() * self.ambient)
        self.sphereColorFinal.setBlue(self.sphereColor.getBlue() * self.ambient)

        self.sphereColorFinal.addRed(self.sphereColor.getRed() * self.diffuse * dotProdLightNormal)
        self.sphereColorFinal.addGreen(self.sphereColor.getGreen() * self.diffuse * dotProdLightNormal)
        self.sphereColorFinal.addBlue(self.sphereColor.getBlue() * self.diffuse * dotProdLightNormal)

        if self.reflection == True:
            #Here we will all the object intersections from greatest to least
            #After that, we then test interseciton point on the object and get color. if it has reflection quality, do this again on that sphere
            reflectedRay = Vector.Vector()
            nDotV = ((self.xNormal * mainRayBack.getX()) + (self.yNormal * mainRayBack.getY()) + (self.zNormal * mainRayBack.getZ()))
            reflectedRay.setX((2 * nDotV * self.xNormal) - mainRayBack.getX())
            reflectedRay.setY((2 * nDotV * self.yNormal) - mainRayBack.getY())
            reflectedRay.setZ((2 * nDotV * self.zNormal) - mainRayBack.getZ())
            reflectedRay.normalize()
            reflectedRay.setXorigin(self.xIntersection)
            reflectedRay.setYorigin(self.yIntersection)
            reflectedRay.setZorigin(self.zIntersection)
            reflectedColor = ColorObject.Color()
            reflectedColor = TraceRay.findIntersectionDepth(reflectedRay, planeObjects, sphereObjects, -1, mVal)

            if reflectedColor.getGreen() > 0 or reflectedColor.getRed() > 0 or reflectedColor.getBlue() > 0:
                self.sphereColorFinal.addRed(reflectedColor.getRed())
                self.sphereColorFinal.addGreen(reflectedColor.getGreen())
                self.sphereColorFinal.addBlue(reflectedColor.getBlue())

        if self.reflection == False:
            #calculate specular shading and set final rgb to sphereColorFinal and calculate shadow rays
            #hnumerator and hdenominator are used to calculate the bisector vector between lightvector and viewing vector for SPECULARITY
            hNumerator = Vector.Vector()
            hNumerator.setX(mainRayBack.getX() + lightVec.getX())
            hNumerator.setY(mainRayBack.getY() + lightVec.getY())
            hNumerator.setZ(mainRayBack.getZ() + lightVec.getZ())

            hDenominator = math.sqrt((hNumerator.getX() ** 2) + (hNumerator.getY() ** 2) + (hNumerator.getZ() ** 2))

            hNumerator.setX(hNumerator.getX() / hDenominator)
            hNumerator.setY(hNumerator.getY() / hDenominator)
            hNumerator.setZ(hNumerator.getZ() / hDenominator)

            dotProdHandNormal = ((hNumerator.getX() * self.xNormal) + (hNumerator.getY() * self.yNormal) + (hNumerator.getZ() * self.zNormal))

            self.sphereColorFinal.addRed(self.sphereColor.getRed() * self.specular * (dotProdHandNormal ** self.specularP))
            self.sphereColorFinal.addGreen(self.sphereColor.getGreen() * self.specular * (dotProdHandNormal ** self.specularP))
            self.sphereColorFinal.addBlue(self.sphereColor.getBlue() * self.specular * (dotProdHandNormal ** self.specularP))

            sizeOfSphereObjects = len(sphereObjects)

            intersection = False

            for n in range(0, sizeOfSphereObjects):
                #test for intersections
                if n != mVal:
                    intersection = sphereObjects[n].calculateIntersectionsShadow(lightVec)

                if intersection == True:
                    self.sphereColorFinal.setRed(self.sphereColor.getRed() * self.ambient)
                    self.sphereColorFinal.setGreen(self.sphereColor.getGreen() * self.ambient)
                    self.sphereColorFinal.setBlue(self.sphereColor.getBlue() * self.ambient)

    def setOpaqueColor(self, mainRay):
        #calculate diffuse and ambient
        lightVec = Vector.Vector()
        lightVec.setX(self.pointLightXorigin - self.xIntersection)
        lightVec.setY(self.pointLightYorigin - self.yIntersection)
        lightVec.setZ(self.pointLightZorigin - self.zIntersection)
        lightVec.setXorigin(mainRay.getXorigin())
        lightVec.setYorigin(mainRay.getYorigin())
        lightVec.setZorigin(mainRay.getZorigin())
        lightVec.normalize()
        mainRayBack = Vector.Vector()
        mainRayBack.setX(mainRay.getXorigin() - self.xIntersection)
        mainRayBack.setY(mainRay.getYorigin() - self.yIntersection)
        mainRayBack.setZ(mainRay.getZorigin() - self.zIntersection)
        mainRayBack.setXorigin(mainRay.getXorigin())
        mainRayBack.setYorigin(mainRay.getYorigin())
        mainRayBack.setZorigin(mainRay.getZorigin())
        mainRayBack.normalize()

        self.xNormal = (self.xIntersection - self.xOrigin) / self.radius
        self.yNormal = (self.yIntersection - self.yOrigin) / self.radius
        self.zNormal = (self.zIntersection - self.zOrigin) / self.radius

        dotProdLightNormal = (lightVec.getX() * self.xNormal) + (lightVec.getY() * self.yNormal) + (lightVec.getZ() * self.zNormal)

        if(dotProdLightNormal < 0):
            dotProdLightNormal = 0

        self.sphereColorFinal.setRed(self.sphereColor.getRed() * self.ambient)
        self.sphereColorFinal.setGreen(self.sphereColor.getGreen() * self.ambient)
        self.sphereColorFinal.setBlue(self.sphereColor.getBlue() * self.ambient)

        self.sphereColorFinal.addRed(self.sphereColor.getRed() * self.diffuse * dotProdLightNormal)
        self.sphereColorFinal.addGreen(self.sphereColor.getGreen() * self.diffuse * dotProdLightNormal)
        self.sphereColorFinal.addBlue(self.sphereColor.getBlue() * self.diffuse * dotProdLightNormal)

        #calculate specular shading and set final rgb to sphereColorFinal
        #hnumerator and hdenominator are used to calculate the bisector vector between lightvector and viewing vector for SPECULARITY
        hNumerator = Vector.Vector()
        hNumerator.setX(mainRayBack.getX() + lightVec.getX())
        hNumerator.setY(mainRayBack.getY() + lightVec.getY())
        hNumerator.setZ(mainRayBack.getZ() + lightVec.getZ())

        hDenominator = math.sqrt((hNumerator.getX() ** 2) + (hNumerator.getY() ** 2) + (hNumerator.getZ() ** 2))

        hNumerator.setX(hNumerator.getX() / hDenominator)
        hNumerator.setY(hNumerator.getY() / hDenominator)
        hNumerator.setZ(hNumerator.getZ() / hDenominator)

        dotProdHandNormal = ((hNumerator.getX() * self.xNormal) + (hNumerator.getY() * self.yNormal) + (hNumerator.getZ() * self.zNormal))

        self.sphereColorFinal.addRed(self.sphereColor.getRed() * self.specular * (dotProdHandNormal ** self.specularP))
        self.sphereColorFinal.addGreen(self.sphereColor.getGreen() * self.specular * (dotProdHandNormal ** self.specularP))
        self.sphereColorFinal.addBlue(self.sphereColor.getBlue() * self.specular * (dotProdHandNormal ** self.specularP))
