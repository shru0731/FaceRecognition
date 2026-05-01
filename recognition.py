import os
import time

import cv2
from deepface import DeepFace

DB_PATH = "dataset"
WINDOW_NAME = "Recognition"
DISPLAY_MODE = os.environ.get("RECOGNITION_DISPLAY", "auto").strip().lower()
STATUS_EVERY_SECONDS = 5


def dataset_ready(db_path):
    return os.path.exists(db_path) and len(os.listdir(db_path)) > 0


def display_requested():
    return DISPLAY_MODE in {"1", "true", "yes", "gui", "window"}


def display_disabled():
    return DISPLAY_MODE in {"0", "false", "no", "headless", "console"}


def can_use_imshow():
    if display_disabled():
        return False

    test_frame = None
    try:
        test_frame = cv2.UMat(1, 1, cv2.CV_8UC3)
        cv2.imshow(WINDOW_NAME, test_frame)
        cv2.waitKey(1)
        cv2.destroyWindow(WINDOW_NAME)
        return True
    except cv2.error:
        if display_requested():
            print("Display requested, but this OpenCV build has no GUI support.")
        return False


def main():
    if not dataset_ready(DB_PATH):
        print("No dataset found! Run capture.py and train.py first.")
        raise SystemExit(1)

    use_display = can_use_imshow()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open camera 0.")
        raise SystemExit(1)

    if use_display:
        print("Starting recognition. Press 'q' to quit.")
    else:
        print("Starting recognition in headless mode.")
        print("OpenCV was installed without GUI support, so frames will not be shown.")
        print("Set RECOGNITION_DISPLAY=window after installing GUI-enabled OpenCV if you want a preview window.")
        print("Press Ctrl+C to quit.")

    last_status_at = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Camera frame read failed.")
                break

            match_name = None

            try:
                results = DeepFace.find(
                    img_path=frame,
                    db_path=DB_PATH,
                    model_name="ArcFace",
                    detector_backend="opencv",
                    enforce_detection=False,
                    silent=True,
                )

                if len(results) > 0 and not results[0].empty:
                    match = results[0].iloc[0]
                    match_name = os.path.basename(os.path.dirname(match["identity"]))

                    x = int(match["source_x"])
                    y = int(match["source_y"])
                    w = int(match["source_w"])
                    h = int(match["source_h"])

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        match_name,
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 0),
                        2,
                    )
            except KeyboardInterrupt:
                raise
            except Exception:
                pass

            if use_display:
                cv2.imshow(WINDOW_NAME, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                now = time.time()
                if match_name:
                    print(f"Match: {match_name}")
                elif now - last_status_at >= STATUS_EVERY_SECONDS:
                    print("Running... no match detected")
                    last_status_at = now
    except KeyboardInterrupt:
        print("\nStopping recognition.")
    finally:
        cap.release()
        if use_display:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
