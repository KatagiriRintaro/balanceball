import serial
from datetime import datetime
import pandas as pd
import time
import argparse
import asyncio

# 各シリアルポートを設定
magnetic_ser = serial.Serial('COM11', 9600, timeout=1)
m5_serial = serial.Serial("COM3", 9600, timeout=1)
button_serial = serial.Serial("COM12", 9600, timeout=1)

# 引数の設定
argparse_r = argparse.ArgumentParser()
argparse_r.add_argument('--name', type=str, help='被験者名')
argparse_r.add_argument('--training', type=str, choices=['hamstring_curl', 'press_up', "knee_extension", "pike", "skier", "abdominal_crunch"], help='内容')
argparse_r.add_argument('--number', type=str, help='回数')

args = argparse_r.parse_args()
name = args.name
training = args.training
number = args.number

# データファイルのパスを設定
dt = datetime.now()
yymmdd = dt.strftime('%Y%m%d')
data_csv_path = './データ/' + yymmdd + '_' + name + '_' + training + '_' + number + '.csv'

elapsedTime = 0
data_list = []
print("start!!")
start_time = time.time()

async def read_serial(serial_port, data_label):
    try:
        line = serial_port.readline()
        result = line.decode('utf-8').strip()
        if result:
            print(f"Received {data_label} data: {result}")
            return list(map(float, result.split(',')))
    except (serial.SerialException, ValueError) as e:
        print(f"Error reading {data_label}: {e}")
        return [0] * 3  # デフォルトの値（例: 3つのセンサー値）

async def main():
    global elapsedTime
    try:
        while elapsedTime < 3600:
            now_time = time.time()
            converted_time = datetime.fromtimestamp(now_time).strftime('%Y-%m-%d %H:%M:%S')
            elapsedTime = now_time - start_time

            # 各シリアルポートからのデータ読み取りを非同期に行う
            magnetic_data = await read_serial(magnetic_ser, "magnetic")
            m5_data = await read_serial(m5_serial, "M5")
            button_data = await read_serial(button_serial, "button")

            # データをリストに追加
            if magnetic_data and m5_data and button_data:
                a_data = [converted_time, elapsedTime] + magnetic_data + m5_data + button_data
                data_list.append(a_data)

            # 多少の遅延を入れることでCPUの使用率を下げる
            # await asyncio.sleep(0.01)

    except KeyboardInterrupt:
        print("Process interrupted by user.")
    
    finally:
        # 終了時にデータをCSVに保存
        df = pd.DataFrame(data_list, columns=['time', 'elapsed time', 'Magnetic_Sensor1', 'Magnetic_Sensor2', 'Magnetic_Sensor3','Acc_x', 'Acc_y', 'Acc_z', 'Gyro_x', 'Gyro_y', 'Gyro_z', 'Button_State'])
        df.to_csv(data_csv_path, index=False)
        print("Data saved to CSV.")
        print(df)

# イベントループを実行
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
