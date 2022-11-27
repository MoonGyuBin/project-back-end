import datetime
import time
import cv2
import numpy as np
from datetime import datetime
import random


def transform_img(model, image):

    input_img = cv2.imread(f"media/{image}")

    models = cv2.dnn.readNetFromTorch(f"post/models/{model}")

    h, w, c = input_img.shape
    input_img = cv2.resize(input_img, dsize=(500, int(h / w * 500)))
    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(input_img, mean=MEAN_VALUE)
    models.setInput(blob)
    output_img = models.forward()
    output_img = output_img.squeeze().transpose((1, 2, 0))
    output_img += MEAN_VALUE
    output_img = np.clip(output_img, 0, 255)
    output_img = output_img.astype('uint8')

    # days = datetime.now()
    # num = random.randrange(1, 100)

    # now = datetime.now()
    # times = now.microsecond
    
    ts = time.time()
    time_str = datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')

    cv2.imwrite(f'media/result/pictures{time_str}.jpg', output_img)
    transform = f"media/result/pictures{time_str}.jpg"

    return transform

# 1. opencv
