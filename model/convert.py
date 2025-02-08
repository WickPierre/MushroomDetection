from ultralytics import YOLO


model = YOLO('/Users/petrlutkin/Desktop/MushroomDetection/result/train2/weights/best.pt')


model.export(format="tflite")