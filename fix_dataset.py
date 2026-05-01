import cv2
import os

db_path = "dataset"

print(f"Enhancing images in {db_path}...")

for person in os.listdir(db_path):
    person_dir = os.path.join(db_path, person)
    if not os.path.isdir(person_dir):
        continue

    for file in os.listdir(person_dir):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(person_dir, file)
            img = cv2.imread(img_path)
            if img is None:
                continue

            # Enhance brightness/contrast using CLAHE on LAB color space
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)

            # Apply CLAHE to L (lightness) channel
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l_enhanced = clahe.apply(l)

            # Merge back and convert to BGR
            img_enhanced = cv2.merge([l_enhanced, a, b])
            img_enhanced = cv2.cvtColor(img_enhanced, cv2.COLOR_LAB2BGR)

            cv2.imwrite(img_path, img_enhanced)
            print(f"  Enhanced: {img_path}")

print("\nDone! All images have been brightened.")
