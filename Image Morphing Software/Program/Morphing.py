'''
List of references:
-------------------
For locating whether point lies inside triangle or not:
    https://www.youtube.com/watch?v=H9qu9Xptf-w
'''

import cv2

###########################################################

#Helper Functions
def inverseColorValueInterpolated(coordinates,image):
    #Returns interpolated value for fractional coordinates.
    x = coordinates[0]
    y = coordinates[1]
    x1 = int(x)
    y1 = int(y)
    x2 = x1+1
    y2 = y1+1

    value=[]
    numberOfChannels = len(image[y1][x1])
    for i in range(0,numberOfChannels):
        if(x==x1 and y==y1):
            interpolatedValue=image[y1][x1][i]
            value.append(int(interpolatedValue))
        elif(x==x1):
            #Interpolating wrt y
            v1= image[y1][x1][i]
            v2= image[y2][x1][i]
            interpolatedValue = (y2-y)*v1 + (y-y1)*v2
            value.append(int(interpolatedValue))
        elif(y==y1):
            #Interpolate wrt x
            v1= image[y1][x1][i]
            v2= image[y1][x2][i]
            interpolatedValue = (x2-x)*v1 + (x-x1)*v2
            value.append(int(interpolatedValue))
        else:
            #Interpolate all 4
            v1= image[y1][x1][i]
            v2= image[y1][x2][i]
            interpolatedXValueFory1 = (x2-x)*v1 + (x-x1)*v2
            v1= image[y2][x1][i]
            v2= image[y2][x2][i]
            interpolatedXValueFory2 = (x2-x)*v1 + (x-x1)*v2
            interpolatedValue = (y2-y)*interpolatedXValueFory1 + (y-y1)*interpolatedXValueFory2
            value.append(int(interpolatedValue))

    return value


def affineTransform(p0x,p0y,p1x,p1y,p2x,p2y,q0x,q0y,q1x,q1y,q2x,q2y,qx,qy):
    #Affine Transform for 2 triangles and 2 points (refer calculations)
    beta = ((qx-q0x)*(q1y-q0y)-(qy-q0y)*(q1x-q0x))/((q2x-q0x)*(q1y-q0y)-(q2y-q0y)*(q1x-q0x))
    alpha = ((qx-q0x)*(q2y-q0y)-(qy-q0y)*(q2x-q0x))/((q1x-q0x)*(q2y-q0y)-(q1y-q0y)*(q2x-q0x))
    px = p0x + alpha*(p1x-p0x) + beta*(p2x-p0x)
    py = p0y + alpha*(p1y-p0y) + beta*(p2y-p0y)
    return [px,py]

###########################################################

#Main Function of the script

def morph(n,totalFrames,x11,y11,x12,y12,x13,y13,x21,y21,x22,y22,x23,y23,image1Url,image2Url):
    #Returns morphed set of points and their values corresponing to input triangle
    img1 = cv2.imread(image1Url)
    img2 = cv2.imread(image2Url)
    size = img1.shape

    m = totalFrames - n

    x1 = (m*x11 + n*x21)/totalFrames
    y1 = (m*y11 + n*y21)/totalFrames
    x2 = (m*x12 + n*x22)/totalFrames
    y2 = (m*y12 + n*y22)/totalFrames
    x3 = (m*x13 + n*x23)/totalFrames
    y3 = (m*y13 + n*y23)/totalFrames



    Area = abs(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))/2
    setOfCoordinates=[]
    for x in range (0,size[0]):
        for y in range (0,size[1]):
            area1 = abs(x*(y2-y3)+x2*(y3-y)+x3*(y-y2))/2
            area2 = abs(x1*(y-y3)+x*(y3-y1)+x3*(y1-y))/2
            area3 = abs(x1*(y2-y)+x2*(y-y1)+x*(y1-y2))/2
            diffInArea = abs(Area-(area1+area2+area3))
            if( diffInArea < 0.0001 ):
                inverseCoordinates1 = affineTransform(x11,y11,x12,y12,x13,y13,x1,y1,x2,y2,x3,y3,x,y)
                inverseCoordinates2 = affineTransform(x21,y21,x22,y22,x23,y23,x1,y1,x2,y2,x3,y3,x,y)
                inverseVal1 = inverseColorValueInterpolated(inverseCoordinates1,img1)
                inverseVal2 = inverseColorValueInterpolated(inverseCoordinates2,img2)
                numberOfChannels = len(inverseVal1)
                inverseVal=[]
                for i in range(0, numberOfChannels):
                    val = int((m*inverseVal1[i] + n*inverseVal2[i])/(totalFrames))
                    inverseVal.append(val)
                setOfCoordinates.append([x,y,inverseVal])
    return setOfCoordinates
