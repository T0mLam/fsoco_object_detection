import os
from ultralytics import YOLO

def main():
    model = YOLO("yolov11n_640/weights/best.pt") 

    for root, dirs, files in os.walk("example_images"):
        for f in files:
            image_path = os.path.join(root, f)
            model.predict(image_path, save=True)

if __name__ == '__main__':
    main()