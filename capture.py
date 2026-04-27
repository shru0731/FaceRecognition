'''import cv2
import os

name = input("Enter the person's name: ")
path = f"dataset/{name}"
os.makedirs(path, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

while count < 5:  # Takes 5 photos
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break
        
    cv2.imshow("Capturing - Press Space", frame)
    
    if cv2.waitKey(1) & 0xFF == ord(' '):
        img_name = f"{path}/{name}_{count}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"Saved: {img_name}")
        count += 1
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()'''
import cv2
import os

name = input("Enter the person's name: ")
path = f"dataset/{name}"
os.makedirs(path, exist_ok=True)

cap = cv2.VideoCapture(0)

# Check if camera opened
if not cap.isOpened():
    print("Error: Cannot access camera")
    exit()

count = 0

while count < 5:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break
        
    cv2.imshow("Capturing - Press Space", frame)

    key = cv2.waitKey(1) & 0xFF   # ✅ read key only once

    if key == ord(' '):  # Space key
        img_name = f"{path}/{name}_{count}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"Saved: {img_name}")
        count += 1

    elif key == ord('q'):  # Quit
        break

cap.release()
cv2.destroyAllWindows()