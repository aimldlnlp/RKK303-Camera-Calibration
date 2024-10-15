# Camera Calibration with OpenCV

## Overview
This project focuses on camera calibration using a ChArUco board, a combination of checkerboard and ArUco markers, to compute the intrinsic camera parameters and distortion coefficients. The calibration process was applied to a **HuatengVision industrial camera** equipped with a **45 mm focal length lens**, yielding a more accurate camera model for industrial applications, such as quality control and robotic vision systems.

## Table of Contents
- [Overview](#overview)
- [Objectives](#objectives)
- [Hardware and Tools](#hardware-and-tools)
- [Methodology](#methodology)
- [Results](#results)

## Objectives
- To perform accurate camera calibration using OpenCV and a ChArUco board.
- To calculate the intrinsic parameters, including the camera matrix and distortion coefficients.
- To undistort images by removing convex distortion from the camera.
- To validate the calibration results by comparing them with the camera's physical settings.

## Hardware and Tools
- **Camera**: HuatengVision industrial camera
- **Lens**: 45 mm focal length lens
- **Calibration Board**: ChArUco board (combination of checkerboard and ArUco markers)
- **Software**: OpenCV (Python)

## Methodology
1. **Image Capture**: Multiple images of the ChArUco board were taken at different angles and positions using the industrial camera.
2. **Detection of Markers**: The ChArUco markers were detected from the captured images.
3. **Calibration**: OpenCV was used to process the detected markers, calculate the intrinsic camera parameters (camera matrix and distortion coefficients), and perform camera calibration.
4. **Undistortion**: After calibration, the distortion was removed from the captured images to achieve undistorted results.

## Results
- **Focal Length**: 
  - Calculated on x-axis: **49.26 mm**
  - Calculated on y-axis: **46.65 mm**
- The calculated focal lengths were close to the physical 45 mm lens settings.
- The calibration successfully flattened the convex distortion, as observed in the undistorted images, with minor errors caused by tilt angles and camera settings during image capture.
