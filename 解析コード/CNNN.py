from datetime import datetime, timedelta
import zipfile
import pandas as pd
from io import BytesIO
import numpy as np
from dotenv import load_dotenv
from DataProcessor import DataProcessor
import os
import ast
from CNN import cnn_model, shuffle


load_dotenv()

subject_name = os.getenv("SUBJECT_NAME")
mag_folder_path = os.getenv("MAG_FOLDER_PATH")
acc_folder_path = os.getenv("ACC_FOLDER_PATH")
subject_name = ast.literal_eval(subject_name)

feature_df = pd.DataFrame(columns = ['z_time_mean','z_fft_mean','z_time_std', 'z_fft_std', 'z_time_max', 'z_fft_max',
                                    'z_time_min', 'z_fft_min', 'z_time_skew', 'z_fft_skew', 'z_time_kurtosis','z_fft_kurtosis',
                                    'z_peak_frequency', 'z_second_peak_frequency', 'z_second_peak_frequency_ratio',
                                    'z_third_peak_frequency', 'z_third_peak_frequency_ration', 'z_mean_frequency',
                                    'y_time_mean','y_fft_mean','y_time_std', 'y_fft_std', 'y_time_max', 'y_fft_max',
                                    'y_time_min', 'y_fft_min', 'y_time_skew', 'y_fft_skew', 'y_time_kurtosis','y_fft_kurtosis',
                                    'y_peak_frequency', 'y_second_peak_frequency', 'y_second_peak_frequency_ratio',
                                    'y_third_peak_frequency', 'y_third_peak_frequency_ration', 'y_mean_frequency',
                                    'x_time_mean','x_fft_mean','x_time_std', 'x_fft_std', 'x_time_max', 'x_fft_max',
                                    'x_time_min', 'x_fft_min', 'x_time_skew', 'x_fft_skew', 'x_time_kurtosis','x_fft_kurtosis',
                                    'x_peak_frequency', 'x_second_peak_frequency', 'x_second_peak_frequency_ratio',
                                    'x_third_peak_frequency', 'x_third_peak_frequency_ration', 'x_mean_frequency',
                                    'acc_x_time_mean','acc_x_fft_mean','acc_x_time_std', 'acc_x_fft_std', 'acc_x_time_max', 'acc_x_fft_max',
                                    'acc_x_time_min', 'acc_x_fft_min', 'acc_x_time_skew', 'acc_x_fft_skew', 'acc_x_time_kurtosis','acc_x_fft_kurtosis',
                                    'acc_x_peak_frequency', 'acc_x_second_peak_frequency', 'acc_x_second_peak_frequency_ratio',
                                    'acc_x_third_peak_frequency', 'acc_x_third_peak_frequency_ration', 'acc_x_mean_frequency',
                                    'acc_y_time_mean','acc_y_fft_mean','acc_y_time_std', 'acc_y_fft_std', 'acc_y_time_max', 'acc_y_fft_max',
                                    'acc_y_time_min', 'acc_y_fft_min', 'acc_y_time_skew', 'acc_y_fft_skew', 'acc_y_time_kurtosis','acc_y_fft_kurtosis',
                                    'acc_y_peak_frequency', 'acc_y_second_peak_frequency', 'acc_y_second_peak_frequency_ratio',
                                    'acc_y_third_peak_frequency', 'acc_y_third_peak_frequency_ration', 'acc_y_mean_frequency',
                                    'acc_z_time_mean','acc_z_fft_mean','acc_z_time_std', 'acc_z_fft_std', 'acc_z_time_max', 'acc_z_fft_max',
                                    'acc_z_time_min', 'acc_z_fft_min', 'acc_z_time_skew', 'acc_z_fft_skew', 'acc_z_time_kurtosis','acc_z_fft_kurtosis',
                                    'acc_z_peak_frequency', 'acc_z_second_peak_frequency', 'acc_z_second_peak_frequency_ratio',
                                    'acc_z_third_peak_frequency', 'acc_z_third_peak_frequency_ration', 'acc_z_mean_frequency',
                                    'training', "subject_id", "posture", "number", 'training_posture'])

sampling_rate = 100
training_seconds = 3

data_processor = DataProcessor(mag_folder_path, acc_folder_path, feature_df, subject_name, sampling_rate, training_seconds, 0.5)

all_file_raw_df, all_file_feature_df, mag_raw_data_df = data_processor.extractData("mag", "raw")

all_file_raw_df.to_csv('all_file_raw_df.csv', index=False)
all_file_feature_df.to_csv('all_file_feature_df.csv', index=False)

mag_cnn_data = np.zeros([mag_raw_data_df.shape[1], sampling_rate * training_seconds, 3, 1])

