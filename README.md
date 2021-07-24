#Anonymizer

![gif](./static/gifa.gif)
#### Description

This is a command line script with the capability of apply a filter to the faces in a picture.
Automatically deliver the image with the time when was processed.


####Libraries:
* argparse
* dlib
* cv2
* imutils
* numpy 

####Use:
-i or --image -> String (required)

`path to the image.`

-m or --model -> String (default=mmod_human_face_detector.dat)

`path to the model. `

-l or --label -> String (default=None)

`add a label in a rectangle at the top-left corner of the output image.`

-u or --upsample -> Integer (default=1)

`upsample the image, preprosses the image for better adquisition of a face, tune it if some faces aren't located.`

-w or --width -> Integer (default=600)

`the width of the output image in pixels, the ratio is conserved.`

-f or --filtermask

`select the types of mask to apply: 0= black box, 1= blurry, 2= big pixels, 3=only eyes.`

black box

![black box](./static/black%20box.jpg)

blurry

![gaussian](./static/gaussian.jpg)

big pixels

![big pixels](./static/big%20pixels.jpg)

only eyes

![eyes](./static/eyes.jpg)

