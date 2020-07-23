'''
List of references:
-------------------
Bowyer Watson Algorithm Pseudocode:
    https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
'''

###########################################################

#Helper functions

def triangleHasCornerPoint(triangle,x1,y1,x2,y2,x3,y3,x4,y4):

    if(triangle[0]==x1 and triangle[1]==y1):
        return True

    elif(triangle[2]==x1 and triangle[3]==y1):
        return True

    elif(triangle[4]==x1 and triangle[5]==y1):
        return True

    elif(triangle[0]==x2 and triangle[1]==y2):
        return True

    elif(triangle[2]==x2 and triangle[3]==y2):
        return True

    elif(triangle[4]==x2 and triangle[5]==y2):
        return True

    elif(triangle[0]==x3 and triangle[1]==y3):
        return True

    elif(triangle[2]==x3 and triangle[3]==y3):
        return True

    elif(triangle[4]==x3 and triangle[5]==y3):
        return True

    elif(triangle[0]==x4 and triangle[1]==y4):
        return True

    elif(triangle[2]==x4 and triangle[3]==y4):
        return True

    elif(triangle[4]==x4 and triangle[5]==y4):
        return True

    else:
        return False



def findCircumcenter(triangle):
    x1 = triangle[0]
    y1 = triangle[1]
    x2 = triangle[2]
    y2 = triangle[3]
    x3 = triangle[4]
    y3 = triangle[5]
    a1 = float(2*x2 - 2*x1)
    b1 = float(2*y2 - 2*y1)
    c1 = float(x1*x1 + y1*y1 - x2*x2 - y2*y2)
    a2 = float(2*x3 - 2*x1)
    b2 = float(2*y3 - 2*y1)
    c2 = float(x1*x1 + y1*y1 - x3*x3 - y3*y3)
    x = (b1*c2 - b2*c1)/(a1*b2 - a2*b1)
    y = (a2*c1 - a1*c2)/(a1*b2 - a2*b1)
    return [x,y]

def sortEdge(x1,y1,x2,y2): #Sort edge by x. If x equal, sort by y
    if(x1 < x2):
        return [x1,y1,x2,y2]
    elif(x2 < x1):
        return [x2,y2,x1,y1]
    elif(y1 < y2):
        return [x1,y1,x2,y2]
    else:
        return [x2,y2,x1,y1]

def isCollinear(triangle):
    x1 = triangle[0]
    y1 = triangle[1]
    x2 = triangle[2]
    y2 = triangle[3]
    x3 = triangle[4]
    y3 = triangle[5]

    if((x3-x1)*(y2-y1)==(x2-x1)*(y3-y1)):
        return True
    else:
        return False

###########################################################
#Main function of script

def findDelaunayTriangles(points,height,width):
    global findCircumcenter
    global sortEdge
    global isCollinear
    global triangleHasCornerPoint
    #setOfTriangles = [[0,0,width-1,height-1,0,height-1], [0,0,width-1,height-1,width-1,0]]
    setOfTriangles = [[100000,100000,-100000,-100000,-100000,100000], [100000,100000,-100000,-100000,100000,-100000]]


    for p in points:
        trianglesToBeDeleted=[]
        indicesOfTrianglesToBeDeleted=[]

        triangleIndex=-1
        for triangle in setOfTriangles:
            triangleIndex+=1;
            circumcenter = findCircumcenter(triangle)
            circumradiusSquare = (circumcenter[0]-triangle[0])*(circumcenter[0]-triangle[0]) + (circumcenter[1]-triangle[1])*(circumcenter[1]-triangle[1])
            distPtToCircumcenterSquare = (circumcenter[0]-p[0])*(circumcenter[0]-p[0]) + (circumcenter[1]-p[1])*(circumcenter[1]-p[1])
            if (distPtToCircumcenterSquare < circumradiusSquare):
                trianglesToBeDeleted.append(triangle)
                indicesOfTrianglesToBeDeleted.append(triangleIndex)

        for i in range(len(trianglesToBeDeleted)):
            triangle = trianglesToBeDeleted[i]
            edge1 = sortEdge(triangle[0],triangle[1],triangle[2],triangle[3])
            edge2 = sortEdge(triangle[2],triangle[3],triangle[4],triangle[5])
            edge3 = sortEdge(triangle[4],triangle[5],triangle[0],triangle[1])
            trianglesToBeDeleted[i] = [edge1,edge2,edge3]

        polygon = []

        for triangle1 in trianglesToBeDeleted:
            for edge in range(3):
                edgeIsUnique = True
                for triangle2 in trianglesToBeDeleted:
                    if (triangle1 != triangle2):
                        if(triangle1[edge]==triangle2[0] or triangle1[edge]==triangle2[1] or triangle1[edge]==triangle2[2]):
                            edgeIsUnique = False

                if(edgeIsUnique):
                    uniqueEdge = triangle1[edge]
                    setOfTriangles.append([uniqueEdge[0],uniqueEdge[1],uniqueEdge[2],uniqueEdge[3],p[0],p[1]])


        indicesOfTrianglesToBeDeleted = reversed(indicesOfTrianglesToBeDeleted)
        for i in indicesOfTrianglesToBeDeleted:
            setOfTriangles.pop(i)

        #Remove collinear triangles
        collinearTriangles=[]
        for i in range(len(setOfTriangles)):
            if(isCollinear(setOfTriangles[i])):
                collinearTriangles.append(i)


        collinearTriangles = reversed(collinearTriangles)
        for i in collinearTriangles:
            setOfTriangles.pop(i)

    trianglesFormedWithCornerPoints=[]
    for i in range(len(setOfTriangles)):
        triangle = setOfTriangles[i]
        if(triangleHasCornerPoint(triangle,100000,100000,-100000,100000,-100000,-100000,100000,-100000)):
            trianglesFormedWithCornerPoints.append(i)

    trianglesFormedWithCornerPoints = reversed(trianglesFormedWithCornerPoints)
    for i in trianglesFormedWithCornerPoints:
        setOfTriangles.pop(i)

    return setOfTriangles
