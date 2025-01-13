from ultralytics import YOLO

# Загружаем предобученную модель YOLOv11
model = YOLO('yolo11n-cls.pt')  # Выберите размер модели: n, s, m, l, x

# Запускаем обучение
model.train(
    data='/Users/petrlutkin/Desktop/MushroomDetection/dataset_new/',
    epochs=20,
    imgsz=512,
    batch=32,
    device='mps',
    project='/Users/petrlutkin/Desktop/MushroomDetection/result'
)
