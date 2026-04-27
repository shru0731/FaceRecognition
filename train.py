import os
import pickle

import numpy as np
from deepface import DeepFace

DATASET_PATH = os.environ.get("DATASET_PATH_PI3", "dataset")
OUTPUT_PATH = os.environ.get("EMBEDDINGS_PATH_PI3", "representations_pi3.pkl")
MODEL_NAME = os.environ.get("MODEL_NAME_PI3", "Facenet")
DETECTOR_BACKEND = os.environ.get("DETECTOR_BACKEND_PI3", "opencv")
DISTANCE_METRIC = os.environ.get("DISTANCE_METRIC_PI3", "cosine")
ALIGN = os.environ.get("ALIGN_PI3", "true").strip().lower() not in {"0", "false", "no"}
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")


def iter_dataset_images(dataset_path):
    for person_name in sorted(os.listdir(dataset_path)):
        person_dir = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_dir) or person_name.startswith("ds_model"):
            continue

        image_paths = []
        for file_name in sorted(os.listdir(person_dir)):
            if file_name.lower().endswith(VALID_EXTENSIONS):
                image_paths.append(os.path.join(person_dir, file_name))

        if image_paths:
            yield person_name, image_paths


def normalize_embedding(embedding):
    vector = np.array(embedding, dtype=np.float32)
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def main():
    if not os.path.isdir(DATASET_PATH):
        print(f"Dataset folder not found: {DATASET_PATH}")
        raise SystemExit(1)

    print("Training Pi3 face embeddings...")
    print(f"Dataset:  {DATASET_PATH}")
    print(f"Output:   {OUTPUT_PATH}")
    print(f"Model:    {MODEL_NAME}")
    print(f"Detector: {DETECTOR_BACKEND}")
    print(f"Align:    {ALIGN}")

    embeddings = {}
    total_images = 0
    used_images = 0

    for person_name, image_paths in iter_dataset_images(DATASET_PATH):
        print(f"\nProcessing {person_name}...")
        person_embeddings = []

        for image_path in image_paths:
            total_images += 1
            file_name = os.path.basename(image_path)

            try:
                embedding_obj = DeepFace.represent(
                    img_path=image_path,
                    model_name=MODEL_NAME,
                    detector_backend=DETECTOR_BACKEND,
                    align=ALIGN,
                    enforce_detection=False,
                )
            except Exception as exc:
                print(f"  SKIP {file_name}: {exc}")
                continue

            if not embedding_obj:
                print(f"  SKIP {file_name}: no embedding generated")
                continue

            vector = normalize_embedding(embedding_obj[0]["embedding"])
            person_embeddings.append(vector.tolist())
            used_images += 1
            print(f"  OK  {file_name}")

        if person_embeddings:
            embeddings[person_name] = person_embeddings

    if not embeddings:
        print("No embeddings were generated. Check the dataset images.")
        raise SystemExit(1)

    payload = {
        "model_name": MODEL_NAME,
        "detector_backend": DETECTOR_BACKEND,
        "distance_metric": DISTANCE_METRIC,
        "align": ALIGN,
        "embeddings": embeddings,
    }

    with open(OUTPUT_PATH, "wb") as file:
        pickle.dump(payload, file, pickle.HIGHEST_PROTOCOL)

    print("\nTraining complete.")
    print(f"Used {used_images} / {total_images} images")
    print(f"Saved embeddings: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()