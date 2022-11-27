# import cv2
# import numpy as np
# import os
# os.getcwd()

# ECCV16_MoDEL = 'deep_learning/models'
# IMG_PATH = 'deep_learning/imgs'
# SAVE_PATH = 'deep_learning/Newimgs'
# INSTANCE_MODEL = 'deep_learning/models/instance_norm'

# net = cv2.dnn.readNetFromTorch(ECCV16_MoDEL +'/la_muse.t7')

# img = cv2.imread(IMG_PATH + '/02.jpg')

# h, w, c = img.shape

# print(img.shape)

# img = cv2.resize(img, dsize=(500, int(h / w * 500)))

# #img = img[162:513, 185:428] #액자 부분 자르기.

# MEAN_VALUE = [103.939, 116.779, 123.680]
# blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)

# print(blob.shape)

# net.setInput(blob)
# output = net.forward()

# output = output.squeeze().transpose((1, 2, 0))
# output += MEAN_VALUE

# output = np.clip(output, 0, 255)
# output = output.astype('uint8')


# cv2.imshow('output', output)
# cv2.imwrite(SAVE_PATH + '/newimg.jpg', output)
# #cv2.imwrite('C:/Users/MIT/Desktop/sparta_deep/week2/madeimgs', output)
# #cv2.imshow('img', img)
# cv2.waitKey(0)

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# import os
# import random

# net_list = [
#     "starry_night.t7",
#     "la_muse.t7",
#     "the_wave.t7",
#     "composition_vii.t7",
#     "feathers.t7",
#     "mosaic.t7",
#     "the_scream.t7",
#     "composition_vii.t7"
# ]
# n = len(net_list)
# rand_num = random.randint(0,n-1)
# net = cv2.dnn.readNetFromTorch(f'models/{net_list[rand_num]}')
# img = cv2.imread(f'../media/uploads/input.jpg')

# h, w, c = img.shape
# img = cv2.resize(img, dsize=(500, int(h / w * 500)))

# MEAN_VALUE = [103.939, 116.779, 123.680]
# blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)

# net.setInput(blob)
# output = net.forward()

# output = output.squeeze().transpose((1, 2, 0))
# output += MEAN_VALUE

# output = np.clip(output, 0, 255)
# output = output.astype('uint8')

# cv2.imwrite('../media/uploads/result.jpeg', output)

# # cv2.waitKey(0)


## 딥러닝 구현 중 팀원 구현 성공으로 중단.