import cv2
import numpy as np
from datetime import datetime


def transform_img(model, image):

    input_img = cv2.imread(f"media/2022/11/{image}")
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

    datetimes = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(datetimes)
    cv2.imwrite(f"post/pictures{datetimes}.jpg", output_img)
    transform = f"pictures{datetimes}.jpg"
    print(transform)

    return transform


# a = image("instance_norm/...t7", "입력 사진")
# a = image("eccv16/...t7", "입력 사진")

# userimage = transform_img("instance_norm/mosaic.t7", "post/02.jpg")
# print(userimage)
