import numpy as np
import cv2
import time
from matplotlib import pyplot as plt


# inicializamos la toma de video
video = cv2.VideoCapture('./../../common/video/test-city.mp4')
fps = video.get(cv2.CAP_PROP_FPS)
# inicializamos el algoritmo ORB
orb = cv2.ORB_create(fastThreshold=50)

while True:
  # usaremos esto para fijar el framerate 
  now = time.time()
  # Obtenemos la info del fotograma actual
  ret, frame = video.read()
  # redimencionamos el fotograma
  frame = cv2.resize(frame, (1280, 720))

  # lo convertimos a escala de grises
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  # canvas blanco para visualizar solo los puntos
  blankCanvas = np.zeros((720, 1280, 3), np.uint8)
  blankCanvas.fill(255)

  # Obtemenos los puntos clave
  kp = orb.detect(gray, None)
  orbImg = cv2.drawKeypoints(frame, kp, None, color=(255,0,0))
  points = cv2.drawKeypoints(blankCanvas, kp, None, color=(255,0,0))
  # mostramos el fotograma
  cv2.imshow('frame', gray)
  cv2.imshow('orb', orbImg)
  cv2.imshow('points', points)

  timeDiff = time.time() - now
  # if (timeDiff < 1.0/(fps)):
    # time.sleep(1.0/(fps) - timeDiff)

  key = cv2.waitKey(1)
  if key == 13:
    break

video.release()
cv2.destroyAllWindows()