__author__ = 'Ben Loisch'
import pygame
import math
import Camera
import Vector
import PlaneObject
import SphereObject
pygame.init()
done = False#main loop on/off

#SETUP:

#Note! I used a "cracked" version or something like that of pygame. It is a cracked "later" version to let me use
#pygame with python 3.0.2. It was very tricky to setup, so I do not think you will be able to compile it.
#I use pygame to get access to (x, y) pixel to change its (r, g, b) value. That's it!
#With pixel manipulation, I went ahead and made the code.

#To make an object, simply copy and paste
"""
planeObjects.append(PlaneObject.Plane())
planeObjects[0].setReflection(False)
planeObjects[0].setPlaneNormal(0, 1, 0)
planeObjects[0].setPlanePoint(0, 0, 0)
planeObjects[0].setPointLightOrigin(lightX, lightY, lightZ)
planeObjects[0].setAmbient(1)
planeObjects[0].setDiffuse(5)
planeObjects[0].setSpecular(0)
planeObjects[0].setSpecularP(0)
planeObjects[0].setPlaneColorRed(0)
planeObjects[0].setPlaneColorGreen(10)
planeObjects[0].setPlaneColorBlue(10)
"""
#Note! Of course, since you are appending a new object, set planeObjects[0] to planeObjects[1] to set new values of the newly created object
#Do the same for extra spheres! :)
#planeObjects[0].setReflections....oh yea super cool...

#Lightx,y,z is used for all objects as the one and only point light

#Feel free to change width and height and fov and aspect ratio. It's fun to set fov to like 120 or somethin'!

#The program will render the scene(shoot rays out) and then it will blend them(my form of anti-aliasing)
#NOTE! YOU WILL WANT TO RUN THIS PROGRAM IN RUN MODE OH PLEASE FOR GOODNESS SAKE! ;) It takes forever in debug mode.

#Last note! I made a ray tracer in c++ back in the summer. I was able to go even farther than that and add some cool features.
#These featuers are...
#Specular shading, depth detection, reflections, anti-aliasing, and multiple objects.

#enjoy messing with the program. I'm sorry if you can't compile it, I could look into it...


#global variables
#1366 * 2 = 2732
#768 * 2 = 1536
#1366 * 3 = 4098
#768 * 3 = 2304
#1366 * 4 = 5464
#768 * 4 = 3072
width = 800
height = 800
fov = (3.14159265 / 3)#fov in radians (60 degree fov)
aspectRatio = width / height

#objects
clock = pygame.time.Clock()
cameraObj = Camera.Camera()
screen = pygame.display.set_mode((width, height)) #pygame.FULLSCREEN)
pxarray = pygame.PixelArray(screen)
mainRay = Vector.Vector()
sphereObjects = []
planeObjects = []
sizeOfSphereObjects = 0
sizeOfPlaneObjects = 0

lightX = 81
lightY = 27
lightZ = -80

#set initial values to setup ray tracer
cameraObj.setCamXpos(100)
cameraObj.setCamYpos(18)
cameraObj.setCamZpos(-110)
cameraObj.setCamLookAt(97, 13, -88)
cameraObj.createCamMatrix()
#cameraObj.printCamMatrix()

#set initial plane values

planeObjects.append(PlaneObject.Plane())
planeObjects[0].setReflection(False)
planeObjects[0].setPlaneNormal(0, 1, 0)
planeObjects[0].setPlanePoint(0, 0, 0)
planeObjects[0].setPointLightOrigin(lightX, lightY, lightZ)
planeObjects[0].setAmbient(1)
planeObjects[0].setDiffuse(5)
planeObjects[0].setSpecular(0)
planeObjects[0].setSpecularP(0)
planeObjects[0].setPlaneColorRed(0)
planeObjects[0].setPlaneColorGreen(10)
planeObjects[0].setPlaneColorBlue(10)


planeObjects.append(PlaneObject.Plane())
planeObjects[1].setReflection(False)
planeObjects[1].setPlaneNormal(-1, 0, 0)
planeObjects[1].setPlanePoint(130, 0, 0)
planeObjects[1].setPointLightOrigin(lightX, lightY, lightZ)
planeObjects[1].setAmbient(1)
planeObjects[1].setDiffuse(4)
planeObjects[1].setSpecular(0)
planeObjects[1].setSpecularP(0)
planeObjects[1].setPlaneColorRed(10)
planeObjects[1].setPlaneColorGreen(0)
planeObjects[1].setPlaneColorBlue(0)


sizeOfPlaneObjects = len(planeObjects)

#set initial sphere values

sphereObjects.append(SphereObject.Sphere())

sphereObjects[0].setPosition(95, 6, -75)
sphereObjects[0].setRadius(6)
sphereObjects[0].setPointLightOrigin(lightX, lightY, lightZ)
sphereObjects[0].setAmbient(1)
sphereObjects[0].setDiffuse(6)
sphereObjects[0].setSpecular(3)
sphereObjects[0].setSpecularP(110)
sphereObjects[0].setReflection(False)
sphereObjects[0].setSphereColorRed(0)
sphereObjects[0].setSphereColorGreen(20)
sphereObjects[0].setSphereColorBlue(0)


