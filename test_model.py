from ultralytics import YOLO


model = YOLO('best.pt')

results1 = model.predict(
    source='img_1.png',
    save=True
)