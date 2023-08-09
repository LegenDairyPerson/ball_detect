import numpy as np
import cv2

def simple_text(text, dist):
    cv2.putText(result, text, (50, height-dist), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

cap = cv2.VideoCapture(0)
threshold = 20

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0, 100, 100])
    upper_blue = np.array([30, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    circle_center = None
    # Filter the contours to find the circular contour (adjust the parameters as needed)
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * area / (perimeter * perimeter)

        # Adjust the threshold for circularity to filter the circular contour
        if 0.5 < circularity < 1.5 and area > 50:
            # Calculate the centerpoint of the circular contour
            M = cv2.moments(contour)
            center_x = int(M['m10'] / M['m00'])
            center_y = int(M['m01'] / M['m00'])

            circle_center = center_x
            # Draw a circle to highlight the centerpoint
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.line(result, (frame.shape[1]//2, 0), (frame.shape[1]//2, frame.shape[0]), color= (0, 0, 255), thickness= 1)

    # cv2.putText(result, "hi", (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), thickness= 1)
    if circle_center is not None:
        print("y")
        if abs(frame.shape[1]//2 - circle_center) <= threshold:
            simple_text("On Target", 25)
        elif circle_center > frame.shape[1]//2:
            simple_text("Move Left", 25)
        elif circle_center < frame.shape[1]//2:
            # result = cv2.putText(result, "Move Right", (50, height - 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))
            simple_text("Move Right", 25)
    else:
        print("n")
        simple_text("N/A", 25)


    # cv2.imshow("iframe", frame)
    cv2.imshow('frame', result)
    # cv2.imshow('mask', mask)

    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()