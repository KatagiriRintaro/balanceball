import serial
from datetime import datetime
import pandas as pd
import time
import argparse

# magnetic_ser = serial.Serial('COM11', 9600, timeout=None)
m5_serial = serial.Serial("COM3", 9600, timeout=None)
# button_serial = serial.Serial("COM12", 9600, timeout=None)

argparse_r = argparse.ArgumentParser()
argparse_r.add_argument('--name', type=str, help='被験者名')
# argparse_r.add_argument('--training', type=str, choices=['setting','hamstring_curl', 'press_up', "knee_extension", "pike", "skier", "abdominal_crunch"] , help='内容')
argparse_r.add_argument('--training', type=str , help='内容')
argparse_r.add_argument('--number', type=str, help='回数')

args = argparse_r.parse_args()
name = args.name
training = args.training
number = args.number

dt = datetime.now()
yymmdd = dt.strftime('%Y%m%d')
data_csv_path = './new/'+yymmdd+'_'+name+'_'+training+'_'+number+'.csv'


elapsedTime = 0
data_list = []
print("start!!")
start_time = time.time()
try: 
        while (elapsedTime < 3600):
            now_time = time.time()
            converted_time = datetime.fromtimestamp(now_time).strftime('%Y-%m-%d %H:%M:%S')
            elapsedTime = now_time-start_time
            # magnetic_bytes = magnetic_ser.readline()
            m5_bytes = m5_serial.readline()
            # button_bytes = button_serial.readline()
            # magnetic_result = magnetic_bytes.decode('utf-8').strip()
            m5_result = m5_bytes.decode("utf-8").strip()
            # button_result = button_bytes.decode("utf-8").strip()
            # print(f"Received magnetic data: {magnetic_result}")
            # print(f"Received M5 data: {m5_result}")
            # a_magnetic_data = list(map(float, magnetic_result.split(',')))
            a_m5_data = list(map(float, m5_result.split(',')))
            # a_button_data = list(map(float, button_result.split(',')))
            a_data = []
            # a_data.extend(a_magnetic_data)
            a_data.extend(a_m5_data)
            # a_data.extend(a_button_data)
            a_data.insert(0, elapsedTime)
            a_data.insert(0, converted_time)
            # print(a_data)
            data_list.append(a_data)

except serial.SerialTimeoutException:
    pass

except KeyboardInterrupt:
    pass

# df = pd.DataFrame(data_list,columns=['time','elapsed time','Sensor1','Sensor2', 'Sensor3','Acc_x','Acc_y', 'Acc_z','Gyro_x','Gyro_y', 'Gyro_z', 'Boolean'])
df = pd.DataFrame(data_list,columns=['time','elapsed time','Acc_x','Acc_y', 'Acc_z','Gyro_x','Gyro_y', 'Gyro_z'])
df.to_csv(data_csv_path)
print(df)