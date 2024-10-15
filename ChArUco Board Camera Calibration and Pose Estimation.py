import cv2
import numpy as np
import os

ARUCO_DICT = cv2.aruco.DICT_6X6_100
SQUARES_VERTICALLY = 5  # rows
SQUARES_HORIZONTALLY = 7  # columns
SQUARE_LENGTH = 0.036  # size of chessboard squares in meters
MARKER_LENGTH = 0.021  # size of ArUco markers in meters
PATH_TO_YOUR_IMAGES = "/home/sulthan/Documents/coolyeah/ComputerVision/jepri/"

all_rvecs = []
all_tvecs = []
all_corners = []
all_ids = []

dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
board = cv2.aruco.CharucoBoard_create(
    squaresX=SQUARES_HORIZONTALLY,
    squaresY=SQUARES_VERTICALLY,
    squareLength=SQUARE_LENGTH,
    markerLength=MARKER_LENGTH,
    dictionary=dictionary
)

params = cv2.aruco.DetectorParameters_create()
params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_NONE
print('params: ', params)

def calibrate_and_save_parameters():
    rvecs = []
    tvecs = []
    camera_matrix = None
    dist_coeffs = None

    # Load images from folder
    print([i for i in os.listdir(PATH_TO_YOUR_IMAGES)])
    image_files = [os.path.join(PATH_TO_YOUR_IMAGES, f) for f in os.listdir(PATH_TO_YOUR_IMAGES) if f.endswith(".jpeg")]
    image_files.sort()

    all_charuco_corners = []
    all_charuco_ids = []
    print(image_files)

    for image_file in image_files:
        print(f"Processing file: {image_file}")
        image = cv2.imread(image_file)
        image_copy = image.copy()

        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(image, dictionary, parameters=params)

        if marker_ids is not None and len(marker_ids) >= 4:
            cv2.aruco.drawDetectedMarkers(image_copy, marker_corners, marker_ids)
            retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
            
            if retval:
                all_charuco_corners.append(charuco_corners)
                all_charuco_ids.append(charuco_ids)
                
                if charuco_ids is not None and len(charuco_ids) > 4:
                    cv2.aruco.drawDetectedCornersCharuco(image_copy, charuco_corners, charuco_ids, (255, 0, 0))
                    cv2.imshow('image', image_copy)
                    cv2.waitKey(100)
                    cv2.destroyAllWindows()

    retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_charuco_corners, all_charuco_ids, board, image.shape[:2], None, None)
    
    np.save('rvecs.npy', rvecs)
    np.save('tvecs.npy', tvecs)
    np.save('cam-mat-NYKtest.npy', camera_matrix)
    np.save('dist-coeffs-NYKtest.npy', dist_coeffs)
    
    return all_charuco_corners, all_charuco_ids, camera_matrix, dist_coeffs, board

def calculate_reprojection_error(all_charuco_corners, all_charuco_ids, camera_matrix, dist_coeffs, board, all_rvecs, all_tvecs):
    mean_error = 0
    for i in range(len(all_charuco_corners)):
        charuco_points = all_charuco_corners[i]
        charuco_ids = all_charuco_ids[i]
        obj_points = np.array(board.getObjPoints(), dtype=np.float32).reshape(-1, 3)
        
        imgpoints, _ = cv2.projectPoints(obj_points, all_rvecs[i][0], all_tvecs[i][0], camera_matrix, dist_coeffs)
        corners_2d = all_charuco_corners[i].reshape(-1, 2)
        imgpoints_2d = imgpoints.squeeze()
        
        min_len = min(len(corners_2d), len(imgpoints_2d))
        corners_2d = corners_2d[:min_len]
        imgpoints_2d = imgpoints_2d[:min_len]

        error = cv2.norm(corners_2d, imgpoints_2d, cv2.NORM_L2) / len(corners_2d)
        mean_error += error

    return mean_error / len(all_charuco_corners) if len(all_charuco_corners) > 0 else 0

def detect_pose(image, camera_matrix, dist_coeffs):
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs)
    marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(undistorted_image, dictionary, parameters=params)

    if len(marker_ids) > 0:
        retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, undistorted_image, board)
        
        if retval:
            success, rvec, tvec = cv2.aruco.estimatePoseCharucoBoard(charuco_corners, charuco_ids, board, camera_matrix, dist_coeffs)
            
            if success:
                cv2.drawFrameAxes(undistorted_image, camera_matrix, dist_coeffs, rvec, tvec, length=0.1, thickness=15)

    return undistorted_image

def main():
    camera_matrix = np.load('cam-mat-NYKtest.npy')
    dist_coeffs = np.load('dist-coeffs-NYKtest.npy')
    
    image_files = [os.path.join(PATH_TO_YOUR_IMAGES, f) for f in os.listdir(PATH_TO_YOUR_IMAGES) if f.endswith(".jpeg")]
    image_files.sort()

    for image_file in image_files:
        image = cv2.imread(image_file)
        pose_image = detect_pose(image, camera_matrix, dist_coeffs)
        cv2.imshow('Pose Image', pose_image)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    all_charuco_corners, all_charuco_ids, camera_matrix, dist_coeffs, board = calibrate_and_save_parameters()
    reprojection_error = calculate_reprojection_error(all_charuco_corners, all_charuco_ids, camera_matrix, dist_coeffs, board, all_rvecs, all_tvecs)
    print("Reprojection error: ", reprojection_error)
