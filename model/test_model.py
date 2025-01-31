from ultralytics import YOLO

model = YOLO('/result/train2/weights/best.pt')

model.predict(
    '../dataset/train/amanita_rubescens/635_amanita_rubescens.jpeg',
imgsz=640
)