import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np


def edit(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')

    eyes = eye_cascade.detectMultiScale(
        image, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    x = 0
    y = 0
    w = 0
    h = 0

    for (ex, ey, ew, eh) in eyes:
        if (ex+ew > image.shape[1]//2):
            x = ex
            y = ey
            w = ew
            h = eh

    crop = image[y-10:y+h+10, x-10:x+w+10]
    resize = cv2.resize(crop, (300, 300))
    blur = cv2.medianBlur(resize, 5)
    color = cv2.applyColorMap(blur, cv2.COLORMAP_HOT)

    mask = np.zeros(color.shape[:2], dtype="uint8")
    cv2.circle(mask, (150, 150), 130, 255, -1)
    masked = cv2.bitwise_and(color, color, mask=mask)
    bg = np.ones_like(color, np.uint8)*240
    cv2.bitwise_not(bg, bg, mask=mask)
    masked = cv2.add(masked, bg)
    return masked


def brightness(image, bright):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - bright
    v[v > lim] = 255
    v[v <= lim] += bright

    final_hsv = cv2.merge((h, s, v))
    image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return image


fourcc = VideoWriter_fourcc(*'MP4V')
video = VideoWriter('mata_menyala.mp4', fourcc, float(6), (300, 300))

for a in range(1, 63):
    image = cv2.imread(str(a)+'.jpg')
    try:
        image = edit(image)
    except:
        image = brightness(image, 60)
        image = edit(image)
    video.write(image)
    cv2.imwrite(str(a)+'.jpg', image)
    print(a)

video.release()
