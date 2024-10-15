import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread

# Load camera matrix and distortion coefficients
mtx = np.load("/home/sulthan/Documents/coolyeah/Computer Vision/cam-mat-NYKtest.npy")
dist = np.load("/home/sulthan/Documents/coolyeah/Computer Vision/dist-coeffs-NYKtest.npy")

print(mtx)
print("=================================")
print(dist)

# Load an image
img = imread("/home/sulthan/Documents/coolyeah/Computer Vision/jepri/WhatsApp Image 2024-10-03 at 22.59.08 (3).jpeg")

# Undistort the image
undistorted = cv2.undistort(img, mtx, dist)

# Display the original and undistorted images
plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original Image")
plt.subplot(1, 2, 2)
plt.imshow(undistorted)
plt.title("Undistorted Image")
plt.show()
