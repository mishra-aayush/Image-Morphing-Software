'''
List of references:
-------------------
For fixing bug in program:
    https://stackoverflow.com/questions/60710743/tkinter-passing-integer-by-value-intead-of-reference

For creating GUI:
    https://www.youtube.com/watch?v=YXPyB4XeYLA

For scrollbar:
    https://www.youtube.com/watch?v=XkCbinbgbdw

For removing border of images(in GUI)
    https://stackoverflow.com/questions/43880224/python-tkinter-how-to-remove-the-border-around-a-frame

For creating scrollbar
    https://blog.tecladocode.com/tkinter-scrollable-frames/
    https://stackoverflow.com/questions/16820520/tkinter-canvas-create-window

For generating video from opencv:
    https://medium.com/@enriqueav/how-to-create-video-animations-using-python-and-opencv-881b18e41397
'''
###########################################################

#Import library scripts
try:
    import cv2 as cv
    import re
    import tkinter as tk
    from PIL import Image, ImageTk
    from functools import partial
except:

    print('\nError including libraries. Please download the following python libraries:\n')
    print('1.opencv:    for processing image dimensions and creating video. We didn\'t use the ffmpeg command')
    print('2.re:        for computing regular expressions')
    print('3.tkinter:   for creating the GUI')
    print('4.functools: for passing parameters in tkinter')
    print('5.PIL:       for displaying images in GUI. tkinter has poor image support. It is also called as Pillow library')
    print()
    exit(0)
###########################################################

#importing custom python scripts
import Delaunay as DT
import Morphing

###########################################################
#Creating the main GUI Window
mainGuiWindow = tk.Tk()
mainGuiWindow.title("MPA Project for 20 Marks")
mainGuiWindow.config(background="#FFFFAA")
mainGuiWindow.columnconfigure(0,weight=1)
mainGuiWindow.rowconfigure(0,weight=1)
###########################################################

#Declare global variables
defaultColoursForNewPoints="00FF00"
TableOfPoints=[]
radiusOfPoints = 2
lineThickness = 2
InitialCheckBoxState=False
totalFrames = 5
showDelaunayTriangles = tk.BooleanVar()
showDelaunayTriangles.set(False)
url1 = 'image1.jpg'
url2 = 'image2.jpg'
morphInExecution=False


try:
    if(cv.imread(url1).shape==cv.imread(url2).shape):
        imageSize=cv.imread(url1).shape
    else:
        print('\nError: The 2 images "image1.jpg" and "image2.jpg" are of different sizes\n')
        exit(0)
except:
    print('\nError loading "image1.jpg" and "image2.jpg"\n')
    exit(0)
###########################################################
#Defining all functions
def onToggleDelaunayTriangles(event):
    global showDelaunayTriangles
    global refreshCanvas1
    global refreshCanvas2
    showDelaunayTriangles.set(not(showDelaunayTriangles.get()))
    refreshCanvas1()
    refreshCanvas2()

def changeNumberOfVideoFrames():
    global numberOfVideoFramesInput
    global totalFrames
    global submitNumberOfVideoFrames
    global statusBar
    global mainGuiWindow
    global morphInExecution
    if(morphInExecution):
        statusBar.config(text="Status Bar: Cannot alter number of frames while morph is in progress.")
        mainGuiWindow.update()
        return
    inputValue = numberOfVideoFramesInput.get()
    try:
        parsedValue = int(inputValue)
    except:
        numberOfVideoFramesInput.delete(0,tk.END)
        numberOfVideoFramesInput.insert(0,totalFrames)
        statusBar.config(text="Status Bar: Invalid input. Number of frames should be an integer")
        mainGuiWindow.update()
        return
    if(parsedValue>0):
        totalFrames = parsedValue
        statusBar.config(text="Status Bar: Output will now have "+str(totalFrames)+" frames")
        mainGuiWindow.update()
    else:
        numberOfVideoFramesInput.delete(0,tk.END)
        numberOfVideoFramesInput.insert(0,totalFrames)
        statusBar.config(text="Status Bar: Invalid input. Number of frames should be greater than 0")
        mainGuiWindow.update()

def onFocusAwayFromNumberOfVideoFramesInput(event):
    global numberOfVideoFramesInput
    global totalFrames
    numberOfVideoFramesInput.delete(0,tk.END)
    numberOfVideoFramesInput.insert(0,totalFrames)

