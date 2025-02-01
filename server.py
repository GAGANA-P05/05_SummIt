import cv2
import threading

# Global flag to control the loop
video_running = True

# Define the function to stop the video feed
def stop_video():
    global video_running
    video_running = False

def display_video():
    global video_running
    # Initialize the webcam (default camera)
    cap = cv2.VideoCapture(0)  # 0 for default camera

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    while video_running:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from the camera.")
            break

        # Resize frame for consistency (optional)
        resized_frame = cv2.resize(frame, (800, 700))

        # Display the frame in an OpenCV window
        cv2.imshow('Video Capture', resized_frame)

        # Save the entire frame (without any rectangles or predictions)
        cv2.imwrite("full_frame_live.png", resized_frame)

        # Exit the loop and stop the video capture when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Video stream stopped by key press.")
            break

    # Release the capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Create a thread to run the display_video function
video_thread = threading.Thread(target=display_video)
video_thread.start()

# Example of how you can stop the video feed from another part of the program
# Call stop_video() to stop the video feed programmatically
# For example, you can add some condition or delay here to stop it after a certain time
import time
time.sleep(10)  # Let the video run for 5 seconds
stop_video()  # This will stop the video feed
video_thread.join()  # Wait for the video thread to finish
