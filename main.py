from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
import math

import cv2

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

class CamApp(App):
    def build(self):
        self.img1=Image()
        layout = BoxLayout(orientation='vertical')
        self.face_pos_label = Label(text='0, 0')
        self.face_distance_to_center_label = Label(text='0')
        layout.add_widget(self.face_pos_label)
        layout.add_widget(self.face_distance_to_center_label)
        layout.add_widget(self.img1)

        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)
        return layout

    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        img = frame
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
            center_x, center_y = int(x+(w/2)),int(y+(h/2))
            self.face_pos_label.text = f"{center_x}, {center_y}"
            distance = math.dist((center_x, center_y),(center,center))
            # self.face_distance_to_center_label.text = f"{distance}

            angle_x = center_x - center
            angle_x = (angle_x + 180) % 360 - 180
            angle_x = angle_x / 10


            angle_y = center_y - center
            angle_y = (angle_y + 180) % 360 - 180
            angle_y = angle_y / 10


            self.face_distance_to_center_label.text = f"{angle_x}, {angle_y}"

            cv2.circle(img, (center_x, center_y),1,(0,0,255),10)
            cv2.line(img, (center_x, center_y),(center,center),(0,0,255),10)


        cv2.imshow("CV2 Image", frame)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()