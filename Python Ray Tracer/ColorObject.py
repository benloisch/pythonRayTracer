class Color:
    """makes a rgb color with other attributes"""
    def __init__(self):
        """define attributes of color"""
        self.red = 0
        self.green = 0
        self.blue = 0

    def addRed(self, colRed):
        self.red += colRed
        if self.red > 255:
            self.red = 255

    def addGreen(self, colGreen):
        self.green += colGreen
        if self.green > 255:
            self.green = 255

    def addBlue(self, colBlue):
        self.blue += colBlue
        if self.blue > 255:
            self.blue = 255

    def setRed(self, colRed):
        self.red = colRed

    def setGreen(self, colGreen):
        self.green = colGreen

    def setBlue(self, colBlue):
        self.blue = colBlue

    def setSpecularity(self, spec):
        self.specularity = spec

    def setDiffuse(self, diff):
        self.diffuse = diff

    def setAmbient(self, amb):
        self.ambient = amb

    def getRed(self):
        return self.red

    def getGreen(self):
        return self.green

    def getBlue(self):
        return self.blue
