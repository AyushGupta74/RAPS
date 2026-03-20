
# Traffic Density Detection using YOLOv8

This project focuses on **traffic density detection at road intersections** using a fine-tuned **YOLOv8 object detection model**. The system detects vehicles such as cars and buses from traffic camera feeds and forms the foundation for downstream tasks like traffic density estimation, prediction, and routing optimization.



## 1. Project Objectives

- Detect traffic participants (cars, buses, etc.) from images and videos
- Fine-tune a YOLOv8 model on traffic surveillance datasets
- Prepare a pipeline for real-time and periodic traffic density estimation
- Enable structured outputs (CSV) for further time-series analysis


## 2. Tech Stack

- **Python 3.9+**
- **YOLOv8 (Ultralytics)**
- OpenCV
- NumPy, Pandas
- PyTorch



## 3. Dataset Used

### DETRAC Dataset
The project uses the **DETRAC traffic surveillance dataset**, which contains annotated images captured from fixed traffic cameras.

Dataset components:
- Traffic intersection images
- XML-based bounding box annotations
- Multiple vehicle categories

### Dataset Structure (Original)

```

DETRAC-Images/
DETRAC-MOT-toolkit/
DETRAC-Test-Annotations-XML/
DETRAC-Train-Annotations-XML/

```

> Note: Raw datasets are excluded from version control and must be downloaded separately.


## 4. Dataset Preprocessing

### 4.1 Annotation Conversion

- Original annotations are in **XML format**
- Converted to **YOLO format**:
```

<class_id> <x_center> <y_center> <width> <height>

```
- Coordinates are normalized between 0 and 1

### 4.2 Train / Validation Split

The dataset is split into:
- **Train**
- **Validation**

Resulting directory structure:

```

data/
└── raw
    ├── images/
    ├── labels/
└── processed
    ├── images/
    │   ├── train/
    │   └── val/
    ├── labels/
    │   ├── train/
    │   └── val/

````


## 5. Class Labels

The model is trained on the following vehicle classes:

| Class ID | Label |
|--------|-------|
| 0 | Car and others |
| 1 | Bus |
| 2 | Truck |



## 6. YOLOv8 Installation

Install dependencies:

```bash
pip install ultralytics opencv-python numpy pandas
````

Verify installation:

```bash
yolo --version
```


## 7. YOLOv8 Configuration

Create a dataset configuration file `traffic.yaml`:

```yaml
path: datasets/traffic
train: images/train
val: images/val

names:
  0: car
  1: bus
  2: truck
```


## 8. Model Training

YOLOv8 is fine-tuned using a pretrained model as the base.

### Training Command

```bash
    data="traffic_density_project/configs/traffic.yaml",
    epochs=5,
    imgsz=320,
    batch=-1,
    device="cpu",
    device=0,               
    workers=8, # for your cpu
    project="outputs",
    name="yolo_tuned"
```

### Training Outputs

After training, YOLO generates:

* Trained weights (`best.pt`, `last.pt`)
* Loss curves and metrics
* Validation predictions

These are stored under:

```
runs/detect/train/
```


## 9. Current Status

* Dataset preprocessing completed
* YOLOv8 model successfully trained
* Model validated on traffic images


## 10. Next Steps

* Generate CSV-based traffic density logs
* Integrate time-series prediction models (EWMA / LSTM)
* Enable real-time intersection-level monitoring


## 11. Notes

* Large files (datasets, weights, videos) are ignored via `.gitignore`
* Training can be scaled using larger YOLO variants (YOLOv8s/m/l)
