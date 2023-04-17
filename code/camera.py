import cv2
import mediapipe as mp
import numpy as np
import exercise
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def start_camera(selected_exercise):
    try:
        selected_exercise = getattr(exercise,selected_exercise)
    except:
        return 0
    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0 
    stage = None
    correct = False

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
#                 print('try')
                correct,counter,stage = selected_exercise(results,counter,stage)
            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, 
                                                           circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, 
                                                           circle_radius=2) 
                                     )    
            # Render curl counter
            # Setup status box
            image=cv2.flip(image,1)
            if correct:
                cv2.rectangle(image, (0,0), (225,73), (0,255,0), -1)
            else:
                cv2.rectangle(image, (0,0), (250,78), (0,0,255), -1)  

            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)


            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return counter


if __name__ == "__main__":
    start_camera(input("Enter Exercise: "))
