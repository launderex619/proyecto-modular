import cv2
import numpy as np 
import glob
from tqdm import tqdm
from pathlib import Path
import PIL.ExifTags
import PIL.Image


def executeCalibration():
  # Definir el tamaño del chessboard que usaremos para calibrar
  chessboard_size = (7, 5)

  # Definir arrays donde almacenaremos los puntos detectados
  obj_points = []
  img_points = []

  # Preparar un grid para los puntos a mostrar
  objp = np.zeros( (np.prod(chessboard_size), 3), dtype=np.float32 )
  objp[:,:2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

  # cargamos las imágenes como parámetros
  calibration_patterns = glob.glob( 'C:/Git/proyecto-modular/refactor/calibration/patterns/*')
  # print( calibration_patterns )

  # iteramos por cada imagen
  for image in tqdm(calibration_patterns):
    img = cv2.imread(image) # carga la imagen

    # if not img:
    #   print("Failure loading image")
    #   return 

    gry_img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY ) # la convertimos a escala de grises
    print( 'Image loaded, analiyzing. . .' )
    ret, corners = cv2.findChessboardCorners( gry_img, chessboard_size, None ) # detectamos las esquinas del chessboard

    if ret == True:
      print( 'Chessboard detected!!! [ {image} ]'.format(image=image) )
      # definimos el criterio para la precisión de cada subpixel
      criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001 )
      # refinamos la ubicación de cada esquina basándonos en el criterio
      cv2.cornerSubPix( gry_img, corners, (5, 5), (-1, -1), criteria )
      obj_points.append(objp)
      img_points.append(corners)

  # calibramos la cámara
  ret, K, dist, rvecs, tvecs = cv2.calibrateCamera( obj_points, img_points, gry_img.shape[::-1], None, None  )

  # guardamos los parámetros en un archivo numpy
  np.save( 'C:/Git/proyecto-modular/refactor/calibration/params/ret', ret )
  np.save( 'C:/Git/proyecto-modular/refactor/calibration/params/K', K )
  np.save( 'C:/Git/proyecto-modular/refactor/calibration/params/dist', dist )
  np.save( 'C:/Git/proyecto-modular/refactor/calibration/params/rvecs', rvecs )
  np.save( 'C:/Git/proyecto-modular/refactor/calibration/params/tvecs', tvecs )

  # exif_img = PIL.Image.open( calibration_patterns[0] )

  # exif_data = {
  #   PIL.ExifTags.TAGS[k]:v 
  #   for k, v in exif_img._getexif().items()
  #   if k in PIL.ExifTags.TAGS
  # }

  # obtener la distancia focal en forma de tupla
  # focal_length_exif = exif_data['FocalLength']

  # obtener la distancia focal en forma decimal
  # focal_length_dec = focal_length_exif[0]/focal_length_exif[1]

  # guardamos la distancia focal
  # np.save( 'params/FocalLength', focal_length_dec )

  mean_error = 0
  for i in range( len(obj_points) ):
    img_points2, _ = cv2.projectPoints( obj_points[i], rvecs[i], tvecs[i], K, dist )
    error = cv2.norm( img_points[i], img_points2, cv2.NORM_L2 )/len(img_points2)
    mean_error += error

  total_error = mean_error/len(obj_points)
  print( total_error )


def loadCalibration():
  # cargamos datos calibrados
  ret = np.load( 'C:/Git/proyecto-modular/refactor/calibration/params/ret.npy' )
  K = np.load( 'C:/Git/proyecto-modular/refactor/calibration/params/K.npy' )
  dist = np.load( 'C:/Git/proyecto-modular/refactor/calibration/params/dist.npy' )
  rvecs = np.load( 'C:/Git/proyecto-modular/refactor/calibration/params/rvecs.npy' )
  tvecs = np.load( 'C:/Git/proyecto-modular/refactor/calibration/params/tvecs.npy' )
  # cargamos distancia focal
  # focal_length = np.load( './params/FocalLength.npy' )
  # retornamos
  # return ret, K, dist, focal_length
  return ret, K, dist, rvecs, tvecs