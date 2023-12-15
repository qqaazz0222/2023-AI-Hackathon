from ultralytics import YOLO

model = YOLO('yolov8m.pt')
model = YOLO('./runs/detect/train15/weights/best.pt')

# results = model.val(device='cpu')
results = model('./test/images/E63_DATA1_T1_L4_D2023-09-26-09-11_042_000840.jpg', save=True)