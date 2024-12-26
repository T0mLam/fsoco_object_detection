import os
import shutil
import random
from tqdm import tqdm


SOURCE_DIR = "fsoco_bounding_boxes_train"
TARGET_DIR = "dataset"
TRAIN_SPLIT = 0.8
VAL_SPLIT = 0.1 # Remaining 0.1 for testing


# Create target directories

# dataset/
# ├── images/
# │   ├── train/
# |   ├── val/
# │   └── test/
# └── labels/
#     ├── train/
#     ├── val/
#     └── test/

os.makedirs(os.path.join(TARGET_DIR, "images", "train"), exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "images", "val"), exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "images", "test"), exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "labels", "train"), exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "labels", "val"), exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "labels", "test"), exist_ok=True)


# Collect paths to all images and labels
images = []
annotations = []

for root, _, files in os.walk(SOURCE_DIR):
    for file in files:
        # Add all png file paths to the images list
        if file.endswith((".png", ".jpg")):
            images.append(os.path.join(root, file))

        # Add all json file paths to the annotations list
        elif file.endswith(".json") and file != "meta.json":
            annotations.append(os.path.join(root, file))


# Check if the number of images and annotations match
print(f"Found {len(images)} images and {len(annotations)} annotations.")
assert len(images) == len(annotations), "Number of images and annotations do not match."


# Group and shuffle the images and annotations together
# data: [(image_path, annotation_path)]
images.sort()
annotations.sort()
data = list(zip(images, annotations))
random.shuffle(data)


# Split the data into train, val, and test sets based on the defined split ratios
train_split = int(len(data) * TRAIN_SPLIT)
val_split = int(len(data) * VAL_SPLIT)
test_split = int(len(data) * 1 - TRAIN_SPLIT - VAL_SPLIT)

train_data = data[:train_split] # 0 to train_split
val_data = data[train_split: train_split + val_split]  # train_split to train_split + val_split
test_data = data[train_split + val_split:] # train_split + val_split to end


# Copy the data to the target directories
def copy_data(data, label_dir):
    for image_path, annotation_path in tqdm(data, desc=f"Copying {label_dir} data"):
        # Get the image and annotation file names from the file paths
        image_name = os.path.basename(image_path)
        annotation_name = os.path.basename(annotation_path)

        # Copy the image and annotation files to the target directory
        shutil.copy(image_path, os.path.join(TARGET_DIR, "images", label_dir, image_name))
        shutil.copy(annotation_path, os.path.join(TARGET_DIR, "labels", label_dir, annotation_name))

copy_data(train_data, "train")
copy_data(val_data, "val")
copy_data(test_data, "test")


# Done
print("All files are copied successfully. :)")