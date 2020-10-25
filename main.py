# imports
from xml.dom import minidom
from tkinter import Tk
from tkinter.filedialog import askopenfile
import re

import os
import sys

import tkinter as tk

import csv
import numpy as np

import math

import matplotlib.pyplot as plt

import pygame
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, parse_path

linesOnlySegmentsArray = []
linesOnlyPointsArray = []

#identify each individual path in the svg file
def parseSVG(svg_file):
    doc = minidom.parse(svg_file)
    path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]

    fileNameCounter = 0

    for k in range(len(path_strings)):
        temporaryPathArray = path_strings[k].split('z')

        for g in range(len(temporaryPathArray)):
            if(g < (len(temporaryPathArray) - 1)):
                segmentedPathArray = []
                segmentedPathArray.append(temporaryPathArray[g])
                f = open("path" + str(fileNameCounter) + ".txt", "w")
                f.write(segmentedPathArray[0])
                f.close()
                fileNameCounter = fileNameCounter + 1
    return fileNameCounter

#import the svg file
def importSVG():
    Tk().withdraw()
    svg_file = askopenfile()

    return svg_file

def drawSVG(svgPaths):
    for x in range(len(svgPaths)):
        print(svgPaths[x])

    path = parse_path(svgPaths[0])

    # svg.path point method returns a complex number p, p.real and p.imag can pull the x, and y
    # # on 0.0 to 1.0 along path, represent percent of distance along path
    n = 999  # number of line segments to draw

    # pts = []
    # for i in range(0,n+1):
    #     f = i/n  # will go from 0.0 to 1.0
    #     complex_point = path.point(f)  # path.point(t) returns point at 0.0 <= f <= 1.0
    #     pts.append((complex_point.real, complex_point.imag))

    # list comprehension version or loop above
    pts = [(p.real, p.imag) for p in (path.point(i / n) for i in range(0, n + 1))]

    pygame.init()  # init pygame
    infoObject = pygame.display.Info()
    surface = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))  # get surface to draw on
    surface.fill(pygame.Color('white'))  # set background to white

    pygame.draw.aalines(surface, pygame.Color('black'), False, pts)  # False is no closing
    pygame.display.update()  # copy surface to display

    while True:  # loop to wait till window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

#This function will identify curves within each particular line segment and then break them up into smaller line segments
def breakUpCurves(lineSegment):

    #why do I not include m/M here? Need to figure that out...
    chars = set('sSqQtTaA')

    for k in range(lineSegment):
        individualSegmentCommandCollection = []
        individualSegmentCommand = []

        f = open("path" + str(k) + ".txt", "r")

        lineSegment = f.readline()
        f.close()

        listOfSegments = re.split("M|m|L|l|H|h|V|v|C|c|S|s|Q|q|T|t|A|a|Z|z", lineSegment)
        svgCommands = re.findall("M|m|L|l|H|h|V|v|C|c|S|s|Q|q|T|t|A|a|Z|z", lineSegment)

        for x in range(len(svgCommands)):
            individualSegmentCommand.append((svgCommands[x] + listOfSegments[x + 1]).strip())
        individualSegmentCommandCollection.append(individualSegmentCommand)


        #go through each instruction in a particular segment and identify curves/arcs
        for b in range(len(individualSegmentCommandCollection[0])):
            if any((c in chars) for c in individualSegmentCommandCollection[0][b][0]):
                #if it has entered this part then it is a segment that is not recognized by the library that I'm using so I have to simplify
                    #it into a bezier curve

                #passing the current curve(simple syntax) and the previous bezier curve(needed to transform from simple to bezier)
                simpleInBezier = simpleToNormalBezierCurve(individualSegmentCommandCollection[0][b], individualSegmentCommandCollection[0][b-1])

                #conceivably this is the next line...
                individualSegmentCommandCollection[0][b] = simpleInBezier

                #currentPath.append(individualSegmentCommandCollection[0][b])


        writeString = ''.join(individualSegmentCommandCollection[0])

        f = open("onlyCurves" + str(k) + ".txt", "w")

        f.write(writeString)

        f.close()



            #print(individualSegmentCommandCollection[0][b])




        #check to see if it is a curve(look for curve instructions)
        #  if curve,
        # get length of curve, choose minimum number of segments to be divided into
        # iterate along path and mark x and y coordinates.
        # create line segments from marked x and y coordinates