sphereObjects.append(SphereObject.Sphere())
sphereObjects[1].setPosition(90, 5, -90)
sphereObjects[1].setRadius(3)
sphereObjects[1].setPointLightOrigin(lightX, lightY, lightZ)
sphereObjects[1].setAmbient(0.5)
sphereObjects[1].setDiffuse(10)
sphereObjects[1].setSpecular(5)
sphereObjects[1].setSpecularP(50)
sphereObjects[1].setReflection(False)
sphereObjects[1].setSphereColorRed(0)
sphereObjects[1].setSphereColorGreen(0)
sphereObjects[1].setSphereColorBlue(20)

sphereObjects.append(SphereObject.Sphere())
sphereObjects[2].setPosition(113, 9, 10)
sphereObjects[2].setRadius(4)
sphereObjects[2].setPointLightOrigin(lightX, lightY, lightZ)
sphereObjects[2].setAmbient(0.5)
sphereObjects[2].setDiffuse(5)
sphereObjects[2].setSpecular(4)
sphereObjects[2].setSpecularP(0)
sphereObjects[2].setReflection(False)
sphereObjects[2].setSphereColorRed(20)
sphereObjects[2].setSphereColorGreen(20)
sphereObjects[2].setSphereColorBlue(20)

sphereObjects.append(SphereObject.Sphere())
sphereObjects[3].setPosition(75, 19, -70)
sphereObjects[3].setRadius(9)
sphereObjects[3].setPointLightOrigin(lightX, lightY, lightZ)
sphereObjects[3].setAmbient(1)
sphereObjects[3].setDiffuse(10)
sphereObjects[3].setSpecular(8)
sphereObjects[3].setSpecularP(200)
sphereObjects[3].setReflection(True)
sphereObjects[3].setSphereColorRed(10)
sphereObjects[3].setSphereColorGreen(10)
sphereObjects[3].setSphereColorBlue(10)

sizeOfSphereObjects = len(sphereObjects)

#set initial ray values
mainRay.setXorigin(cameraObj.getX())
mainRay.setYorigin(cameraObj.getY())
mainRay.setZorigin(cameraObj.getZ())

screen.fill((10, 10, 10))#draw in a clean slate

yTemp = 0
for y in range(height):
    #next for lines give info on how much is rendered
    if(y > (yTemp + 40)):
        print("Rendering scene, ", int((y / height) * 100), " percent done.")
        yTemp = y
    for x in range(width):

        ndcX = (x + 0.5) / width
        ndcY = (y + 0.5) / height

        #camAtX and Y represent the pixel at (x,y,1) in CAMERA space
        camAtX = ((2 * ndcX) - 1) * aspectRatio * math.tan(fov / 2)
        camAtY = (1 - (2 * ndcY)) * math.tan(fov / 2)

        #next three values mainRay takes as temporary
        mainRay.setX(camAtX)
        mainRay.setY(camAtY)
        mainRay.setZ(1)

        #next two lines matter, main ray is calculated and transformed to world space.
        #it now represents a ray from the virtual camera and then is normalized
        mainRay.setMainRay(cameraObj.multVectByCamMatrix(mainRay), cameraObj)
        mainRay.normalize()
        #mainRay.printMainRay()

        #draw planes
        globalLengthPlane = 100000
        testParticularPlane = 0

        for n in range(0, sizeOfPlaneObjects):
            lengthTest = planeObjects[n].calculateIntersectionsDepth(mainRay)#sort by what plane shows first (has the least distance from ray)
            #print("Plane ", n, " length", lengthTest)
            if lengthTest < globalLengthPlane:
                globalLengthPlane = lengthTest
                testParticularPlane = n#record this index for use later
        if globalLengthPlane < 100000:
            planeObjects[testParticularPlane].calculateLighting(mainRay, sphereObjects, planeObjects, testParticularPlane)

        #draw spheres
        globalLengthSphere = 100000
        testParticularSphere = 0

        for m in range(0, sizeOfSphereObjects):
            lengthTest = sphereObjects[m].calculateIntersectionsDepth(mainRay)
            #print("Sphere ", m, " length", lengthTest)
            if lengthTest < globalLengthSphere:
                globalLengthSphere = lengthTest
                testParticularSphere = m#record this index for use later
        if globalLengthSphere < 100000:
            sphereObjects[testParticularSphere].calculateLighting(mainRay, sphereObjects, planeObjects, testParticularSphere)

        #test whether sphere or plane is closest and then draw that to screen
        if globalLengthPlane < globalLengthSphere:
            pxarray[x, y] = (planeObjects[testParticularPlane].getRedFinal(), planeObjects[testParticularPlane].getGreenFinal(), planeObjects[testParticularPlane].getBlueFinal())
        else:
            pxarray[x, y] = (sphereObjects[testParticularSphere].getRedFinal(), sphereObjects[testParticularSphere].getGreenFinal(), sphereObjects[testParticularSphere].getBlueFinal())






