import cv2
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolov11n_640x640/weights/best.pt")  
    results = model.predict("C:/Users/admin/Desktop/FSAI/fsoco/object_detection/dataset/images/test/amz_00225.png")

    # Visualize the detection
    img = results[0].plot()  # This plots the detections on the image

    cv2.imwrite('output_detection.png', img)