# def curvesToLines(curve, currentPath):
#
#     #Don't include s here because the library that I'm using doesn't recognize s
#     chars = set('mMcCqQtTaA')
#
#
#     #need to change the s commands into c commands(look online)
#     #print(curve)
#     # test = parse_path(curve)
#
#
#
#
#     if any((c in chars) for c in curve):
#         #add this to the current calculation for the current X and Y
#         currentPath.append(parse_path(curve))
#
#
#
#     elif (('s' in curve) or ('S' in curve)):
#         #use the developed path to get the current X and Y for the function
#         print(currentPath.point(1.0))
#         bezierCurve = simpleToNormalBezierCurve(lastSegmentInstruction, curve, currentX, currentY)
#
#         currentPath.append(parse_path(bezierCurve))
#
#     lastSegmentInstruction = curve
#     return currentPath[-1]
#
#
#
#
#
#
#
#     # #get length of curve
#     # lengthOfCurve = curveSegment.length()
#     # print(lengthOfCurve)
#     #
#     # lineSegment = lengthOfCurve
#     #
#     # return lineSegment

def simpleToNormalBezierCurve(simpleCurve, bezierCurve):
    # bezierCurveArray = re.split("(c\A|,\d|-\d)", bezierCurve)
    # simpleCurveArray = re.split(r"(s\A|-\d+.+\d|,)", simpleCurve)

    chars = set('qQtTaA')

    if any((c in chars) for c in simpleCurve):
        if any((c in chars) for c in bezierCurve):
            print("The program does not current support Q, T, or A commands.")
            sys.exit()

    bezierCurveArrayFloats = re.findall(r"[-+]?\d*\.\d+|\d+", bezierCurve)
    simpleCurveArrayFloats = re.findall(r"[-+]?\d*\.\d+|\d+", simpleCurve)

    newBezierCurveArray = []
    newSimpleCurveArray = []

    newBezierCurveArray = ['c', bezierCurveArrayFloats[0], bezierCurveArrayFloats[1], bezierCurveArrayFloats[2], bezierCurveArrayFloats[3], bezierCurveArrayFloats[4], bezierCurveArrayFloats[5]]
    newSimpleCurveArray = ['s', simpleCurveArrayFloats[0], simpleCurveArrayFloats[1], simpleCurveArrayFloats[2], simpleCurveArrayFloats[3]]


    simpleToCubic = []
    # skip = False

    # for k in range(len(bezierCurveArray)):
    #     if (skip == True):
    #         skip = False
    #         continue
    #     if (bezierCurveArray[k] == "-"):
    #         newBezierCurveArray.append(bezierCurveArray[k] + bezierCurveArray[k+1])
    #         skip = True
    #     elif (bezierCurveArray[k] != ","):
    #         newBezierCurveArray.append(bezierCurveArray[k])
    #
    #
    #
    # for k in range(len(simpleCurveArray)):
    #     if (skip == True):
    #         skip = False
    #         continue
    #     if (bezierCurveArray[k] == "-"):
    #         newSimpleCurveArray.append(simpleCurveArray[k] + simpleCurveArray[k+1])
    #         skip = True
    #     elif (bezierCurveArray[k] != ","):
    #         newSimpleCurveArray.append(simpleCurveArray[k])


    #identify the key parameters for each curve and label them

    #bezier curve
    cubicX2 = newBezierCurveArray[3]
    cubicY2 = newBezierCurveArray[4]
    cubicX = newBezierCurveArray[5]
    cubicY = newBezierCurveArray[6]

    #calculate mirrored 1st control point
    simpleX1 = (2*float(cubicX) - float(cubicX2))
    simpleY1 = ((2*float(cubicY)) - float(cubicY2))

    #simple curve
    simpleX2 = newSimpleCurveArray[1]
    simpleY2 = newSimpleCurveArray[2]
    simpleX = newSimpleCurveArray[3]
    simpleY = newSimpleCurveArray[4]

    #create list for complex curve from simple curve
    simpleToCubic.append(str("c"))
    simpleToCubic.append(str(simpleX1))
    simpleToCubic.append(str(simpleY1))
    simpleToCubic.append(str(simpleX2))
    simpleToCubic.append(str(simpleY2))
    simpleToCubic.append(str(simpleX))
    simpleToCubic.append(str(simpleY))

    #add commas if there is no '-' sign b/w numbers
    for g in range(len(simpleToCubic)-1):
        if "-" not in simpleToCubic[g+1]:
            simpleToCubic[g+1] = (',' + simpleToCubic[g+1])

    simpleToCubicString = ''.join(simpleToCubic)

    return simpleToCubicString