def changeDefaultColorForPoints():
    global defaultColorForPointsInput
    global defaultColoursForNewPoints
    global submitDefaultColorForPoints
    global statusBar
    global mainGuiWindow
    global refreshCanvas1
    global refreshCanvas2
    global statusBar
    global mainGuiWindow
    global morphInExecution
    if(morphInExecution):
        statusBar.config(text="Status Bar: Please wait until morph is completed until changing color.")
        mainGuiWindow.update()
        return

    inputValue = defaultColorForPointsInput.get()
    validHexValues = '^[0-9a-fA-F]{6}$'
    if(re.match(validHexValues,inputValue)):
        defaultColoursForNewPoints = inputValue
        defaultColorForPointsInput.config(background='#'+defaultColoursForNewPoints)
        submitDefaultColorForPoints.config(background='#'+defaultColoursForNewPoints)
        statusBar.config(text="Status Bar")
        mainGuiWindow.update()
        refreshCanvas1()
        refreshCanvas2()
    else:
        defaultColorForPointsInput.delete(0,tk.END)
        defaultColorForPointsInput.insert(0,defaultColoursForNewPoints)
        statusBar.config(text="Status Bar: Invalid Hex code. Enter a valid hex code (without the # sign)")
        mainGuiWindow.update()

def onFocusAwayFromDefaultColorForPointsInput(event):
    global defaultColorForPointsInput
    global defaultColoursForNewPoints
    defaultColorForPointsInput.delete(0,tk.END)
    defaultColorForPointsInput.insert(0,defaultColoursForNewPoints)

def refreshTable():
    global TableContainer
    global TableOfPoints

    TableContainer.destroy()
    TableContainer = tk.Frame(scrollable_frame,background="#FFFFAA")
    TableContainer.grid(row=5,column=0)
    if (len(TableOfPoints)==0):
        return
    tk.Label(TableContainer,text="Sl. No",padx=5,borderwidth=1, relief='solid').grid(row=0,column=0)
    tk.Label(TableContainer,text="Hex Color Code",padx=5,borderwidth=1, relief='solid').grid(row=0,column=1)
    tk.Label(TableContainer,text="Coordinates of Image 1",padx=5,borderwidth=1, relief='solid').grid(row=0,column=2)
    tk.Label(TableContainer,text="Coordinates of Image 2",padx=5,borderwidth=1, relief='solid').grid(row=0,column=3)
    tk.Label(TableContainer,text="",background="#FFFFAA").grid(row=0,column=4)

    numberOfEntries = 0
    for entry in TableOfPoints:
        numberOfEntries += 1
        tk.Label(TableContainer,text=numberOfEntries,background="#FFFFFF",borderwidth=1, relief='solid').grid(row=numberOfEntries,column=0,sticky='nswe')
        tk.Label(TableContainer,text=entry[0],background="#FFFFFF",borderwidth=1, relief='solid').grid(row=numberOfEntries,column=1,sticky='nswe')
        tk.Label(TableContainer,text="(" + str(entry[1][0])+ " , " +str(entry[1][1])+ ")",background="#FFFFFF",borderwidth=1, relief='solid').grid(row=numberOfEntries,column=2,sticky='nswe')
        tk.Label(TableContainer,text="(" + str(entry[2][0])+ " , " +str(entry[2][1])+ ")",background="#FFFFFF",borderwidth=1, relief='solid').grid(row=numberOfEntries,column=3,sticky='nswe')
        tk.Button(TableContainer, text="REMOVE",command=partial(deleteTableEntry, numberOfEntries),background="#FF0000").grid(row=numberOfEntries,column=4,sticky='nswe')

def deleteTableEntry(rowNumber):
    global TableOfPoints
    global morphInExecution
    global statusBar
    global mainGuiWindow
    if(morphInExecution):
        statusBar.config(text="Status Bar: Cannot remove entries. Morph is in execution")
        mainGuiWindow.update()
        return
    TableOfPoints.pop(rowNumber-1)
    refreshTable()
    refreshCanvas1()
    refreshCanvas2()

