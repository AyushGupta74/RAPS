from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="./configs/traffic.yaml",
    epochs=20,
    imgsz=320,
    batch=-2,
    workers=4,
    device=0,
    persist = True,
    project="./outputs",
    name="yolo_vehicle"
)
