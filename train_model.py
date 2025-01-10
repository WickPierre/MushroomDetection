from ultralytics import YOLO

# Загружаем предобученную модель YOLOv11
model = YOLO('yolo11n-cls.pt')  # Выберите размер модели: n, s, m, l, x

# Запускаем обучение
model.train(
    data='/Users/petrlutkin/Desktop/MushroomDetection/dataset/',
    epochs=20,
    imgsz=520,
    device='mps',
    save_dir='/Users/petrlutkin/Desktop/MushroomDetection/result',
)