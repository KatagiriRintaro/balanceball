from data import extract_features
import numpy as np
import pandas as pd
import pickle

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
                                    ])

def predictor(data, sampling_rate, data_seconds):

    df = pd.DataFrame(columns=['time', 'x', 'y', 'z', 'elapsed time'])

    df = pd.DataFrame(data, columns= ['time', 'x', 'y', 'z', 'elapsed time'])
    df['time'] = pd.to_datetime(df['time']).dt.floor('S')

    df = df.reset_index(drop=True)

    end_time = df['time'].iloc[-1] - pd.Timedelta(seconds = 1)
    start_time = end_time - pd.Timedelta(seconds = 27)

    # print(df)
    print(f'start: {start_time}')
    print(f'end: {end_time}')

    df = df[(df['time'] >= start_time) & (df['time'] < end_time)]

    new_df = pd.DataFrame(columns = ['z', 'y', 'x'])
    for i in range(len(df['time'].unique())):
        a_df_data = df[df['time'] == df['time'].unique()[i]]
        a_mag_data = a_df_data[['z', 'y', 'x']]

        a_new_df = pd.DataFrame(columns = ['z', 'y', 'x'])

        new_indices = np.arange(0, 1, 1/sampling_rate)

        # for column in a_mag_data.columns:
        #     interpolated = np.interp(new_indices, a_df_data['elapsed time'], a_df_data[column])
        #     a_new_df[column] = pd.Series(interpolated).reset_index(drop=True)

        a_new_df_data = {}
        for column in a_mag_data.columns:
        # 補間の実行
            interpolated = np.interp(new_indices, a_df_data['elapsed time'], a_df_data[column])
            a_new_df_data[column] = interpolated
        a_new_df = pd.DataFrame(a_new_df_data)

        if not a_new_df.empty and not a_new_df.isna().all().all():
            a_new_df = a_new_df.reindex(columns=new_df.columns)  # 列を一致させる
            new_df = pd.concat([new_df, a_new_df], axis=0, ignore_index=True)
        else:
            print('TT')

    i = 0
    file_feature_df = pd.DataFrame(columns=feature_df.columns)
    while i * data_seconds * sampling_rate <= len(new_df):
        sliding_data = new_df.iloc[i * data_seconds * sampling_rate : (i+1) * data_seconds * sampling_rate]
        a_feature_df = []
        for column in sliding_data.columns:
            a_data = sliding_data[column].values
            a_data_feature = extract_features(a_data, sampling_rate)
            a_feature_df.extend(a_data_feature)
        
        file_feature_df.loc[len(file_feature_df)] = a_feature_df
        i += 1

    print(file_feature_df)

    label_names = ['training', 'posture', 'training_posture']
    dfs = pd.DataFrame

    for i in range(len(label_names)):
        with open('./RF' + label_names[i] + '_.pickle', mode = 'rb') as f:
            clf = pickle.load(f)
        y = clf.predict(file_feature_df)

        results = []

    # 最初の値を設定
    current_value = y[0]
    current_count = 1

    # リストの2番目からループ開始
    for i in range(1, len(y)):
        if y[i] == current_value:
            # 同じ値が続いている場合、カウントを増やす
            current_count += 1
        else:
            # 異なる値になった場合、結果に追加してリセット
            results.append([current_value, current_count * data_seconds])
            current_value = y[i]
            current_count = 1

    # 最後の値も追加
    results.append([current_value, current_count * data_seconds])

    # DataFrameに変換
    result_df = pd.DataFrame(results, columns=["Label", "Duration (seconds)"])
    dfs = result_df.copy()

    del df

    return dfs