def onClickOfImage1(event):
    global activeImage
    global coordinates
    global canvas1
    global radiusOfPoints
    global TableOfPoints
    global imageSize
    global morphInExecution
    global statusBar
    global mainGuiWindow
    if(morphInExecution):
        statusBar.config(text="Status Bar: Cannot add entries. Morph is in execution")
        mainGuiWindow.update()
        return

    for entry in TableOfPoints:
        if((entry[1][0]==event.x)and(entry[1][1]==event.y)):
            statusBar.config(text="Status Bar: Nice Try. You cannot select the same point twice")
            mainGuiWindow.update()
            return
    if(activeImage==1):
        activeImage=2
        coordinates[0][0]=event.x
        coordinates[0][1]=event.y
        refreshCanvas1()
        statusBar.config(text="Status Bar")
        mainGuiWindow.update()
    else:
        statusBar.config(text="Status Bar: Point already selected in Image 1. Select its corresponding point in Image 2")
        mainGuiWindow.update()

def refreshCanvas1():
    global defaultColoursForNewPoints
    global url1
    global activeImage
    global image1
    global image1size
    global canvas1
    global radiusOfPoints
    global onClickOfImage1
    global TableOfPoints
    global showDelaunayTriangles
    canvas1.destroy()
    canvas1=tk.Canvas(ImageFramesContainer,height=image1size[0],width=image1size[1],borderwidth=0,highlightthickness=0)
    canvas1.create_image(1,1,image=image1,anchor='nw')
    canvas1.grid(row=0,column=0)
    canvas1.bind("<Button-1>",onClickOfImage1)
    for entry in TableOfPoints:
        canvas1.create_oval(entry[1][0]-radiusOfPoints,entry[1][1]-radiusOfPoints,entry[1][0]+radiusOfPoints,entry[1][1]+radiusOfPoints,fill="#"+entry[0])
    if(activeImage==2):
        canvas1.create_oval(coordinates[0][0]-radiusOfPoints,coordinates[0][1]-radiusOfPoints,coordinates[0][0]+radiusOfPoints,coordinates[0][1]+radiusOfPoints,fill="#"+defaultColoursForNewPoints)

    if(showDelaunayTriangles.get()):
        setOfPointsInImage1=[]
        for entry in TableOfPoints:
            setOfPointsInImage1.append(entry[1])
        imageSize = cv.imread(url1).shape
        triangleList = DT.findDelaunayTriangles(setOfPointsInImage1,imageSize[0],imageSize[1])
        for entry in triangleList:
            p1=[int(entry[0]),int(entry[1])]
            p2=[int(entry[2]),int(entry[3])]
            p3=[int(entry[4]),int(entry[5])]
            canvas1.create_line(p1[0],p1[1],p2[0],p2[1],width=lineThickness)
            canvas1.create_line(p1[0],p1[1],p3[0],p3[1],width=lineThickness)
            canvas1.create_line(p2[0],p2[1],p3[0],p3[1],width=lineThickness)

def onClickOfImage2(event):
    global activeImage
    global coordinates
    global TableOfPoints
    global imageSize
    global morphInExecution
    global statusBar
    global mainGuiWindow
    if(morphInExecution):
        statusBar.config(text="Status Bar: Cannot add entries. Morph is in execution")
        mainGuiWindow.update()
        return

    for entry in TableOfPoints:
        if((entry[1][0]==event.x)and(entry[1][1]==event.y)):
            statusBar.config(text="Status Bar: Nice Try. You cannot select the same point twice")
            mainGuiWindow.update()
            return
    if(activeImage==2):
        activeImage=1
        coordinates[1][0]=event.x
        coordinates[1][1]=event.y
        TableOfPoints.append([defaultColoursForNewPoints,[coordinates[0][0],coordinates[0][1]],[coordinates[1][0],coordinates[1][1]]])
        refreshTable()
        refreshCanvas2()
        statusBar.config(text="Status Bar")
        mainGuiWindow.update()
    else:
        statusBar.config(text="Status Bar: First select the point in image 1")
        mainGuiWindow.update()

