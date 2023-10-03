from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
import math

import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import cv2

class CamApp(App):
    def build(self):
        self.img1=Image()
        layout = BoxLayout(orientation='vertical')
        self.face_pos_label = Label(text='0, 0')
        self.face_distance_to_center_label = Label(text='0')
        layout.add_widget(self.face_pos_label)
        layout.add_widget(self.face_distance_to_center_label)
        layout.add_widget(self.img1)
        self.width = 320
        self.height = 240
        self.cam_pan = 40
        self.cam_tilt = 20

        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        self.detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)   
        Clock.schedule_interval(self.update, 1.0/33.0)
        return layout

    def update(self, dt):
        # display image from cam in opencv window
        
        # Detects faces of different sizes in the input image
        success, img = self.capture.read()

        # Find face mesh in the image
        # img: Updated image with the face mesh if draw=True
        # faces: Detected face information
        img, bboxs = self.detector.findFaces(img, draw=False)

        # Check if any face is detected
        if bboxs:
            # Loop through each bounding box
            for bbox in bboxs:
                # bbox contains 'id', 'bbox', 'score', 'center'

                # ---- Get Data  ---- #
                center = bbox["center"]
                x, y, w, h = bbox['bbox']
                score = int(bbox['score'][0] * 100)

                # ---- Draw Data  ---- #
                cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
                cvzone.putTextRect(img, f'{score}%', (x, y - 10))
                cvzone.cornerRect(img, (x, y, w, h))
                cx = (x + x + w) // 2
                cy = (y + y + h) // 2

                cv2.line(img,(cx,cy),(self.width,self.height),(0,0,255),2)

                distance = math.dist((cx,cy),(self.width,self.height))
                
                

                # Correct relative to centre of image
                turn_x  = float(x - (self.width/2))
                turn_y  = float(y - (self.height/2))

                # Convert to percentage offset
                turn_x  /= float(self.width/2)
                turn_y  /= float(self.height/2)
                
                # Scale offset to degrees (that 2.5 value below acts like the Proportional factor in PID)
                turn_x   *= 2.5 # VFOV
                turn_y   *= 2.5 # HFOV
                cam_pan   = -turn_x
                cam_tilt  = turn_y


                # Clamp Pan/Tilt to 0 to 180 degrees
                cam_pan = max(0,min(180,cam_pan))
                cam_tilt = max(0,min(180,cam_tilt))

                print(cam_pan, cam_tilt)

                # # Update the servos
                # pan(int(cam_pan-90))
                # tilt(int(cam_tilt-90))


        # convert it to texture
        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()