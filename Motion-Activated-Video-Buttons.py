

# Press buttons using motion detection. Append press and release sequence to lists.


import cv2
import numpy as np
import time


cap = cv2.VideoCapture(0)

# cap.set(propId=cv2.CAP_PROP_FPS, value=30)
# fps = cap.get(cv2.CAP_PROP_FPS)

b1 = 0
b2 = 0
b3 = 0

b1t = 0
b2t = 0
b3t = 0

hold = 0.3          # a higher number better avoids double presses, but also disables button for a longer time

seq = []            # press sequence
rel_seq = []        # release sequence

while True:

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    if ret == True:

        # Adjusts threshold depending on highest light value pixel, to better detect in the dark, without getting
        # false detections in high light situations
        npmax = np.max(frame1)
        npmax = npmax / 255
        th = 22 * npmax + 4
        th = round(th, 0)

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY)

        btn1 = np.sum(thresh[300:360, 40:100])
        cv2.rectangle(frame1, (40, 300), (100, 360), (255, 0, 0), 2)
        cv2.putText(frame1, "BTN 1", (50, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (190, 190, 0), 2)

        btn2 = np.sum(thresh[200:260, 40:100])
        cv2.rectangle(frame1, (40, 200), (100, 260), (255, 0, 0), 2)
        cv2.putText(frame1, "BTN 2", (50, 195), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (190, 190, 0), 2)

        btn3 = np.sum(thresh[100:160, 40:100])
        cv2.rectangle(frame1, (40, 100), (100, 160), (255, 0, 0), 2)
        cv2.putText(frame1, "BTN 3", (50, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (190, 190, 0), 2)

        saved_seq = len(seq)
        saved_rel_seq = len(rel_seq)

        # If btn's are pressed fast and in 3, 2, 1 then 2 will be skipped, can be fixed, but btn's shouldn't be pressed too fast
        if btn1 > 500:
            b1t = time.time() + hold  # makes btn stay on for, a time after last press, to avoid double pressing

        if b1t > time.time(): # and b2 == 0 and b3 == 0:        # make so only one button pressed at a time
            if b1 == 0:
                seq.append(1)
                print("Button 1 pressed")
            b1 = 1
            cv2.putText(frame1, "BTN 1", (250, 90), cv2.FONT_HERSHEY_SIMPLEX, 2, (190, 190, 0), 3)
            cv2.rectangle(frame1, (45, 305), (95, 355), (0, 0, 155), 6)
        else:
            if b1 == 1:             # just once for on release
                rel_seq.append(1)
            b1 = 0

        if btn2 > 500:
            b2t = time.time() + hold  # makes btn stay on for, a time after last press, to avoid double pressing

        if b2t > time.time(): #and b1 == 0 and b3 == 0:        # make so only one button pressed at a time
            if b2 == 0:
                seq.append(2)
                print("          Button 2 pressed")
            b2 = 1
            cv2.putText(frame1, "BTN 2", (250, 90), cv2.FONT_HERSHEY_SIMPLEX, 2, (190, 190, 0), 3)
            cv2.rectangle(frame1, (45, 205), (95, 255), (0, 0, 155), 6)
        else:
            if b2 == 1:
                rel_seq.append(2)
            b2 = 0

        if btn3 > 500:
            b3t = time.time() + hold  # makes btn stay on for, a time after last press, to avoid double pressing

        if b3t > time.time(): #and b1 == 0 and b2 == 0:   # make so only one button pressed at a time (the "ands")
            if b3 == 0:   # just once per press            # if more pressed per frame previous code will trump
                seq.append(3)
                print("                         Button 3 pressed")
            b3 = 1
            cv2.putText(frame1, "BTN 3", (250, 90), cv2.FONT_HERSHEY_SIMPLEX, 2, (190, 190, 0), 3)
            cv2.rectangle(frame1, (45, 105), (95, 155), (0, 0, 155), 6)
        else:
            if b3 == 1:
                rel_seq.append(3)
            b3 = 0

        if len(seq) != saved_seq:  # if seq changed print it
            print("On Press", seq)

        if len(rel_seq) != saved_rel_seq:  # if rel seq changed print it
            print("On Release", rel_seq)

        # Optional
        # dilated = cv2.dilate(thresh, None, iterations=3)
        dilated = thresh

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame1, contours, -1, (0, 25, 255), 2)
        for c in contours:
            if cv2.contourArea(c) < 20:
                continue
            x, y, w, h = cv2.boundingRect(c)
            # cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 1)

        cv2.imshow("Frame1", frame1)
        # print(fps)

        if cv2.waitKey(1) & 0xff == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()













