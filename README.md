# Image-Morphing-Software

The Software takes input of two images of the same size and morphs one image into another. 
This is done using a GUI. The GUI is used to mark control points on both the images. 
Delaunay Triangulation is applied on the points selected. 
The triangles thus formed are warped using Affine Transformation. 
Finally, a set of intermediate images are obtained that show one image being morphed into the other image.

NOTE: The GUI, The Delaunay Triangulation, The Affine Transform have all been created indigenously, non of the OpenCV libraries have been used to simulate their funcionalities.

## The Working of the Software

![The initial view of the GUI](initialGUI.JPG)<br>
The initial view of the GUI<br>

![Feature Points Marked](fp2.JPG)<br>
Feature Points Marked<br>

![Table for Feature Points present on GUI](tb2.JPG)<br>
Table for Feature Points present on GUI<br>

![Corresponding Delaunay Triangles mapped for given feature points](dllll.JPG)<br>
Corresponding Delaunay Triangles mapped for given feature points<br>

![After clicking the morph button, the status of morphing can be seen here](stb.JPG)<br>
After clicking the morph button, the status of morphing can be seen here<br>

![Intermediate images with background](withb.png)<br>
Intermediate images with background<br>

![Intermediate images without background](outb.png)<br>
Intermediate images without background<br><br><br>

## Contributor - Abhay Aravinda [Email - <17ucs002@lnmiit.ac.in>]
