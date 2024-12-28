# FSOCO Object Detection
_Instructions for setting up FSOCO dataset to train the YOLO model for cone detection using the [Ultralytics](https://docs.ultralytics.com) library._

## Installation
_Step-by-step instructions to install the project locally._

1. Clone the repository:  
   ```bash
   git clone https://github.com/T0mLam/fsoco_object_detection.git
   cd fsoco_object_detection
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Download the FSOCO (Bounding Boxes) dataset from [FSOCO](https://www.fsoco-dataset.com/download) and save the folder `fsoco_bounding_boxes_train` in the root directory.

    ```
    fsoco_object_detection
    ├───fsoco_bounding_boxes_train
    │   ├───ampera
    │   │   ├───ann
    │   │   └───img
    │   ├───amz
    │   │   ├───ann
    │   │   └───img
    │   ...
    ├───yolov11n_640
    ├───yolov11s_1024
    │
    ...
    ```
   

## Usage  
_Set up the directory for training the YOLO models with the FSOCO dataset using Ultralytics._

1. Reallocate the images in the form of
    ```
    dataset/
    ├── images/
    │   ├── train/
    │   ├── val/
    │   └── test/
    └── labels/
        ├── train/
        ├── val/
        └── test/
    ```  
    by running the command
    ```bash
    python organize_dataset.py 
    ```  
    Notes: </br>
    You can change the settings in `organize_dataset.py`
    ```python
    SOURCE_DIR = "fsoco_bounding_boxes_train"
    TARGET_DIR = "dataset"
    TRAIN_SPLIT = 0.8
    VAL_SPLIT = 0.1 
    # Randomly shuffle and split the dataset
    # Remaining 0.1 for testing
    ```


2. Creating custom training labels for each image by converting JSON files into TXT format. </br>
    Original:
    ```
    {
        "description": "",
        "tags": [
            {
                "id": 118613237,
                "tagId": 30143178,
                "name": "train",
                "value": null,
                "labelerLogin": "fsocov2",
                "createdAt": "2020-06-04T10:03:32.322Z",
                "updatedAt": "2020-06-04T10:03:32.322Z"
            }
        ],
        "size": {
            "height": 1480,
            "width": 1880
        },
        "objects": [
            {
                "id": 889945915,
                "classId": 9993511,
                "description": "",
                "geometryType": "rectangle",
                "labelerLogin": "fsocov2",
                "createdAt": "2020-06-04T10:03:32.324Z",
                "updatedAt": "2020-06-04T10:03:32.324Z",
                "tags": [],
                "classTitle": "blue_cone",
                "points": {
                    "exterior": [
                        [
                            641,
                            895
                        ],
                        [
                            688,
                            957
                        ]
                    ],
                    "interior": []
                }
            },
        ...
        ]
    }
    ```
    Converted:
    ```
    # class x_center y_center width height 
    # (of each bounding box in the image) 
    1 0.353457 0.625676 0.025000 0.041892
    1 0.390957 0.598649 0.017021 0.029730
    1 0.413032 0.583446 0.012234 0.022297
    ...
    ```
    __Run the command__
    ```bash
    python bbox_converter <dataset_dir> data.yaml
    ```
    It should create a txt file for each json annotation file.
    ```
    dataset/
    ├── images/
    │   ├── train/
    │   │   ├── ecurieaix_00109.png
    │   │   ├── ...
    │   ├── val/
    │   └── test/
    └── labels/
        ├── train/
        │   ├── ecurieaix_00109.png.json
        │   ├── ecurieaix_00109.txt
        │   ├── ... 
        ├── val/
        └── test/
    ```

3. Train the model with Ultralytics YOLO models:  
    - Configure the `train.py` file
        ```python
        from ultralytics import YOLO

        def main():
            model = YOLO("yolo11s.pt")  
            results = model.train(
                data="data.yaml", 
                epochs=100, 
                imgsz=1024, 
                device=0, # use gpu
                batch=-1,
                plots=True
            )

        if __name__ == '__main__':
            main()
        ```
    - Run the command
        ```bash
        python train.py
        ```
        or use cli commands provided by ultralytics, e.g.
        ```bash
        yolo detect train data=data.yaml model=yolo11s.pt epochs=100 imgsz=640 device=0
        ```

4. Test the trained model with the test dataset </br>
    e.g.
    using the trained yolo11n model with reshaped image size of <?>x640.
    ```bash
    yolo task=detect mode=predict model=yolov11n_640/weights/best.pt source=dataset/images/test save=True device=0
    ```

## TODO

- fine tune the model
- run object detection on videos
- make sure the model is quick enough for real-time inference
- btw how to integrate the model into euf-sim?
