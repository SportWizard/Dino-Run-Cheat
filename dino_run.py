import cv2
import mss
import numpy as np
import pyautogui

running = True
dino = cv2.imread("Dino.png")
dino_gray = cv2.cvtColor(dino, cv2.COLOR_BGR2GRAY)
template = cv2.imread("obstacle.png")
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template2 = cv2.imread("obstacle2.png")
template_gray2 = cv2.cvtColor(template2, cv2.COLOR_BGR2GRAY)
template3 = cv2.imread("obstacle3.png")
template_gray3 = cv2.cvtColor(template3, cv2.COLOR_BGR2GRAY)
template4 = cv2.imread("obstacle4.png")
template_gray4= cv2.cvtColor(template4, cv2.COLOR_BGR2GRAY)

obstacles = [template_gray, template_gray2, template_gray3, template_gray4]

method = cv2.TM_CCOEFF_NORMED #method of scanning the template and the screen
threshold = 0.35 #accuracy

def screen_shot(left=0, top=0, width=1920, height=1080):
    stc = mss.mss()
    scr = stc.grab({
        'left': left,
        'top': top,
        'width': width,
        'height': height
    })

    img = np.array(scr)
    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)

    return img

def dino_position():
    screen = screen_shot()

    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen_gray, dino_gray, method)
    min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc
    
    return location

dino_location = dino_position()

while running:
    screen = screen_shot(dino_location[0], dino_location[1]-30, 180, 100)

    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    for i in range(len(obstacles)):
        result = cv2.matchTemplate(screen_gray, obstacles[i], method)
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)

        #get location
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            location = min_loc
        else:
            location = max_loc

        bottomtemplateRight = (location[0] + 50, location[1] + 50)

        #draw rectangle
        cv2.rectangle(screen, location, bottomtemplateRight, (0, 0, 255), 5)

        if i == 2 or i == 3:
            max_value -= 0.3

        print(max_value)
        if max_value > threshold:
            pyautogui.press("space")
    cv2.imshow("Scanner", screen)

    key = cv2.waitKey(25)

    if key == ord("q"):
        running = False

cv2.destroyAllWindows()
