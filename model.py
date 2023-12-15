import os
from ultralytics import YOLO

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# # Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# # Use the model
if __name__ == "__main__":
    model.train(data="C:/Users/HP/Desktop/test2/data_custom.yaml", epochs=100)  # train the model
# metrics = model.val()  # evaluate model performance on the validation set

# model.predict(source='이미지경로', save=True)