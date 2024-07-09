import numpy as np
import struct
import pynmea2
class readdat():
    def __init__(self,path) -> None:
        self.datpath = path
        self.f = open(self.datpath,'rb')
        self.VER = self.f.read(16)  # 数据版本（只在每个数据文件开头标注）共16字节
        self.MRU = []
        self.GPS = []
        self.Water = {}
        self.Depth = {}
        self.AllWater = []
        self.AllDepth = []
        self.size = []
    
    def readMRU(self):
        tmp = self.f.read(27)
        print('MRU Data\n')
        print(tmp.decode())
        self.MRU.append(tmp.decode())
        # print(self.time_stamp_recv)
    def readGPS(self):
        # tmp = self.f.read(6)
        # if tmp.decode() == '$GPHDT':
        #     _ = self.f.read(7)
        #     self.GPS.append(tmp.decode()+_.decode())
        # elif tmp.decode() == '$GPVTG':
        #     _ = self.f.read(39)
        #     self.GPS.append(tmp.decode()+_.decode())
        # elif tmp.decode() == '$GPZDA':
        #     _ = self.f.read(32)
        #     self.GPS.append(tmp.decode()+_.decode())
        # elif tmp.decode() == '$GPGGA':
        #     _ = self.f.read(86)
        #     self.GPS.append(tmp.decode()+_.decode())
        tmp = self.f.read(6)
        print(tmp)
        data = tmp.decode()
        while tmp.decode() != '\n':
            tmp = self.f.read(1)
            data = data + tmp.decode()
        self.GPS.append(data)
        if data[:6] == '$GPGGA':
            print('GPGGA\n')
            print(data)
        tmp = pynmea2.parse(data[:-2])
        # print(self.time_stamp_recv)

    def readWater(self):
        self.Water['preamble'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['type'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['size'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['version'] = int.from_bytes(self.f.read(4),byteorder='little')
        _ = self.f.read(4)
        self.Water['crc'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['snd_velocity'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['sample_rate'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['N'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['M'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['Time'] = struct.unpack('2f',self.f.read(8))[0]
        self.Water['dtype'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['t0'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['gain'] = struct.unpack('f',self.f.read(4))[0]
        _ = self.f.read(4)
        self.Water['swath_dir'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['swath_open'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['tx_freq'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['tx_bw'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['tx_len'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['tx_amp'] = int.from_bytes(self.f.read(4),byteorder='little')
        _ = self.f.read(12)
        self.Water['ping_rate'] = struct.unpack('f',self.f.read(4))[0]
        _ = self.f.read(4)
        self.Water['ping_number'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['time_net'] = struct.unpack('2f',self.f.read(8))[0]
        self.Water['beams'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['vga_t1'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['vga_g1'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['vga_t2'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Water['vga_g2'] = struct.unpack('f',self.f.read(4))[0]
        _ = self.f.read(4)
        self.Water['tx_angle'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['tx_voltage'] = struct.unpack('f',self.f.read(4))[0]
        self.Water['beam_dist_mode'] = int.from_bytes(self.f.read(1),byteorder='little')
        self.Water['sonar_mode'] = int.from_bytes(self.f.read(1),byteorder='little')
        _ = self.f.read(2)
        self.Water['gate_tilt'] = struct.unpack('f',self.f.read(4))[0]
        _ = self.f.read(32)
        tmp = self.f.read(2*self.Water['M']*self.Water['N'])
        data = np.zeros((self.Water['N'],self.Water['M']),dtype=np.uint16)
        for i in range(self.Water['N']):
            for j in range(self.Water['M']):
                data[i,j] = int.from_bytes(tmp[i*self.Water['N']+j*2:i*self.Water['N']+j*2+2],byteorder='little')
        self.Water['data'] = data
        tmp = self.f.read(4*self.Water['N'])
        ang = np.zeros((self.Water['N']),dtype=np.float32)
        for i in range(self.Water['N']):
            ang[i] = struct.unpack('f',tmp[i*4:i*4+4])[0]
        self.Water['bmAng'] = ang

        self.AllWater.append(self.Water)
        self.Water = {}

    def readDepth(self):
        self.Depth['preamble'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Depth['type1'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Depth['size'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Depth['version'] = int.from_bytes(self.f.read(4),byteorder='little')
        _ = self.f.read(4)
        self.Depth['crc'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Depth['snd_velocity'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['sample_rate'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['N'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Depth['ping_number'] = int.from_bytes(self.f.read(4),byteorder='little')
        self.Depth['time'] = struct.unpack('2f',self.f.read(8))[0]
        self.Depth['time_net'] = struct.unpack('2f',self.f.read(8))[0]
        print(self.time_stamp_recv,self.Depth['time'],self.Depth['time_net'])
        self.Depth['ping_rate'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['type2'] = int.from_bytes(self.f.read(2),byteorder='little')
        self.Depth['beam_dist_mode'] = int.from_bytes(self.f.read(1),byteorder='little')
        self.Depth['sonar_mode'] = int.from_bytes(self.f.read(1),byteorder='little')
        _ = self.f.read(8)
        self.Depth['tx_angle'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['gain'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['tx_freq'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['tx_bw'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['tx_len'] = struct.unpack('f',self.f.read(4))[0]
        _ = self.f.read(4)
        self.Depth['tx_voltage'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['swath_dir'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['swath_open'] = struct.unpack('f',self.f.read(4))[0]
        self.Depth['gate_tilt'] = struct.unpack('f',self.f.read(4))[0]
        tmp = self.f.read(20*self.Depth['N'])
        data = np.zeros((self.Depth['N'],8))
        for i in range(self.Depth['N']):
            data[i,0] = int.from_bytes(tmp[i*20:i*20+4],byteorder='little')
            data[i,1] = struct.unpack('f',tmp[i*20+4:i*20+8])[0]
            data[i,2] = int.from_bytes(tmp[i*20+8:i*20+10],byteorder='little')
            data[i,3] = int.from_bytes(tmp[i*20+10:i*20+12],byteorder='little')
            data[i,4] = struct.unpack('f',tmp[i*20+12:i*20+16])[0]
            data[i,5] = int.from_bytes(tmp[i*20+16:i*20+18],byteorder='little')
            data[i,6] = int.from_bytes(tmp[i*20+18:i*20+19],byteorder='little')
            data[i,7] = int.from_bytes(tmp[i*20+19:i*20+20],byteorder='little')
        self.Depth['data'] = data
        # print('a')
        self.AllDepth.append(self.Depth)
        self.Depth = {}
    
    def read(self):
        # for i in range(3000):
        i = 0
        while self.f.read(8) != 'RECORD_\x00':
            # self.RECORD = self.f.read(8) #数据包头
            self.data_type = self.f.read(4) # int 
            if self.data_type.decode() == '':
                print('读取完成')
                break
            size = self.f.read(4) 
            self.size.append(int.from_bytes(size,byteorder='little'))

            self.time_stamp_recv = struct.unpack('2f',self.f.read(8))[0]
            # print(self.time_stamp_recv)
            
            

            if self.data_type.decode()  == '\x05\x00\x00\x00':
                #MRU数据
                print(f'{i}:MRU数据,{self.time_stamp_recv}')
                self.readMRU()
            elif self.data_type.decode()  == '\x03\x00\x00\x00':
                #测深数据
                print(f'{i}:测深数据,{self.time_stamp_recv}')
                self.readDepth()
            elif self.data_type.decode()  == '\x04\x00\x00\x00':
                #GPS数据
                print(f'{i}:GPS数据,{self.time_stamp_recv}')
                self.readGPS()
            else:
                #水体数据
                print(f'{i}:水体数据,{self.time_stamp_recv}')
                self.readWater()
            i = i+1
        
    def close(self):
        self.f.close()