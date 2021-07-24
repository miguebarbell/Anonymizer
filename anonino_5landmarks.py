#

import argparse
import dlib
import cv2
import imutils
import numpy as np
from imutils import face_utils
import anonhelper

# construct the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', type=str, required=True, help='path to input the image')
ap.add_argument('-m', '--model', type=str, default='../../commonfiles/mmod_human_face_detector.dat',
                help="path to dlib pre-trained model")
ap.add_argument('-l', '--label', type=str, default=0,
                help='add a label/location to your image in a black rectangle top-left corner')
ap.add_argument("-f", "--filtermask", type=int, default=0,
                help="select the types of mask to apply: 0= black box, 1= blurry, 2= big pixels, 3=only eyes")
ap.add_argument("-u", "--upsample", type=int, default=1,
                help="# of times to upsample, the bigger more accurate and slow")
ap.add_argument("-w", "--width", type=int, default=600, help="select the width of the output image")

args = vars(ap.parse_args())

# load image
image = cv2.imread(args["image"])
image = imutils.resize(image, width=args["width"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# prepare the model for facial marks
if args["filtermask"] == 3:
    landmark_detector = dlib.get_frontal_face_detector()
    landmark_predictor = dlib.shape_predictor('../../commonfiles/shape_predictor_5_face_landmarks.dat')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = landmark_detector(gray, 1)
    print(f"[INFO] found {len(faces)} face for landmarks.")
    for (i, face) in enumerate(faces):
        shape = landmark_predictor(gray, face)
        shape = face_utils.shape_to_np(shape)
        thickness = round((shape[0][0] - shape[2][0])/5)
        print(f"line thickness {thickness}")
        cv2.line(image, shape[0], shape[2], (0, 0, 0), thickness)
else:
    # load the model
    print("[INFO] loading CNN face detector...")
    detector = dlib.cnn_face_detection_model_v1(args["model"])
    # perform the face detection
    results = detector(rgb, args["upsample"])
    faces = [anonhelper.convert_and_trim_bb(image, r.rect) for r in results]
    print(f"[INFO] found {len(faces)} faces")
    # add the filters
    face_num = 1
    for (startX, startY, w, h) in faces:
        # todo: make a function that return the face blurred
        endX = startX + w
        endY = startY + h
        # show the face detected
        face_detected = image[startY:endY, startX:endX]
        # anonhelper.show_and_save(face_detected, title=f"Face n: {face_num}", save=False)
        cv2.imshow(f"Face n: {face_num}", face_detected)
        cv2.waitKey()
        print(f'Mask face {face_num}? [Y]/n')
        response = input()
        cv2.destroyAllWindows()
        if response == 'n':
            response = False
        else:
            response = True
        face_num += 1
        if response:
            if args['filtermask'] == 0:
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 0), -1)
            elif args["filtermask"] == 1:
                # make a subimage
                face_filter = image[startY:endY, startX:endX]
                face_filter = cv2.GaussianBlur(face_filter, (71, 71), 71)
                image[startY:endY, startX:endX] = face_filter

            elif args['filtermask'] == 2:
                # print("working in big pixels")
                face_filter = image[startY:endY, startX:endX]
                temp = cv2.resize(face_filter, (10, 10), interpolation=cv2.INTER_LINEAR)
                output = cv2.resize(temp, (endX - startX, endY - startY), interpolation=cv2.INTER_NEAREST)
                image[startY:endY, startX:endX] = output

            elif args["filtermask"] == 4:
                # make a subimage
                face_filter = image[startY:endY, startX:endX]
                face_filter = cv2.medianBlur(face_filter, 23)
                image[startY:endY, startX:endX] = face_filter

# return the image if they recognize any image
# check if the output is different
difference = np.subtract(image, imutils.resize(cv2.imread(args['image']), width=args['width']))
if sum(difference.flatten()) == 0:
    print('0 Faces not founded')
else:
    if args['label'] != 0:
        print(f"[INFO] adding {args['label'].upper()} to image")
        cv2.rectangle(image, (0, 0), (len(args['label']*9), 17), (255, 255, 255), -1)
        cv2.putText(image, args['label'].upper(), (0, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
    anonhelper.show_and_save(image, title="Anonymized", save=True)





