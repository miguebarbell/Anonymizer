#Anonymizer

![gif](./static/gifa.gif)
#### Description

This is a command line script with the capability of apply a filter to the faces in a picture.

####Libraries:
* argparse
* dlib
* cv2
* imutils
* numpy 

####Use:

-f or --filtermask

`select the types of mask to apply: 0= black box, 1= blurry, 2= big pixels, 3=only eyes`

black box

![black box](./static/black%20box.jpg)

blurry

![gaussian](./static/gaussian.jpg)

big pixels

![big pixels](./static/big%20pixels.jpg)

only eyes

![eyes](./static/eyes.jpg)