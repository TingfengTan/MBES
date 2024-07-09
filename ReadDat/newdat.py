import numpy as np
import struct


old_data = open('./data.dat','rb')
new_data = open('./data1.dat','wb')
# file header
data = old_data.read(16)
new_data.write(data)

_ = old_data.read(12*(24+27))

while True:
    tmp = old_data.read(24)
    _ = old_data.read(6)
    data = _
    while _.decode()!= '\n':
        _ = old_data.read(1)
        data = data + _
    if data[:6].decode() == '$GPGGA':
        print('GPGGA')
        new_data.write(tmp)
        new_data.write(data)
        break
while True:
    data = old_data.read(1)
    if not data:
        break
    else:
        new_data.write(data)



old_data.close()
new_data.close()