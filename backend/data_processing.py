'''
process livefeed data from webcam 

1) preprocess data to eliminate noise 
2) face recognitiion 
    i) if face detected within radius -> run similarity check against existing profiles, 
        run live audio processing, send to LLM for summarization, store
        summarization and time in DB (nurse, parents, etc.)
3) Live video feed processing
    i) capture video feed in frames only when significant scene change
    -> send to LLM for summarization
        -> store summarization and time in DB
    ii) have temporary current relevant conversation recording (for the individual to 
    query their current conversation, indicate redundancy )
4) Data handling and storage
    i) thorughout the day scenes and events summarized
    ii) temporary current relevant conversation recording 
    iii) summarized audio data associated with relevant profile
    iv) facial profiles 
'''
import collections
from typing import Optional

import cv2
import numpy as np


def preprocess_frame(frame):
    """preprocess video frame to reduce noise and normalize to grayscale"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    equalized = cv2.equalizeHist(denoised)
    processed_bgr = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
    return processed_bgr, equalized

#class to keep previous frame states and used to detect significant scene change
class SceneChangeDetector:
    """Detects meaningful scene changes by tracking large pixel-area shifts."""

    # tune intensity_threshold, change_ratio, and smoothing for sensitivity
    def __init__(
        self,
        intensity_threshold: float = 35.0,
        change_ratio: float = 0.25,
        smoothing: int = 5,
    ):
        self.intensity_threshold = intensity_threshold
        self.change_ratio = change_ratio
        self.smoothing = max(smoothing, 1)
        self.previous_frame: Optional[np.ndarray] = None
        self._recent_ratios = collections.deque(maxlen=self.smoothing)

    def detect(self, frame: np.ndarray, gray: np.ndarray) -> bool:
        if self.previous_frame is None:
            self.previous_frame = gray
            return False

        # dynamically compare the difference between previous frame, current frame, and 
        #update metrics  
        difference = cv2.absdiff(self.previous_frame, gray)
        _, mask = cv2.threshold(
            difference,
            self.intensity_threshold,
            255,
            cv2.THRESH_BINARY,
        )

        kernel = np.ones((3, 3), np.uint8)
        cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        changed_pixels = float(np.count_nonzero(cleaned_mask))
        total_pixels = float(cleaned_mask.size)

        #if the average ratio of the current frame is greater than the
        #threshold than return True, indicating a significant scene change
        ratio = changed_pixels / total_pixels if total_pixels else 0.0

        self.previous_frame = gray
        self._recent_ratios.append(ratio)
        averaged_ratio = float(np.mean(self._recent_ratios))
        return averaged_ratio > self.change_ratio


# constantly running and processing live webcam feed
def webcam_processing():
    # change the indice to the webcam index
    cap = cv2.VideoCapture(0)
    scene_detector = SceneChangeDetector()
    # reads frames from webcam and projects
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # preprocess live video feed
        frame, gray = preprocess_frame(frame)

        cv2.imshow("BRIO feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # only record frames when significant scene change is detected
        if scene_detector.detect(frame, gray):
            record_frame(frame)

        # if familiar face detected, run the facial recognition process and record conversation
        if face_detected(frame):
            process_face(frame)
        else:
            continue

#facial similarity check
def face_detected(frame):
    #detect face in frame using deepface library
    #compare with similarity from database recorded facial profiles
    pass
#run live audio processing, send to LLM for summarization, process text, store
def process_face(frame):
    #process face in frame
    pass


def record_frame(frame):
    #record frame to database
    pass


def main():
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            cap.release()
    #webcam_processing()

if __name__ == "__main__":
    main()