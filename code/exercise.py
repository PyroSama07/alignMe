import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def curl(results,counter,stage):
    landmarks = results.pose_landmarks.landmark

    # Get coordinates
    shoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
    
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]
    
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z]

    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y,
           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z]

    # Calculate angle
    angle = calculate_angle(shoulder, elbow, wrist)
    temp_angle = calculate_angle(shoulder,elbow,hip)
        
    if temp_angle >160 or temp_angle < 15:
        if angle > 140:
            stage = "down"
        if angle < 40 and stage =='down':
            stage="up"
            counter +=1
        return True,counter,stage
    return False,counter,"Wrong"

def push_up(results,counter,stage):
    landmarks = results.pose_landmarks.landmark

    # Get coordinates
    shoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]
    
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z]
    
    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
             landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
             landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z]

    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y,
           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z]
    
    knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].z]
    
    # Calculate angle
    angle = calculate_angle(shoulder, elbow, wrist)
    temp_angle = calculate_angle(shoulder,hip,knee)
    
    if temp_angle >165 or temp_angle < 15:
        if angle > 160 or angle < 10:
            stage = "up"
        if angle < 130 and angle > 10 and stage =='up':
            stage="down"
            counter +=1
        return True,counter,stage
    return False,counter,"Wrong"