def createPathObject(numberOfFiles):
    k = 0
    while (k < numberOfFiles):
        parsedPath = Path()
        individualSegmentCommand = []
        individualSegmentCollection = []

        f = open("onlyCurves" + str(k) + ".txt", "r")

        pathToFormString = str(f.readline())

        f.close()

        listOfSegments = re.split("M|m|L|l|H|h|V|v|C|c|S|s|Q|q|T|t|A|a|Z|z", pathToFormString)
        svgCommands = re.findall("M|m|L|l|H|h|V|v|C|c|S|s|Q|q|T|t|A|a|Z|z", pathToFormString)

        for x in range(len(svgCommands)):
            individualSegmentCommand.append((svgCommands[x] + listOfSegments[x + 1]).strip())
        individualSegmentCollection.append(individualSegmentCommand)

        # for y in range(len(individualSegmentCollection[0])):
        #     # parsedPath.append(individualSegmentCollection[0][y])
        #     parsedPath = Path(individualSegmentCollection[0])

        f = open("onlyCurves" + str(k) + ".txt", "w")

        f.write(str(individualSegmentCollection[0]))

        f.close()

        k = k + 1

def parsePathObject(numberOfFiles):
    k = 0

    while (k < numberOfFiles):
        linesOnlySegment = []
        f = open("onlyCurves" + str(k) + ".txt", "r")

        pathToFormString = f.readline()

        f.close()

        currentPathObject = parse_path(pathToFormString)

        #I'm assuming that the first command I will always see is the Move command(I need to make this more robust/dynamic)
        for l in range(len(currentPathObject)-1):
            # print(currentPathObject[l])
            linesOnlySegment.append(breakIntoLines(currentPathObject[l+1]))

        linesOnlySegmentsArray.append(linesOnlySegment)

        #seeing what each part of my array holds so that I can use that information to extract points
        # print(linesOnlySegmentsArray)
        # print(linesOnlySegmentsArray[0])
        # if (k == 1):
        #     print(linesOnlySegmentsArray[1][0])


        # print(len(linesOnlySegment))
        f = open("onlyLines" + str(k) + ".txt", "w")

        f.write(str(linesOnlySegment))

        f.close()


        k = k + 1

def breakIntoLines(segment):

    #I may need to check if it is a move command and do nothing...

    #for now I am just going to hardcode this but it is possible that I will make it dynamic in the future
    numberOfSegments = 1
    baseSegmentStep = 1 / (numberOfSegments)
    segmentStep = 1 / (numberOfSegments)
    k = 0
    linesOnlySegment = Path()

    initialPoint = segment.point(0.0)

    while (k <= numberOfSegments):
        currentPoint = segment.point(segmentStep)
        if (k == 0):
            returnedLine = createLineSegment(currentPoint, initialPoint)
        else:
            returnedLine = createLineSegment(currentPoint, lastPoint)

        linesOnlySegment.append(returnedLine)
        lastPoint = segment.point(segmentStep)

        k = k + 1
        segmentStep = baseSegmentStep * k

    return linesOnlySegment

def createLineSegment(currentPoint, previousPoint):
    lineSegment = Line(previousPoint, currentPoint)
    # print(lineSegment)
    return lineSegment


def extractPoints(numberOfFiles):

    k = 0
    for k in range(numberOfFiles):
        pointsArrayStartX = []
        pointsArrayStartY = []
        # pointsArrayEndX = []
        # pointsArrayEndY = []

        for l in range(len(linesOnlySegmentsArray[k])):
            for m in range(len(linesOnlySegmentsArray[k][l])):
                pointsArrayStartX.append(float(linesOnlySegmentsArray[k][l][m].point(0.0).real))
                pointsArrayStartY.append(float(linesOnlySegmentsArray[k][l][m].point(0.0).imag))
                # pointsArrayEnd.append(linesOnlySegmentsArray[k][l][m].point(1.0))

        #writes the X and Y to the same file(in different rows)
        with open("Points" + str(k) + ".txt", "w", newline='') as myfile:
            # wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            wr.writerow(pointsArrayStartX)
            wr.writerow(pointsArrayStartY)

        #below writes the X and Y to two separate files
        # with open("XPoints" + str(k) + ".txt", "w", newline='') as myfile:
        #     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        #     wr.writerow(pointsArrayStartX)
        #
        # with open("YPoints" + str(k) + ".txt", "w", newline='') as myfile:
        #     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        #     wr.writerow(pointsArrayStartY)


        # f = open("XPoints" + str(k) + ".txt", "w")
        # f.write(str(pointsArrayStartX))
        # f.close()
        #
        # f = open("YPoints" + str(k) + ".txt", "w")
        # f.write(str(pointsArrayStartY))
        # f.close()


        k = k + 1