def refreshCanvas2():
    global refreshCanvas1
    global defaultColoursForNewPoints
    global image2
    global image2size
    global canvas2
    global onClickOfImage2
    global showDelaunayTriangles
    global url2
    refreshCanvas1()
    canvas2.destroy()
    canvas2=tk.Canvas(ImageFramesContainer,height=image1size[0],width=image1size[1],borderwidth=0,highlightthickness=0)
    canvas2.create_image(1,1,image=image2,anchor='nw')
    canvas2.grid(row=0,column=1)
    canvas2.bind("<Button-1>",onClickOfImage2)
    for entry in TableOfPoints:
        canvas2.create_oval(entry[2][0]-radiusOfPoints,entry[2][1]-radiusOfPoints,entry[2][0]+radiusOfPoints,entry[2][1]+radiusOfPoints,fill="#"+entry[0])

    if(showDelaunayTriangles.get()):
        setOfPointsInImage2=[]
        for entry in TableOfPoints:
            setOfPointsInImage2.append(entry[2])
        imageSize = cv.imread(url2).shape
        triangleList = DT.findDelaunayTriangles(setOfPointsInImage2,imageSize[0],imageSize[1])
        for entry in triangleList:
            p1=[int(entry[0]),int(entry[1])]
            p2=[int(entry[2]),int(entry[3])]
            p3=[int(entry[4]),int(entry[5])]
            canvas2.create_line(p1[0],p1[1],p2[0],p2[1],width=lineThickness)
            canvas2.create_line(p1[0],p1[1],p3[0],p3[1],width=lineThickness)
            canvas2.create_line(p2[0],p2[1],p3[0],p3[1],width=lineThickness)

def generateCorrespondingTriangles():
    global TableOfPoints
    global url1
    global url2
    setOfPointsInImage1=[]
    for entry in TableOfPoints:
        setOfPointsInImage1.append(entry[1])

    setOfPointsInImage2=[]
    for entry in TableOfPoints:
        setOfPointsInImage2.append(entry[2])

    imageSize = cv.imread(url1).shape
    triangleList1 = DT.findDelaunayTriangles(setOfPointsInImage1,imageSize[0],imageSize[1])
    triangleList2 = DT.findDelaunayTriangles(setOfPointsInImage2,imageSize[0],imageSize[1])

    if(len(triangleList1) != len(triangleList2)):
        return -1

    serializedTriangleList1=[]
    for triangle in triangleList1:
        serializedTriangleEntry=[]
        index=0
        for point in TableOfPoints:
            if((point[1][0]==triangle[0])and(point[1][1]==triangle[1])):
                serializedTriangleEntry.append(index)
            if((point[1][0]==triangle[2])and(point[1][1]==triangle[3])):
                serializedTriangleEntry.append(index)
            if((point[1][0]==triangle[4])and(point[1][1]==triangle[5])):
                serializedTriangleEntry.append(index)
            index+=1
        serializedTriangleList1.append(serializedTriangleEntry)

    serializedTriangleList2=[]
    for triangle in triangleList2:
        serializedTriangleEntry=[]
        index=0
        for point in TableOfPoints:
            if((point[2][0]==triangle[0])and(point[2][1]==triangle[1])):
                serializedTriangleEntry.append(index)
            if((point[2][0]==triangle[2])and(point[2][1]==triangle[3])):
                serializedTriangleEntry.append(index)
            if((point[2][0]==triangle[4])and(point[2][1]==triangle[5])):
                serializedTriangleEntry.append(index)
            index+=1
        serializedTriangleList2.append(serializedTriangleEntry)

    mapping=[]
    index1 = 0
    for entry1 in serializedTriangleList1:
        index2 = 0
        for entry2 in serializedTriangleList2:
            if(entry1==entry2):
                mapping.append([index1,index2])
            index2 += 1
        index1 += 1

    if(len(mapping) != len(triangleList2)):
        return -2

    correspondingTrianglesList=[]
    for entry in mapping:
        point11 = serializedTriangleList1[entry[0]][0]
        point12 = serializedTriangleList1[entry[0]][1]
        point13 = serializedTriangleList1[entry[0]][2]
        point21 = serializedTriangleList2[entry[1]][0]
        point22 = serializedTriangleList2[entry[1]][1]
        point23 = serializedTriangleList2[entry[1]][2]

        x11 = TableOfPoints[point11][1][0]
        y11 = TableOfPoints[point11][1][1]

        x12 = TableOfPoints[point12][1][0]
        y12 = TableOfPoints[point12][1][1]


        x13 = TableOfPoints[point13][1][0]
        y13 = TableOfPoints[point13][1][1]


        x21 = TableOfPoints[point21][2][0]
        y21 = TableOfPoints[point21][2][1]

        x22 = TableOfPoints[point22][2][0]
        y22 = TableOfPoints[point22][2][1]


        x23 = TableOfPoints[point23][2][0]
        y23 = TableOfPoints[point23][2][1]




        correspondingTrianglesList.append([x11,y11,x12,y12,x13,y13,x21,y21,x22,y22,x23,y23])
    return correspondingTrianglesList

