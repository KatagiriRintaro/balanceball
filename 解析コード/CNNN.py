from datetime import datetime, timedelta
import zipfile
import pandas as pd
from io import BytesIO
import numpy as np
from dotenv import load_dotenv
from DataProcessor import DataProcessor
import os
import ast


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

data_processor = DataProcessor(mag_folder_path, acc_folder_path, feature_df, subject_name, 100, 3, 0.5)

all_file_raw_df, all_file_feature_df = data_processor.importData()

all_file_raw_df.to_csv('all_file_raw_df.csv', index=False)
all_file_feature_df.to_csv('all_file_feature_df.csv', index=False)

print(all_file_feature_df)
print(all_file_raw_df)



