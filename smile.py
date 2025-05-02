import cv2

#use face, smile and eye from pretrained model Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')          
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye.xml') 
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml') 
                      

def detect_smiles(image):
    
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)

      for (x, y, w, h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,255),2)
            cv2.putText(image, "Face", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

            for (sx, sy, sw, sh) in smiles:
                  cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
                  cv2.putText(roi_color, "smile", (sx, sy),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)   
      return image