def executeMorph():
    global generateCorrespondingTriangles
    global url1
    global url2
    global statusBar
    global morphInExecution
    global activeImage
    global refreshCanvas1
    global refreshCanvas2
    global statusBar
    global mainGuiWindow
    global totalFrames
    activeImage=1
    refreshCanvas1()
    refreshCanvas2()
    if(morphInExecution):
        statusBar.config(text="Status Bar: Morph already in execution. Stop clicking repeatedly.")
        mainGuiWindow.update()
        return
    else:
        morphInExecution=True
    listOfTriangles = generateCorrespondingTriangles()
    if(listOfTriangles == -1):
        statusBar.config(text="Status Bar: Different number of Delaunay Triangles generated. Choose corresponding points correctly")
        mainGuiWindow.update()
        morphInExecution=False
        return
    if(listOfTriangles == -2):
        statusBar.config(text="Status Bar: Delaunay Triangles don't match. Choose the corresponding points correctly")
        mainGuiWindow.update()
        morphInExecution=False
        return

    if (len(listOfTriangles)==0):
        statusBar.config(text="Status Bar: Insufficient Points selected to form Delaunay Triangles.")
        mainGuiWindow.update()
        morphInExecution=False
        return

    outputVideo1 = cv.VideoWriter('./OutputFolder/WithBackground.avi', cv.VideoWriter_fourcc(*'MP42'), float(1), (imageSize[1], imageSize[0]))
    outputVideo2 = cv.VideoWriter('./OutputFolder/WithoutBackground.avi', cv.VideoWriter_fourcc(*'MP42'), float(1), (imageSize[1], imageSize[0]))

    for i in range (0,totalFrames+1):
        mainGuiWindow.update()
        image = cv.imread(url1)
        image2 = cv.imread(url2)
        numberOfChannels = len(image[0][0])
        statusBar.config(text="Status Bar: Processing Frame " + str(i)+ " of "+ str(totalFrames)+". Step 1/2: Generating background by interpolating values ... ")
        mainGuiWindow.update()

        for rowNumber in range(0,len(image)):
            mainGuiWindow.update()
            for cell in range(0,len(image[0])):
                for channel in range(0,len(image[0][0])):
                    val1 = image[rowNumber][cell][channel]
                    val2 = image2[rowNumber][cell][channel]
                    val1 = ((i*val2)+((totalFrames-i)*val1))/totalFrames
                    val1=int(val1)
                    image[rowNumber][cell][channel] = val1
                    image2[rowNumber][cell][channel] = 0


        for triangleNumber in range(len(listOfTriangles)):
            triangle = listOfTriangles[triangleNumber]
            statusBar.config(text="Status Bar: Processing Frame " + str(i)+ " of "+ str(totalFrames)+". Step 2/2: Morphing triangles and generating foreground...")
            mainGuiWindow.update()
            MorphedTriangle = Morphing.morph(i,totalFrames,triangle[0],triangle[1],triangle[2],triangle[3],triangle[4],triangle[5],triangle[6],triangle[7],triangle[8],triangle[9],triangle[10],triangle[11],url1,url2)


            for numberOfCellsInTriangle in range (len(MorphedTriangle)):
                entry = MorphedTriangle[numberOfCellsInTriangle]
                for channel in range(0,numberOfChannels):
                    image[entry[1]][entry[0]][channel] = entry[2][channel]
                    image2[entry[1]][entry[0]][channel] = entry[2][channel]
        cv.imwrite('./OutputFolder/In_Between_Frames/With_Background/Image'+str(i)+'.jpg',image)
        cv.imwrite('./OutputFolder/In_Between_Frames/Without_Background/Image'+str(i)+'.jpg',image2)
        outputVideo1.write(image)
        outputVideo2.write(image2)
    statusBar.config(text="Status Bar: Adding final formatting to video")
    mainGuiWindow.update()
    outputVideo1.release()
    outputVideo2.release()


    statusBar.config(text="Status Bar:")
    mainGuiWindow.update()
    morphInExecution=False

