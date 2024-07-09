import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file_path = './data/AllWater_Data.npz'
data = np.load(file_path)
data_list = list(data.files)
Arr = []
for i, arr in enumerate(data_list):
    print(f'{i}:{data[arr].shape}:{data[arr].max()}')
    Arr.append(data[arr])

test = np.zeros((256,7540),dtype=np.uint16)
for i in range(10):
    test[:,754*i:754*(i+1)] = Arr[i+1]

plt.figure(1)
plt.imshow(test)
plt.savefig('test.png')
plt.show()

import cv2
img = np.clip(test, 0, 255)
img = img.astype(np.uint8) 
# img = cv2.convertScaleAbs(test,alpha=255/test.max())
cv2.imwrite('img.png',img)


# y = np.linspace(-30,30,256)
# x = np.linspace(0,50,75400)
# x,y = np.meshgrid(x,y)


# 创建一个新的图形窗口
# fig = plt.figure()

# 创建一个3D坐标轴
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(x,y,test)
# ax = fig.add_subplot(222, projection='3d')
# ax.plot_surface(x,y,data['arr_23'],cmap='magma')
# ax = fig.add_subplot(223, projection='3d')
# ax.plot_surface(x,y,data['arr_24'],cmap='magma')
# ax = fig.add_subplot(224, projection='3d')
# ax.plot_surface(x,y,data['arr_25'],cmap='magma')

# plt.show()