xTemp = 0
#next for loop is for anti-aliasing (I do a form of multi sampling except not really. my own idea!)
for x in range(1, width - 1):
    #next lines give info on how much is blended
    if(x > xTemp + 40):
        print("Blending scene, ", int((x / width) * 100), " percent done.")
        xTemp = x
    for y in range(1, height - 1):
        #pixel arrangement 2
        #| 5 | 3 | 6 |
        #| 1 | 0 | 2 |
        #| 7 | 4 | 8 |

        #if you are interested in what I do here. ask. its easier to explain in words :D I know I should
        #say the stuff in comments but I'ld love to talk!

        colorTest = pygame.Color(pxarray[x, y])
        color1 = pygame.Color(pxarray[x - 1, y])
        color2 = pygame.Color(pxarray[x + 1, y])
        color3 = pygame.Color(pxarray[x, y - 1])
        color4 = pygame.Color(pxarray[x, y + 1])

        color5 = pygame.Color(pxarray[x - 1, y - 1])
        color6 = pygame.Color(pxarray[x + 1, y - 1])
        color7 = pygame.Color(pxarray[x - 1, y + 1])
        color8 = pygame.Color(pxarray[x + 1, y + 1])

        redAvg = colorTest.g
        greenAvg = colorTest.b
        blueAvg = colorTest.a

        diff = 15
        #if difference in color is greater than 15, then go ahead and smooth out the color change
        if (math.fabs(color1.g - colorTest.g) > diff):
            redAvg = (color1.g + colorTest.g) / 2

        if(math.fabs(color1.b - colorTest.b) > diff):
            greenAvg = (color1.b + colorTest.b) / 2

        if(math.fabs(color1.a - colorTest.a) > diff):
            blueAvg = (color1.a + colorTest.a) / 2

        if (math.fabs(color2.g - colorTest.g) > diff):
            redAvg = (redAvg + color2.g + colorTest.g) / 3

        if(math.fabs(color2.b - colorTest.b) > diff):
            greenAvg = (greenAvg + color2.b + colorTest.b) / 3

        if(math.fabs(color2.a - colorTest.a) > diff):
            blueAvg = (blueAvg + color2.a + colorTest.a) / 3

        if (math.fabs(color3.g - colorTest.g) > diff):
            redAvg = (redAvg + color3.g + colorTest.g) / 3

        if(math.fabs(color3.b - colorTest.b) > diff):
            greenAvg = (greenAvg + color3.b + colorTest.b) / 3

        if(math.fabs(color3.a - colorTest.a) > diff):
            blueAvg = (blueAvg + color3.a + colorTest.a) / 3

        if (math.fabs(color4.g - colorTest.g) > diff):
            redAvg = (redAvg + color4.g + colorTest.g) / 3

        if(math.fabs(color4.b - colorTest.b) > diff):
            greenAvg = (greenAvg + color4.b + colorTest.b) / 3

        if(math.fabs(color4.a - colorTest.a) > diff):
            blueAvg = (blueAvg + color4.a + colorTest.a) / 3

        if (math.fabs(color5.g - colorTest.g) > diff):
            redAvg = (redAvg + color5.g + colorTest.g) / 3

        if(math.fabs(color5.b - colorTest.b) > diff):
            greenAvg = (greenAvg + color5.b + colorTest.b) / 3

        if(math.fabs(color5.a - colorTest.a) > diff):
            blueAvg = (blueAvg + color5.a + colorTest.a) / 3

        if (math.fabs(color6.g - colorTest.g) > diff):
            redAvg = (redAvg + color6.g + colorTest.g) / 3

        if(math.fabs(color6.b - colorTest.b) > diff):
            greenAvg = (greenAvg + color6.b + colorTest.b) / 3

        if(math.fabs(color6.a - colorTest.a) > diff):
            blueAvg = (blueAvg + color6.a + colorTest.a) / 3

        if (math.fabs(color7.g - colorTest.g) > diff):
            redAvg = (redAvg + color7.g + colorTest.g) / 3

        if(math.fabs(color7.b - colorTest.b) > diff):
            greenAvg = (greenAvg + color7.b + colorTest.b) / 3

        if(math.fabs(color7.a - colorTest.a) > diff):
            blueAvg = (blueAvg + color7.a + colorTest.a) / 3

        if (math.fabs(color8.g - colorTest.g) > diff):
            redAvg = (redAvg + color8.g + colorTest.g) / 3

        if(math.fabs(color8.b - colorTest.b) > diff):
            greenAvg = (greenAvg + color8.b + colorTest.b) / 3

        if(math.fabs(color8.a - colorTest.a) > diff):
            blueAvg = (blueAvg + color8.a + colorTest.a) / 3

        pxarray[x, y] = (redAvg, greenAvg, blueAvg)

surf = pxarray.make_surface()
pygame.display.flip()
pygame.image.save(surf, "test.bmp")

'''
while(done == False):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
'''



