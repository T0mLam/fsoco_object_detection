from ultralytics import YOLO

def main():
    model = YOLO("yolo11s.pt")  
    results = model.train(
        data="data.yaml", 
        epochs=100, 
        imgsz=1024, 
        device=0, 
        batch=-1,
        plots=True
    )

if __name__ == '__main__':
    main()