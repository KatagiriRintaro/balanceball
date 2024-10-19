from datetime import datetime, timedelta
import zipfile
import pandas as pd
from io import BytesIO
import numpy as np
from scipy.stats import skew
from scipy.stats import kurtosis
import os


class DataProcessor:

    def __init__(self, mag_folder_path, acc_folder_path, feature_df, subject_name, sampling_rate, data_seconds, sliding_window):
        self.mag_folder_path = mag_folder_path
        self.acc_folder_path = acc_folder_path
        self.feature_df = feature_df
        self.subject_name = subject_name
        self.sampling_rate = sampling_rate
        self.data_seconds = data_seconds
        self.sliding_window = sliding_window
        self.training = ['bounce', 'walk', 'sit', 'extension', 'knee', 'roll']
        self.posture = ['daru', 'shan']
        self.all_file_feature_df = pd.DataFrame(columns = self.feature_df.columns)
        self.all_file_raw_df = pd.DataFrame()

    def apply_time(self, time):
        digit_count = len(str(time))
        if digit_count == 13:
            dt = datetime(1970, 1, 1) + timedelta(seconds=time / 1000) + timedelta(hours=9)
        else:
            dt = datetime(1970, 1, 1) + timedelta(seconds=time / 1e9) + timedelta(hours=9)

        # フォーマットして表示
        formatted_time = dt.strftime('%Y/%m/%d %H:%M:%S')
        return formatted_time
    
    def extract_features(self, data, hz):
        N = len(data)  # データ数
        if N <= 2:
            return np.zeros(18)  # 十分なデータがない場合はゼロの特徴量を返す

        # FFTの計算
        freq = np.fft.fftfreq(N, d=1/hz)  # FFTの横軸(分解能はデータ数で決まる)
        data_fft = np.fft.fft(data)
        power_spectrum = np.abs(data_fft)**2 / N  # データ数で割ることでパワースペクトルに変換
        freq = freq[1:N//2]
        power_spectrum = power_spectrum[1:N//2]

        features = []

        # 時系列データの基本統計量
        features.append(round(np.mean(data), 3))
        features.append(round(np.mean(power_spectrum), 3))
        features.append(round(np.std(data), 3))
        features.append(round(np.std(power_spectrum), 3))
        features.append(round(np.max(data), 3))
        features.append(round(np.max(power_spectrum), 3))
        features.append(round(np.min(data), 3))
        features.append(round(np.min(power_spectrum), 3))
        features.append(round(skew(data), 3))
        features.append(round(skew(power_spectrum), 3))
        features.append(round(kurtosis(data), 3))
        features.append(round(kurtosis(power_spectrum), 3))

        # パワースペクトルのピーク周波数の計算
        peak_sorted_indices = np.argsort(power_spectrum)[::-1]
        peak_sorted_power_spectrum = power_spectrum[peak_sorted_indices]
        peak_sorted_freq = freq[peak_sorted_indices]

        if len(peak_sorted_freq) >= 3:
            # 第1ピーク周波数
            peak_freq = peak_sorted_freq[0]
            features.append(round(peak_freq, 3))

            # 第2ピーク周波数
            second_peak_freq = peak_sorted_freq[1]
            features.append(round(second_peak_freq, 3))

            # 第2ピーク周波数の比率
            if peak_sorted_power_spectrum[0] != 0:
                second_peak_freq_ratio = peak_sorted_power_spectrum[1] / peak_sorted_power_spectrum[0]
            else:
                second_peak_freq_ratio = 0
            features.append(round(second_peak_freq_ratio, 3))

            # 第3ピーク周波数
            third_peak_freq = peak_sorted_freq[2]
            features.append(round(third_peak_freq, 3))

            # 第3ピーク周波数の比率
            if peak_sorted_power_spectrum[0] != 0:
                third_peak_freq_ratio = peak_sorted_power_spectrum[2] / peak_sorted_power_spectrum[0]
            else:
                third_peak_freq_ratio = 0
            features.append(round(third_peak_freq_ratio, 3))
        else:
            # 十分なピークデータがない場合はゼロを追加
            features.extend([0, 0, 0, 0, 0])

        # 重み付き平均周波数の計算
        weighted_frequencies = power_spectrum * freq
        total_sum = np.sum(power_spectrum)
        if total_sum != 0:
            mean_frequency = round(np.sum(weighted_frequencies) / total_sum, 3)
        else:
            mean_frequency = 0
        features.append(mean_frequency)

        # NaNを0に置換
        features = np.nan_to_num(features)

        return features

    def importData(self):
        mag_files = os.listdir(self.mag_folder_path)
        zip_files = [file for file in mag_files if file.endswith('.zip')]
        acc_files = os.listdir(self.acc_folder_path)
        csv_files = [file for file in acc_files if file.endswith('.csv')]
        for zip_file in zip_files:
            zip_file_path = os.path.join(self.mag_folder_path, zip_file)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()

                for file_name in file_list:
                    if file_name.endswith('MagnetometerUncalibrated.csv'):
                        with zip_ref.open(file_name) as file:
                            mag_data_df = pd.read_csv(BytesIO(file.read()))
                if mag_data_df is not None and not mag_data_df.empty:
                    mag_data_df['time'] = mag_data_df['time'].apply(self.apply_time)
                    columns_to_adjust = ['z', 'y', 'x']  # 対象の列名をリストにする
                    for col in columns_to_adjust:
                        mag_data_df[col] = mag_data_df[col] - mag_data_df[col].iloc[0]
                    for csv_file in csv_files:
                        csv_file_name = csv_file.split('.csv')[0]
                        zip_file_name = zip_file.split('.zip')[0]

                        if csv_file_name.startswith(zip_file_name):
                            acc_data_df = pd.read_csv(self.acc_folder_path + csv_file)
                            acc_data_df['epoch (ms)'] = acc_data_df['epoch (ms)'].apply(self.apply_time)
                            columns_to_adjust = ['x-axis (g)', 'y-axis (g)', 'z-axis (g)']  # 対象の列名をリストにする
                            for col in columns_to_adjust:
                                acc_data_df[col] = acc_data_df[col] - acc_data_df[col].iloc[0]

                            mag_data_df['time'] = pd.to_datetime(mag_data_df['time'])
                            acc_data_df['epoch (ms)'] = pd.to_datetime(acc_data_df['epoch (ms)'])

                            start_time = max(mag_data_df['time'].min(), acc_data_df['epoch (ms)'].min())
                            end_time = min(mag_data_df['time'].max(), acc_data_df['epoch (ms)'].max())

                            mag_data_df = mag_data_df[(mag_data_df['time'] > start_time) & (mag_data_df['time'] < end_time)]
                            acc_data_df = acc_data_df[(acc_data_df['epoch (ms)'] > start_time) & (acc_data_df['epoch (ms)'] < end_time)]

                            mag_data_df = mag_data_df.copy()
                            acc_data_df = acc_data_df.copy()


                            end_time = mag_data_df['time'].iloc[-1]  - pd.Timedelta(seconds=1)
                            start_time = end_time - pd.Timedelta(seconds=25)
                            mag_data_df = mag_data_df[(mag_data_df['time'] >= start_time) & (mag_data_df['time'] < end_time)]
                            acc_data_df = acc_data_df[(acc_data_df['epoch (ms)'] >= start_time) & (acc_data_df['epoch (ms)'] < end_time)]

                            a_file_df = pd.DataFrame(columns = ['z', 'y', 'x','Acc_x', 'Acc_y', 'Acc_z'])

                            for i in range(len(mag_data_df['time'].unique())):
                                a_mag_data_df = mag_data_df[mag_data_df['time'] == mag_data_df['time'].unique()[i]]
                                a_acc_data_df = acc_data_df[acc_data_df['epoch (ms)'] == acc_data_df['epoch (ms)'].unique()[i]]

                                mag_indices = a_mag_data_df['seconds_elapsed'].values
                                acc_indices = a_acc_data_df['elapsed (s)'].values

                                a_mag_data_df = a_mag_data_df[['z','y','x']]
                                a_acc_data_df = a_acc_data_df[['x-axis (g)', 'y-axis (g)', 'z-axis (g)']]

                                a_mag_data_df = a_mag_data_df.reset_index(drop=True)
                                a_acc_data_df = a_acc_data_df.reset_index(drop=True)

                                new_indices = np.arange(0, 1, 1/self.sampling_rate)
                                a_part_a_file_df = pd.DataFrame(columns = ['z', 'y', 'x','Acc_x', 'Acc_y', 'Acc_z'])
                                columns = a_part_a_file_df.columns
                                for j, column in enumerate(a_mag_data_df.columns):
                                    mag_interpolated = np.interp(new_indices, mag_indices, a_mag_data_df[column])
                                    a_part_a_file_df[columns[j]] = pd.Series(mag_interpolated)
                                for j, column in enumerate(a_acc_data_df.columns):
                                    acc_interpolated = np.interp(new_indices, acc_indices, a_acc_data_df[column])
                                    a_part_a_file_df[columns[j+3]] = pd.Series(acc_interpolated)

                                if not a_part_a_file_df.empty and not a_part_a_file_df.isna().all().all():
                                    a_part_a_file_df = a_part_a_file_df.dropna(how='all', axis=1)
                                    a_file_df = a_file_df.dropna(how='all', axis=1)
                                    a_file_df = pd.concat([a_file_df, a_part_a_file_df], axis=0, ignore_index=True)
                                else:
                                    print('TT')

                            a_file_df = a_file_df.reset_index(drop=True)
                            i = 0
                            a_file_feature_df = pd.DataFrame(columns=self.feature_df.columns)
                            a_file_raw_df = pd.DataFrame()
                            while self.data_seconds*self.sampling_rate + i*self.sliding_window*self.sampling_rate <= len(a_file_df):
                                sliding_data_df = a_file_df.iloc[int(i*self.sliding_window*self.sampling_rate) : int(self.data_seconds * self.sampling_rate) + int(i*self.sliding_window*self.sampling_rate), :]
                                a_raw_data = []
                                a_feature_data = []
                                for column in sliding_data_df.columns:
                                    a_data = sliding_data_df[column].values
                                    a_data_feature = self.extract_features(a_data, self.sampling_rate)
                                    a_raw_data.extend(a_data)
                                    a_feature_data.extend(a_data_feature)
                                for j in range(len(self.training)):
                                    if self.training[j] in zip_file_name:
                                        a_raw_data.append(self.training[j])
                                        a_feature_data.append(self.training[j])
                                        t = self.training[j]
                                for j in range(len(self.subject_name)):
                                    if self.subject_name[j] in zip_file_name:
                                        a_raw_data.append(j+1)
                                        a_feature_data.append(j+1)    
                                for j in range(len(self.posture)):
                                    if self.posture[j] in zip_file_name:
                                        if self.posture[j] == 'shan':
                                            a_raw_data.append('Good Posture')
                                            a_feature_data.append('Good Posture')
                                            p = 'Good Posture'
                                        else:
                                            a_raw_data.append('Bad Posture')
                                            a_feature_data.append('Bad Posture')
                                            p = 'Bad Posture'
                                number = zip_file_name[-1]
                                a_raw_data.append(number)
                                a_feature_data.append(number)
                                a_raw_data.append(t+p)
                                a_feature_data.append(t+p)

                                a_file_raw_df[f"{zip_file_name}{i}"] = a_raw_data
                                a_file_feature_df.loc[len(a_file_feature_df)] = a_feature_data
                                i += 1
                
                a_file_raw_df = a_file_raw_df.dropna(how='all', axis=1)
                self.all_file_raw_df = self.all_file_raw_df.dropna(how='all', axis=1)
                self.all_file_raw_df = pd.concat([self.all_file_raw_df, a_file_raw_df], axis=1)
                a_file_feature_df = a_file_feature_df.dropna(how='all', axis=1)
                self.all_file_feature_df = self.all_file_feature_df.dropna(how='all', axis=1)
                self.all_file_feature_df = pd.concat([self.all_file_feature_df, a_file_feature_df], axis=0)
        print(self.all_file_raw_df.shape)
        
        self.all_file_raw_df = self.all_file_raw_df.reset_index(drop=True)
        self.all_file_feature_df = self.all_file_feature_df.reset_index(drop=True)

        return self.all_file_raw_df, self.all_file_feature_df
    
    def extractData(self, sensor, type):
        self.all_file_raw_df, self.all_file_feature_df = self.importData()
        if sensor == "mag":
            if type == "raw":
                extractedData1 = self.all_file_raw_df.iloc[ : self.sampling_rate * self.data_seconds * 3]
                extractedData2 = self.all_file_raw_df.iloc[-5:]
                extractedData = pd.concat([extractedData1, extractedData2], axis=0)
            elif type == "feature":
                extractedData1 = self.all_file_feature_df.iloc[:, :54]
                extractedData2 = self.all_file_feature_df.iloc[:, -5:]
                extractedData = pd.concat([extractedData1, extractedData2], axis=1)

        elif sensor == "acc":
            if type == "raw":
                extractedData = self.all_file_raw_df.iloc[self.sampling_rate * self.data_seconds * 3 : ]
            elif type == "feature":
                extractedData = self.all_file_feature_df.iloc[:, 54:]
        
        return self.all_file_raw_df, self.all_file_feature_df, extractedData


