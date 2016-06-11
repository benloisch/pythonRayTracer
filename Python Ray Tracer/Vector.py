class Vector:
    """Vector class used to perform vector calculations"""
    def __init__(self):
        """properties of a vector, x, y, z"""
        self.x = 0
        self.y = 0
        self.z = 0

        self.xOrigin = 0
        self.yOrigin = 0
        self.zOrigin = 0

        self.rayLength = 0

    def setLength(self, len):
        self.rayLength = len

    def getLength(self):
        return self.rayLength

    def setX(self, xVal):
        """set x val"""
        self.x = xVal

    def setY(self, yVal):
        """set y val"""
        self.y = yVal

    def setZ(self, zVal):
        """set z val"""
        self.z = zVal

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def setXorigin(self, xVal):
        self.xOrigin = xVal

    def setYorigin(self, yVal):
        self.yOrigin = yVal

    def setZorigin(self, zVal):
        self.zOrigin = zVal

    def getXorigin(self):
        return self.xOrigin

    def getYorigin(self):
        return self.yOrigin

    def getZorigin(self):
        return self.zOrigin

    def normalize(self):
        xUnChanged = self.x
        yUnChanged = self.y
        zUnChanged = self.z
        self.x = xUnChanged / ((xUnChanged  * xUnChanged ) + (yUnChanged  * yUnChanged ) + (zUnChanged  * zUnChanged)) ** 0.5
        self.y = yUnChanged / ((xUnChanged  * xUnChanged ) + (yUnChanged  * yUnChanged ) + (zUnChanged  * zUnChanged)) ** 0.5
        self.z = zUnChanged / ((xUnChanged  * xUnChanged ) + (yUnChanged  * yUnChanged ) + (zUnChanged  * zUnChanged)) ** 0.5

    def setMainRay(self, mainRay, cam):
        self.x = mainRay.getX() - cam.m41
        self.y = mainRay.getY() - cam.m42
        self.z = mainRay.getZ() - cam.m43

        self.xOrigin = cam.getX()
        self.yOrigin = cam.getY()
        self.zOrigin = cam.getZ()

    def printMainRay(self):#testing purposes
        print("MAIN RAY")
        print(self.x, " ", self.y, " ", self.z)