import cv2

# load the required trained XML classifiers
# https://github.com/Itseez/opencv/blob/master/
# data/haarcascades/haarcascade_frontalface_default.xml
# Trained XML classifiers describes some features of some
# object we want to detect a cascade function is trained
# from a lot of positive(faces) and negative(non-faces)
# images.
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

# capture frames from a camera
cap = cv2.VideoCapture(0)

# loop runs if capturing has been initialized.
while 1:

	# reads frames from a camera
	ret, img = cap.read()
	center = img.max()-img.min()
	# convert to gray scale of each frames
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Detects faces of different sizes in the input image
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	#for (x,y,w,h) in faces:
		# cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
		# roi_gray = gray[y:y+h, x:x+w]
		# roi_color = img[y:y+h, x:x+w]
		# print(f"X: {x}, Y: {y}")
	if len(faces) is 1:
		x,y,w,h = faces[0]
		centerX, centerY = int(x+(w/2)),int(y+(h/2))
		cv2.circle(img, (centerX, centerY),1,(0,0,255),10)
		cv2.line(img, (centerX, centerY),(center,center),(0,0,255),10)

	# Display an image in a window
	cv2.imshow('img',img)

	# Wait for Esc key to stop
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

# Close the window
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()