def graphPoints(numberOfFiles):

    w = 0
    while w < numberOfFiles:
        x = []
        y = []

        # x, y = np.loadtxt('Points0.txt', delimiter=',', unpack=True)
        pointHolder = np.loadtxt('Points' + str(w) + '.txt', delimiter=',', unpack=True)
        # testVar = np.loadtxt('Points4.txt', delimiter=',', unpack=True)

        z = 0
        while z < len(pointHolder):
            x.append(pointHolder[z][0])
            y.append(pointHolder[z][1])
            z = z + 1


        # with open("XPoints0.txt", "r") as csvfile:
        #     plots = csv.reader(csvfile, delimiter=",")
        #     for row in plots:
        #         x.append(tuple(row))
        #
        # with open("YPoints0.txt", "r") as csvfile:
        #     plots = csv.reader(csvfile, delimiter=",")
        #     for row in plots:
        #         y.append(tuple(row))


        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

        plt.close()

        w = w + 1


    return 777
    
def processDataPoints(numberOfFiles):
    lastAngle = 0

    w = 0
    while w < numberOfFiles:
        pointHolder = np.loadtxt('Points' + str(w) + '.txt', delimiter=',', unpack=True)

        pathHistoryX = []
        pathHistoryY = []
        print(w)
        print("searchValue")

        z = 0
        while z < len(pointHolder):
            pathHistoryX.append(pointHolder[z][0])
            pathHistoryY.append(pointHolder[z][1])

            currentX = pointHolder[z][0]
            currentY = pointHolder[z][1]

            if (z >= (len(pointHolder) - 1)):
                nextX = pointHolder[z][0]
                nextY = pointHolder[z][1]
            else:
                nextX = pointHolder[z + 1][0]
                nextY = pointHolder[z + 1][1]

            lineSegmentLength = getLineSegmentLength(currentX, currentY, nextX, nextY)
            angle = getDifferentialAngle(currentX, currentY, nextX, nextY)

            # print(currentX)
            # print(currentY)
            print(lineSegmentLength)
            print(angle - lastAngle)
            # print(currentX)
            # print(currentY)
            # print(z)
            # print(len(pointHolder - 1))
            print()

            lastAngle = angle

            z = z + 1
            if (z == 6524):
                print(z)
        w = w + 1

    return 777

def getLineSegmentLength(currentX, currentY, nextX, nextY):
    yLength = nextY - currentY
    xLength = nextX - currentX

    lineSegmentLength = math.sqrt((yLength ** 2) + (xLength ** 2))

    return lineSegmentLength

def getDifferentialAngle(currentX, currentY, nextX, nextY):
    yLength = nextY - currentY
    xLength = nextX - currentX

    differentialAngle = math.degrees(math.atan(yLength/xLength))

    return differentialAngle

def test():


    return 777


def main():

    # test()
    #below is the data parsing part of my program
    svg_file = importSVG()
    numberOfFiles = parseSVG(svg_file)

    breakUpCurves(numberOfFiles)
    createPathObject(numberOfFiles)

    parsePathObject(numberOfFiles)

    extractPoints(numberOfFiles)

    #the below code processes all of the data and outputs the file that is read through by the machine
    processDataPoints(numberOfFiles)

    graphPoints(numberOfFiles)

    #I need to start processing the x and y points that I have..
    # 1) I need to find out the "inside" of the letter(which way the flange is supposed to bend)
    # 2) I need to create a function to get the slope of each line segment
    # 3) I need to create a "language" to describe to my machine what to do


    # After the above is done then I can start ordering the parts

    # I can finish it up by creating a GUI

    #below is the user interface part of my program
    # #I'm going to build the GUI later but I need to use a visual GUI builder(look on the internet)
    # createWindow()




    # for x in range(len(pathHolder)):
    #     curvesToLines(pathHolder[x])

    # #need to use this to start the next part(turning curves into line segments) -- using svg.path library
    # print(pathHolder[0][1])
    # testPath = parse_path(pathHolder[0][0] + pathHolder[0][1] + pathHolder[0][2] + pathHolder[0][3])
    # print(testPath.length())
    #
    # print(testPath)
    #
    # #curvesToLines(pathHolder[0][0])


#    for path in svgPaths:
#        pathObjects.append(breakUpCurves(path))


#   This section will draw a particular line segment of the svg file generated from svgPaths()
#    drawSVG(svgPaths)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()