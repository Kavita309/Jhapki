from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from twilio.rest import Client
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import pygame
from geopy.geocoders import Nominatim
import geocoder

def loc():
	g = geocoder.ip('me')
	print(g.latlng)
	geolocator = Nominatim(user_agent="Drowsiness Detection")
	loca=str(g.latlng[0])+","+str(g.latlng[1])
	# location = geolocator.reverse(loca)
	location = geolocator.reverse("28.6082819, 77.0350079")
	print(location.address)
	print((location.latitude, location.longitude))
	return location


def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("myapp:addprofile")
    template_name = "signup.html"


class MyProfile(TemplateView):
    template_name = 'myprofile.html'

def SendSMS():
	account_sid = 'ACbbc0add8b0c9821500ebef3164b07884'
	auth_token = 'b7497199ab5af1e2c2783759f4ea279a'
	client = Client(account_sid, auth_token)
	loc()
	message = client.messages.create(
	                              from_='+15077246172',
	                              body='Drowsiness Detected! Mansi needs your help uregntly. Her Location: NSIT, Azad Hind Fauj Marg, Nawada, Sector 3, Dwarka, West Delhi, Delhi, 110078, India (28.6082819, 77.0350079)',
								  # body='Drowsiness Detected! {User} needs your help uregntly.
								  # Her Location: {location}
								  # (location.latitude,location.longitude)',
	                              to='+918860243261'
	                          )
	print(message.sid)


def StartDrive(request):
	pygame.mixer.pre_init(22050, -16, 2, 64)
	pygame.mixer.init()
	pygame.mixer.quit()
	pygame.mixer.init(22050, -16, 2, 64)

	EYE_AR_THRESH = 0.3
	EYE_AR_CONSEC_FRAMES = 3
	sleep_frames = 100

    # initialize the frame counters and the total number of blinks
	COUNTER = 0
	TOTAL = 0
	SETS = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
	print("[INFO] loading facial landmark predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor("static/shape_predictor_68_face_landmarks0.dat")

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
	print("[INFO] starting video stream thread...")
	vs = FileVideoStream("").start()
	fileStream = True
	vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
	fileStream = False
	time.sleep(1.0)

    # loop over frames from the video stream
	while True:
    	# if this is a file video stream, then we need to check if
    	# there any more frames left in the buffer to process
		if fileStream and not vs.more():
			break

    	# grab the frame from the threaded video file stream, resize
    	# it, and convert it to grayscale
    	# channels)
		frame = vs.read()
		frame = imutils.resize(frame, width=450)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    	# detect faces in the grayscale frame
		rects = detector(gray, 0)

    	# loop over the face detections
		for rect in rects:
    		# determine the facial landmarks for the face region, then
    		# convert the facial landmark (x, y)-coordinates to a NumPy
    		# array
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)

    		# extract the left and right eye coordinates, then use the
    		# coordinates to compute the eye aspect ratio for both eyes
			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			leftEAR = eye_aspect_ratio(leftEye)
			rightEAR = eye_aspect_ratio(rightEye)

    		# average the eye aspect ratio together for both eyes
			ear = (leftEAR + rightEAR) / 2.0

    		# compute the convex hull for the left and right eye, then
    		# visualize each of the eyes
			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)
			cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

    		# check to see if the eye aspect ratio is below the blink
    		# threshold, and if so, increment the blink frame counter
			if ear < EYE_AR_THRESH:
				COUNTER += 1
				if COUNTER >= sleep_frames:
					COUNTER=0
					SETS += 1
					print("DONT SLEEP")
					pygame.mixer.music.load("static/file.mp3")
					pygame.mixer.music.play()

					if SETS >= 4:
						SendSMS()
						SETS = 0
						print("msg sent")

    		# otherwise, the eye aspect ratio is not below the blink
    		# threshold
			else:
				pygame.mixer.music.stop()
    			# if the eyes were closed for a sufficient number of
    			# then increment the total number of blinks
				if COUNTER >= EYE_AR_CONSEC_FRAMES:
					TOTAL += 1


    			# reset the eye frame counter
					COUNTER = 0
					SETS = 0

			cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "Frames: {}".format(COUNTER), (30, 200),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

    	# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

    # do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

	return render(request,'index.html')


class add_profile(CreateView):
    form_class = forms.AddProfileForm
    success_url = reverse_lazy("myapp:login")
    template_name = "addprofile.html"
