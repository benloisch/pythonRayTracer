import Vector

class Camera:
    """Virtual Camera used to setup a scene and render an image"""
    def __init__(self):
        """Setup all variables in camera class"""

        self.m11 = 1#make a 4x4 matrix by hand
        self.m12 = 0
        self.m13 = 0
        self.m14 = 0
        self.m21 = 0
        self.m22 = 1
        self.m23 = 0
        self.m24 = 0
        self.m31 = 0
        self.m32 = 0
        self.m33 = 1
        self.m34 = 0
        self.m41 = 0#m41, m42, m43 are the cam translation variables
        self.m42 = 0
        self.m43 = 0
        self.m44 = 1

        self.lookAtVec = Vector.Vector() #this vector is used to point the camera in a particular direction
        #self.tempVector = Vector.Vector() #this vector is used to calculated the main ray

    def setCamXpos(self, xVal):
        self.m41 = xVal

    def setCamYpos(self, yVal):
        self.m42 = yVal

    def setCamZpos(self, zVal):
        self.m43 = zVal

    def getX(self):
        return self.m41

    def getY(self):
        return self.m42

    def getZ(self):
        return self.m43

    def setCamLookAt(self, LAVx, LAVy, LAVz):
        self.lookAtVec.setX(LAVx)
        self.lookAtVec.setY(LAVy)
        self.lookAtVec.setZ(LAVz)

    def createCamMatrix(self):
        right = Vector.Vector()
        up = Vector.Vector()
        forward = Vector.Vector()

        #Cross Product is
		#Cx = AyBz - AzBy
		#Cy = AzBx - AxBz
		#Cz = AxBy - AyBx

    	#First find camera positive z axis of cam by (lookAt.xyz - camOrigin)
        self.lookAtVec.setX(self.lookAtVec.getX() - self.m41)
        self.lookAtVec.setY(self.lookAtVec.getY() - self.m42)
        self.lookAtVec.setZ(self.lookAtVec.getZ() - self.m43)

        #Calculate the right vector (x axis) by taking cross product of world 'up'(0, 1, 0) and lookat vector
        right.setX((1 * self.lookAtVec.getZ()) - (0 * self.lookAtVec.getY()))
        right.setY((0 * self.lookAtVec.getX()) - (0 * self.lookAtVec.getZ()))
        right.setZ((0 * self.lookAtVec.getY()) - (1 * self.lookAtVec.getX()))

        #Calculate camera up vector (y axis) by taking the cross product of lookat vector and right(just above) vector
        up.setX((self.lookAtVec.getY() * right.getZ()) - (self.lookAtVec.getZ() * right.getY()));
        up.setY((self.lookAtVec.getZ() * right.getX()) - (self.lookAtVec.getX() * right.getZ()));
        up.setZ((self.lookAtVec.getX() * right.getY()) - (self.lookAtVec.getY() * right.getX()));

        #Last, calculate forward vector (positive z axis) which is just the lookat vector

        forward.setX(self.lookAtVec.getX())
        forward.setY(self.lookAtVec.getY())
        forward.setZ(self.lookAtVec.getZ())

        right.normalize()
        up.normalize()
        forward.normalize()

        self.m11 = right.getX()
        self.m12 = right.getY()
        self.m13 = right.getZ()

        self.m21 = up.getX()
        self.m22 = up.getY()
        self.m23 = up.getZ()

        self.m31 = forward.getX()
        self.m32 = forward.getY()
        self.m33 = forward.getZ()

    def multVectByCamMatrix(self, mainRay):
        vecXunChanged = mainRay.getX();
        vecYunChanged = mainRay.getY();
        vecZunChanged = mainRay.getZ();

        mainRay.setX((vecXunChanged * self.m11) + (vecYunChanged  * self.m21) + (vecZunChanged * self.m31) + (1 * self.m41))
        mainRay.setY((vecXunChanged * self.m12) + (vecYunChanged  * self.m22) + (vecZunChanged * self.m32) + (1 * self.m42))
        mainRay.setZ((vecXunChanged * self.m13) + (vecYunChanged  * self.m23) + (vecZunChanged * self.m33) + (1 * self.m43))

        return mainRay


    def printCamMatrix(self):#testing purposes
        print(self.m11, " ", self.m12, " ", self.m13, " ", self.m14)
        print(self.m21, " ", self.m22, " ", self.m23, " ", self.m24)
        print(self.m31, " ", self.m32, " ", self.m33, " ", self.m34)
        print(self.m41, " ", self.m42, " ", self.m43, " ", self.m44)