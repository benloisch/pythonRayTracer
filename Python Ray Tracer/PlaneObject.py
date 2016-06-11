import math
import ColorObject
import Vector
import TraceRay

class Plane:
    """Plane objects"""
    def __init__(self):
        """assign plane attributes"""
        #used to find the point of intersection of the ray and plane
        self.pntXintersect = 0
        self.pntYintersect = 0
        self.pntZintersect = 0

        #a point on the plane used for intersection calculations
        self.pointOnPlaneX = 0
        self.pointOnPlaneY = 0
        self.pointOnPlaneZ = 0

        #normal to the plane
        self.planeNormalX = 0
        self.planeNormalY = 0
        self.planeNormalZ = 0

        #lighting variables
        self.pointLightXorigin = 0
        self.pointLightYorigin = 0
        self.pointLightZorigin = 0
        self.ambient = 0
        self.diffuse = 0
        self.specular = 0
        self.specularP = 0

        #check for reflections or not
        self.reflection = False

        #test depth
        self.length = 0

        #color of plane
        self.planeColor = ColorObject.Color()
        self.planeColorFinal = ColorObject.Color()

    def setSpecularP(self, specP):
        self.specularP = specP

    def getRedFinal(self):
        return self.planeColorFinal.getRed()

    def getGreenFinal(self):
        return self.planeColorFinal.getGreen()

    def getBlueFinal(self):
        return self.planeColorFinal.getBlue()

    def setAmbient(self, lightIntense):
        self.ambient = lightIntense

    def setDiffuse(self, lightIntense):
        self.diffuse = lightIntense

    def setSpecular(self, lightIntense):
        self.specular = lightIntense

    def setPlaneColorRed(self, red):
        self.planeColor.setRed(red)

    def setPlaneColorGreen(self, green):
        self.planeColor.setGreen(green)

    def setPlaneColorBlue(self, blue):
        self.planeColor.setBlue(blue)

    def setPointLightOrigin(self, x, y, z):
        self.pointLightXorigin = x
        self.pointLightYorigin = y
        self.pointLightZorigin = z

    def setReflection(self, boolSet):
        self.reflection = boolSet

    def getReflection(self):
        return self.reflection

    def setPlaneNormal(self, xpn, ypn, zpn):
        self.planeNormalX = xpn
        self.planeNormalY = ypn
        self.planeNormalZ = zpn

    def setPlanePoint(self, xpp, ypp, zpp):
        self.pointOnPlaneX = xpp
        self.pointOnPlaneY = ypp
        self.pointOnPlaneZ = zpp

    def calculateIntersectionsDepth(self, mainRay):
        #find (po - lo(camxyz)) . n
        numerator = ((self.pointOnPlaneX - mainRay.getXorigin()) * self.planeNormalX) + ((self.pointOnPlaneY - mainRay.getYorigin()) * self.planeNormalY) + ((self.pointOnPlaneZ - mainRay.getZorigin()) * self.planeNormalZ)

        #eqaution is Distance = (po - lo) . n / (l . n)
        #po is point on plane
        #lo is point on line
        #n is normal to the plane
        #l is a vector in the direction of the line
        #(.) is the dot product

        #find (l . n)
        denominator = ((mainRay.getX() * self.planeNormalX) + (mainRay.getY() * self.planeNormalY) + (mainRay.getZ() * self.planeNormalZ))

        #find distance from ray origin(camxyz) to point of intersection on plane
        distToPlane = numerator / denominator

        #find (po - lo(camxyz)) . n
        #already pre calculated it in calcNumerator

        #find point of intersection of ray against plane
        #point of intersection is (distance * l + lo)
        self.pntXintersect = (distToPlane * mainRay.getX()) + mainRay.getXorigin()
        self.pntYintersect = (distToPlane * mainRay.getY()) + mainRay.getYorigin()
        self.pntZintersect = (distToPlane * mainRay.getZ()) + mainRay.getZorigin()

        self.length = math.sqrt(((self.pntXintersect - mainRay.getXorigin()) ** 2) + ((self.pntYintersect - mainRay.getYorigin()) ** 2) + ((self.pntZintersect - mainRay.getZorigin()) ** 2))
        if(distToPlane < 0):
            return 100000
        else:
            return self.length

    def calculateLighting(self, mainRay, sphereObjects, planeObjects, nVal):
        #calculate diffuse and ambient
        lightVec = Vector.Vector()
        lightVec.setX(self.pointLightXorigin - self.pntXintersect)
        lightVec.setY(self.pointLightYorigin - self.pntYintersect)
        lightVec.setZ(self.pointLightZorigin - self.pntZintersect)
        lightVec.setXorigin(self.pntXintersect)
        lightVec.setYorigin(self.pntYintersect)
        lightVec.setZorigin(self.pntZintersect)
        lightVec.normalize()
        mainRayBack = Vector.Vector()
        mainRayBack.setX(mainRay.getXorigin() - self.pntXintersect)
        mainRayBack.setY(mainRay.getYorigin() - self.pntYintersect)
        mainRayBack.setZ(mainRay.getZorigin() - self.pntZintersect)
        mainRayBack.normalize()

        dotProdLightNormal = (lightVec.getX() * self.planeNormalX) + (lightVec.getY() * self.planeNormalY) + (lightVec.getZ() * self.planeNormalZ)

        if(dotProdLightNormal < 0):
            dotProdLightNormal = 0

        self.planeColorFinal.setRed(self.planeColor.getRed() * self.ambient)
        self.planeColorFinal.setGreen(self.planeColor.getGreen() * self.ambient)
        self.planeColorFinal.setBlue(self.planeColor.getBlue() * self.ambient)

        self.planeColorFinal.addRed(self.planeColor.getRed() * self.diffuse * dotProdLightNormal)
        self.planeColorFinal.addGreen(self.planeColor.getGreen() * self.diffuse * dotProdLightNormal)
        self.planeColorFinal.addBlue(self.planeColor.getBlue() * self.diffuse * dotProdLightNormal)

        if self.reflection == True:
            #Here we will all the object intersections from greatest to least
            #After that, we then test interseciton point on the object and get color. if it has reflection quality, do another reflection on that object
            #exact reflection off of normal
            reflectedRay = Vector.Vector()
            nDotV = ((self.planeNormalX * mainRayBack.getX()) + (self.planeNormalY * mainRayBack.getY()) + (self.planeNormalZ * mainRayBack.getZ()))
            reflectedRay.setX((2 * nDotV * self.planeNormalX) - mainRayBack.getX())
            reflectedRay.setY((2 * nDotV * self.planeNormalY) - mainRayBack.getY())
            reflectedRay.setZ((2 * nDotV * self.planeNormalZ) - mainRayBack.getZ())
            reflectedRay.normalize()
            reflectedRay.setXorigin(self.pntXintersect)
            reflectedRay.setYorigin(self.pntYintersect)
            reflectedRay.setZorigin(self.pntZintersect)
            reflectedColor = ColorObject.Color()
            reflectedColor = TraceRay.findIntersectionDepth(reflectedRay, planeObjects, sphereObjects, nVal, -1)

            if reflectedColor.getGreen() > 0 or reflectedColor.getRed() > 0 or reflectedColor.getBlue() > 0:
                self.planeColorFinal.setRed(reflectedColor.getRed())
                self.planeColorFinal.setGreen(reflectedColor.getGreen())
                self.planeColorFinal.setBlue(reflectedColor.getBlue())

            sizeOfSphereObjects = len(sphereObjects)

            intersection = False

            for n in range(0, sizeOfSphereObjects):
                #test for intersections
                intersection = sphereObjects[n].calculateIntersectionsShadow(lightVec)
                if intersection == True:
                    self.planeColorFinal.addRed(-0.6 * self.planeColorFinal.getRed())
                    self.planeColorFinal.addGreen(-0.6 * self.planeColorFinal.getGreen())
                    self.planeColorFinal.addBlue(-0.6 * self.planeColorFinal.getBlue())

            if self.planeColorFinal.getRed() > 255:
                self.planeColorFinal.setRed(255)

            if self.planeColorFinal.getGreen() > 255:
                self.planeColorFinal.setGreed(255)

            if self.planeColorFinal.getBlue() > 255:
                self.planeColorFinal.setBlue(255)

            if self.planeColorFinal.getRed() < 0:
                self.planeColorFinal.setRed(0)

            if self.planeColorFinal.getGreen() < 0:
                self.planeColorFinal.setGreen(0)

            if self.planeColorFinal.getBlue() < 0:
                self.planeColorFinal.setBlue(0)


        if self.reflection == False:
            #calculate specular shading and set final rgb to planeColorFinal and calculate shadow rays
            #hnumerator and hdenominator are used to calculate the bisector vector between lightvector and viewing vector for SPECULARITY
            hNumerator = Vector.Vector()
            hNumerator.setX(mainRayBack.getX() + lightVec.getX())
            hNumerator.setY(mainRayBack.getY() + lightVec.getY())
            hNumerator.setZ(mainRayBack.getZ() + lightVec.getZ())

            hDenominator = math.sqrt((hNumerator.getX() ** 2) + (hNumerator.getY() ** 2) + (hNumerator.getZ() ** 2))

            hNumerator.setX(hNumerator.getX() / hDenominator)
            hNumerator.setY(hNumerator.getY() / hDenominator)
            hNumerator.setZ(hNumerator.getZ() / hDenominator)

            dotProdHandNormal = ((hNumerator.getX() * self.planeNormalX) + (hNumerator.getY() * self.planeNormalY) + (hNumerator.getZ() * self.planeNormalZ))

            self.planeColorFinal.addRed(self.planeColor.getRed() * self.specular * (dotProdHandNormal ** self.specularP))
            self.planeColorFinal.addGreen(self.planeColor.getGreen() * self.specular * (dotProdHandNormal ** self.specularP))
            self.planeColorFinal.addBlue(self.planeColor.getBlue() * self.specular * (dotProdHandNormal ** self.specularP))

            sizeOfSphereObjects = len(sphereObjects)

            intersection = False

            for n in range(0, sizeOfSphereObjects):
                #test for intersections
                intersection = sphereObjects[n].calculateIntersectionsShadow(lightVec)
                if intersection == True:
                    self.planeColorFinal.setRed(self.planeColor.getRed() * self.ambient)
                    self.planeColorFinal.setGreen(self.planeColor.getGreen() * self.ambient)
                    self.planeColorFinal.setBlue(self.planeColor.getBlue() * self.ambient)

    def setOpaqueColor(self, mainRay):
        #calculate diffuse and ambient
        lightVec = Vector.Vector()
        lightVec.setX(self.pointLightXorigin - self.pntXintersect)
        lightVec.setY(self.pointLightYorigin - self.pntYintersect)
        lightVec.setZ(self.pointLightZorigin - self.pntZintersect)
        lightVec.setXorigin(mainRay.getXorigin())
        lightVec.setYorigin(mainRay.getYorigin())
        lightVec.setZorigin(mainRay.getZorigin())
        lightVec.normalize()
        mainRayBack = Vector.Vector()
        mainRayBack.setX(mainRay.getXorigin() - self.pntXintersect)
        mainRayBack.setY(mainRay.getYorigin() - self.pntYintersect)
        mainRayBack.setZ(mainRay.getZorigin() - self.pntZintersect)
        mainRayBack.setXorigin(mainRay.getXorigin())
        mainRayBack.setYorigin(mainRay.getYorigin())
        mainRayBack.setZorigin(mainRay.getZorigin())
        mainRayBack.normalize()

        dotProdLightNormal = (lightVec.getX() * self.planeNormalX) + (lightVec.getY() * self.planeNormalY) + (lightVec.getZ() * self.planeNormalZ)

        if(dotProdLightNormal < 0):
            dotProdLightNormal = 0

        self.planeColorFinal.setRed(self.planeColor.getRed() * self.ambient)
        self.planeColorFinal.setGreen(self.planeColor.getGreen() * self.ambient)
        self.planeColorFinal.setBlue(self.planeColor.getBlue() * self.ambient)

        self.planeColorFinal.addRed(self.planeColor.getRed() * self.diffuse * dotProdLightNormal)
        self.planeColorFinal.addGreen(self.planeColor.getGreen() * self.diffuse * dotProdLightNormal)
        self.planeColorFinal.addBlue(self.planeColor.getBlue() * self.diffuse * dotProdLightNormal)

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

        dotProdHandNormal = ((hNumerator.getX() * self.planeNormalX) + (hNumerator.getY() * self.planeNormalY) + (hNumerator.getZ() * self.planeNormalZ))

        self.planeColorFinal.addRed(self.planeColor.getRed() * self.specular * (dotProdHandNormal ** self.specularP))
        self.planeColorFinal.addGreen(self.planeColor.getGreen() * self.specular * (dotProdHandNormal ** self.specularP))
        self.planeColorFinal.addBlue(self.planeColor.getBlue() * self.specular * (dotProdHandNormal ** self.specularP))