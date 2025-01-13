from ultralytics import YOLO


model = YOLO('/Users/petrlutkin/Desktop/MushroomDetection/result/train2/weights/best.pt')

results1 = model.predict(
    source='img_3.png',
    save=True
)