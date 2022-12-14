import cv2
import requests

avgX = list()
avgY = list()

##testing git updates

trained_data = cv2.CascadeClassifier('./def.xml')
webcam = cv2.VideoCapture(0)

while True:
    frame_read,frame = webcam.read()

    greyscale_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    divh = height/3

    width = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
    divw = width/3

    face_cordinates = trained_data.detectMultiScale(greyscale_frame)
    for (x,y,w,h) in face_cordinates:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cx = x + w/2
        cy = y + y/2
        #print("X: " + str(cx) + " y: " + str(cy))

        #loop 7 frames to find average pos of faces
        for x in range(0,20):
            avgX.append(cx)
            avgY.append(cy)

        #get new avg
        cx = sum(avgX) / len(avgX)
        cy = sum(avgY) / len(avgY)

        if int(cx) < divw and int(cy) < divh:
            print("LU")
            requests.get("http://192.168.100.3/cgi-bin/ptzctrl.cgi?ptzcmd&leftup&2&2")
        elif int(cx) < divw and int(cy) > height - divh:
            print("LD")
            requests.get("http://192.168.100.3/cgi-bin/ptzctrl.cgi?ptzcmd&leftdown&2&2")
        elif int(cx) > width - divw and int(cy) < divh:
            print("RU")
            requests.get("http://192.168.100.3/cgi-bin/ptzctrl.cgi?ptzcmd&rightup&2&2")
        elif int(cx) > width - divw and int(cy) > height - divh:
            print("RD")
            requests.get("http://192.168.100.3/cgi-bin/ptzctrl.cgi?ptzcmd&rightdown&2&2")
        #### X Mvmt
        elif int(cx) < divw:
            print("L")
            requests.get("http://192.168.100.3/cgi-bin/ptzctrl.cgi?ptzcmd&left&2&2")
        elif int(cx) > width - divw:
            print("R")
            requests.get("http://192.168.100.3/cgi-bin//ptzctrl.cgi?ptzcmd&right&2&2")
        #### Y Mvmt
        elif int(cy) < divh:
            print("U")
            requests.get("http://192.168.100.3/cgi-bin/ptzctrl.cgi?ptzcmd&up&2&2")
        elif int(cy) > height - divh:
            print("D")
            requests.get("http://192.168.100.3/cgi-bin/ptzctrl.cgi?ptzcmd&down&2&2")
        else:
            requests.get("http://192.168.100.3/cgi-bin/ptzctrl.cgi?ptzcmd&ptzstop")

        #reset avg of 7 frames
        avgX.clear()
        avgY.clear()

    cv2.imshow("Out:",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()