for i in range(len(mag_raw_data_df)//(sampling_rate * training_seconds)):
  mag_cnn_data[i, :, :, 0] = mag_raw_data_df.iloc[i * sampling_rate * training_seconds : (i + 1) * sampling_rate * training_seconds, :3].values

TrainLabel = np.zeros([len(mag_raw_data_df.columns), mag_raw_data_df.iloc[-5].nunique()])
PostureLabel = np.zeros([len(mag_raw_data_df.columns), mag_raw_data_df.iloc[-3].nunique()])
TrainPostureLabel = np.zeros([len(mag_raw_data_df.columns), mag_raw_data_df.iloc[-1].nunique()])

train_name = ['bounce', 'walk', 'sit', 'extension', 'knee', 'roll']
posture_name = ["Good Posture", "Bad Posture" ]
train_posture_name = []
for i in range(len(train_name)):
  for j in range(len(posture_name)):
    train_posture_name.append(train_name[i]+posture_name[j])

for i in range(len(mag_raw_data_df)):
    TrainLabel[i, :] = np.zeros([1, mag_raw_data_df.iloc[-5].nunique()])
    TrainLabel[i, train_name.index(mag_raw_data_df.iloc[-5,i])] = 1
    PostureLabel[i, :] = np.zeros([1, mag_raw_data_df.iloc[-3].nunique()])
    PostureLabel[i, posture_name.index(mag_raw_data_df.iloc[-3,i])] = 1
    TrainPostureLabel[i, :] = np.zeros([1, mag_raw_data_df.iloc[-1].nunique()])
    TrainPostureLabel[i, train_posture_name.index(mag_raw_data_df.iloc[-1,i])] = 1

s_mag_cnn_data, s_TrainLabel, s_PostureLabel, s_TrainPostureLabel = shuffle(mag_cnn_data, TrainLabel, PostureLabel, TrainPostureLabel)

train_m = s_mag_cnn_data[:int(len(s_mag_cnn_data) * 0.8), :, :, :]
test_m = s_mag_cnn_data[int(len(s_mag_cnn_data) * 0.8):, :, :, :]
train_TrainLabel = s_TrainLabel[:int(len(s_mag_cnn_data) * 0.8), :]
test_TrainLabel = s_TrainLabel[int(len(s_mag_cnn_data) * 0.8):, :]
train_PostureLabel = s_PostureLabel[:int(len(s_mag_cnn_data) * 0.8), :]
test_PostureLabel = s_PostureLabel[int(len(s_mag_cnn_data) * 0.8):, :]
train_ClassLabel = s_TrainPostureLabel[:int(len(s_mag_cnn_data) * 0.8), :]
test_TrainPostureLabel = s_TrainPostureLabel[int(len(s_mag_cnn_data) * 0.8):, :]

filter_size_list = [1,2,4] #,8,16,32,64]
filter_size_list_str = [str(element) for element in filter_size_list]
kernel_size_list = [4,6,8] #,10,12,15,20]
kernel_size_list_str = [str(element) for element in kernel_size_list]

train_result_df = pd.DataFrame(index = filter_size_list_str, columns=kernel_size_list_str)
test_result_df = pd.DataFrame(index = filter_size_list_str, columns=kernel_size_list_str)

for i in range(len(filter_size_list)):
  for j in range(len(kernel_size_list)):
    for k in range(1):
      score_train_array = []
      score_test_array = []
      learning_process, model = cnn_model(sampling_rate * training_seconds, 3, mag_raw_data_df.iloc[-5].nunique(), 6, 800, train_m, train_TrainLabel, filter_size_list[i], kernel_size_list[j])

  # plt.figure()
  # plt.plot(learning_process.epoch, np.array(learning_process.history['accuracy']),label='Train acc')
  # plt.xlabel('Epoch')
  # plt.ylabel('Acc')
  # plt.grid()
  # plt.legend()
  # plt.show()

      score_train = model.evaluate(train_m, train_TrainLabel, verbose=1, batch_size=1)
      score_test = model.evaluate(test_m, test_TrainLabel, verbose=1, batch_size=1)
      print(f'試行パターン', ':', '{i}, {j}, {k}')
      score_train_array.append(np.round(score_train[1], 4))
      score_test_array.append(np.round(score_test[1], 4))
    train_ave_score = np.mean(score_train_array)
    test_ave_score = np.mean(score_test_array)
    train_result_df.at[filter_size_list_str[i], kernel_size_list_str[j]] = train_ave_score
    test_result_df.at[filter_size_list_str[i], kernel_size_list_str[j]] = test_ave_score

train_result_csv_path = './train_result_df.csv'
test_result_csv_path = './test_result_df.csv'
train_result_df.to_csv(train_result_csv_path)
test_result_df.to_csv(test_result_csv_path)





