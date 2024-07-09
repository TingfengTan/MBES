from ReadDat import readdat
from SaveExcel import SaveExcel

Dat = readdat('./data.dat')
Dat.read()
Dat.close()
# save = SaveExcel(Dat=Dat)
# save.save()
# import numpy as np
# num = len(Dat.AllDepth)
# data = np.zeros((num,512))
# for i in range(num):
#     data[i,:] = Dat.AllDepth[i]['data'][:,0]

# result = np.zeros_like(data)

# result = data*(1497/78125)/2

# y = np.linspace(-10,10,248)
# x = np.linspace(0,50,512)
# x, y = np.meshgrid(x,y)
# import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = fig.add_subplot(111,projection='3d')
# ax.plot_surface(x,y,result)
# plt.show()