###########################################################
scrollableFrameHolder = tk.Frame(mainGuiWindow)
scrollableFrameHolder.grid(row=0,column=0,sticky='nsew')


container = tk.Frame(scrollableFrameHolder)
canvas = tk.Canvas(container,background='#FFFFAA')
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas,background="#FFFFAA")

scrollable_frame.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.bind('<Configure>',lambda e:canvas.itemconfig(frame_id, width=e.width))

canvas.configure(yscrollcommand=scrollbar.set)


container.pack(side="left", fill="both", expand=True)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


scrollable_frame.columnconfigure(0,weight=1)
###########################################################
#Frame containing 2 images which can be clicked to select points

activeImage = 1
coordinates=[[0,0],[0,0]]

ImageFramesContainer = tk.Frame(scrollable_frame)


image1size=cv.imread(url1).shape
image1 = ImageTk.PhotoImage(Image.open(url1))
canvas1=tk.Canvas(ImageFramesContainer,height=image1size[0],width=image1size[1],borderwidth=0,highlightthickness=0)
canvas1.grid(row=0,column=0)
refreshCanvas1()

image2size=cv.imread(url2).shape
image2 = ImageTk.PhotoImage(Image.open(url2))
canvas2=tk.Canvas(ImageFramesContainer,height=image2size[0],width=image2size[1],borderwidth=0,highlightthickness=0)
canvas2.grid(row=0,column=1)
refreshCanvas2()

ImageFramesContainer.grid(row=0,column=0)
###########################################################

#Checkbox to toggle delaunay triangles
tempVariableToDisableCheckboxBinding=tk.BooleanVar()
tempVariableToDisableCheckboxBinding.set(False)

showDelaunayTrianglesCheckBox = tk.Checkbutton(scrollable_frame, text="Show Delaunay Traingles",background='#FFFFAA',borderwidth=0,highlightthickness=0)
showDelaunayTrianglesCheckBox.grid(row=1,column=0)
showDelaunayTrianglesCheckBox.bind("<Button-1>",onToggleDelaunayTriangles)
###########################################################


#Input to change points colour along with corresponding submit button
frameForColorInput = tk.Frame(scrollable_frame,background='#FFFFAA')

defaultColorForPointsInput = tk.Entry(frameForColorInput,borderwidth=5,background='#'+defaultColoursForNewPoints)
defaultColorForPointsInput.insert(0,defaultColoursForNewPoints)
defaultColorForPointsInput.grid(row=2,column=0)
defaultColorForPointsInput.bind('<FocusOut>',onFocusAwayFromDefaultColorForPointsInput)

submitDefaultColorForPoints = tk.Button(frameForColorInput,text="Submit default colour for new points",command=changeDefaultColorForPoints,background='#'+defaultColoursForNewPoints)
submitDefaultColorForPoints.grid(row=2,column=1)

frameForColorInput.grid(row=2,column=0)

###########################################################

#Input number of video frames
frameForVideoFramesInput = tk.Frame(scrollable_frame,background='#FFFFAA')

numberOfVideoFramesInput = tk.Entry(frameForVideoFramesInput,borderwidth=5,background='#EEEE99')
numberOfVideoFramesInput.insert(0,totalFrames)
numberOfVideoFramesInput.grid(row=2,column=0)
numberOfVideoFramesInput.bind('<FocusOut>',onFocusAwayFromNumberOfVideoFramesInput)

submitNumberOfVideoFrames = tk.Button(frameForVideoFramesInput,text="Submit Number Of Video Frames",command=changeNumberOfVideoFrames,background='#EEEE99')
submitNumberOfVideoFrames.grid(row=2,column=1)

frameForVideoFramesInput.grid(row=3,column=0)

###########################################################

#Morph button
morphButton=tk.Button(scrollable_frame,text="Morph",command=executeMorph,background="#EEEE99")
morphButton.grid(row=4,column=0)
###########################################################

#Table of points
TableContainer = tk.Frame(scrollable_frame)
TableContainer.grid(row=5,column=0)
refreshTable()
###########################################################

#Status bar
statusBar = tk.Label(mainGuiWindow,text="Status Bar",relief='raised',anchor='w',background='#FFAAFF')
statusBar.grid(row=1,column=0,sticky='wes')

###########################################################

#Start the GUI window
mainGuiWindow.mainloop()
