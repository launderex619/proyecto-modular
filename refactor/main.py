
from calibration.calibrate import executeCalibration, loadCalibration


if __name__ == '__main__':  
  # ejecutamos calibración si es la primera vez que trabajamos con una cámara
  # executeCalibration()

  # cargamos la matriz de calibración de la cámara
  ret, K, dist, rvecs, tvecs = loadCalibration()
  print("asdasdas")