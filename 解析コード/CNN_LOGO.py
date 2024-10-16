from CNN import cnn_model
from Make_Class import Make_Class
import numpy as np
import pandas as pd
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler

sampling_hz = 20
a_training_second = 6
train_name = ['hamstring_curl', 'press_up', "knee_extension", "pike", "skier", "abdominal_crunch"]
nor_df_path = "./nor_df.csv"
nor_df = pd.read_csv(nor_df_path)
all_training_feature_df_path = "./all_training_feature_df.csv"
all_training_feature_df = pd.read_csv(all_training_feature_df_path)

m_cnn_data = np.zeros([len(all_training_feature_df), sampling_hz * a_training_second, 3, 1])
m5_cnn_data = np.zeros([len(all_training_feature_df), sampling_hz * a_training_second, 6, 1])
all_cnn_data = np.zeros([len(all_training_feature_df), sampling_hz * a_training_second, 9, 1])

for i in range(len(nor_df)//(sampling_hz * a_training_second)):
    m_cnn_data[i, :, :, 0] = nor_df.iloc[i * sampling_hz * a_training_second : (i + 1) * sampling_hz * a_training_second, :3].values
    m5_cnn_data[i, :, :, 0] = nor_df.iloc[i * sampling_hz * a_training_second : (i + 1) * sampling_hz * a_training_second, 3:].values
    all_cnn_data[i, :, :, 0] = nor_df.iloc[i * sampling_hz * a_training_second : (i + 1) * sampling_hz * a_training_second, :].values

# StandardScalerのインスタンスを作成
scaler = StandardScaler()

# 各データを標準化
m_cnn_data = m_cnn_data.reshape(m_cnn_data.shape[0], -1)
m_cnn_data = scaler.fit_transform(m_cnn_data).reshape(m_cnn_data.shape[0], sampling_hz * a_training_second, 3, 1)

m5_cnn_data = m5_cnn_data.reshape(m5_cnn_data.shape[0], -1)
m5_cnn_data = scaler.fit_transform(m5_cnn_data).reshape(m5_cnn_data.shape[0], sampling_hz * a_training_second, 6, 1)

all_cnn_data = all_cnn_data.reshape(all_cnn_data.shape[0], -1)
all_cnn_data = scaler.fit_transform(all_cnn_data).reshape(all_cnn_data.shape[0], sampling_hz * a_training_second, 9, 1)

# Classlabel = np.zeros([len(all_training_feature_df), all_training_feature_df["class"].nunique()])
# for i in range(len(all_training_feature_df["class"])):
#     Classlabel[i, :] = np.zeros([1, 6])
#     Classlabel[i, train_name.index(all_training_feature_df["class"][i])] = 1

print("m_cnn_data.shape:", m_cnn_data.shape)

# LOGOのインスタンスを作成
logo = LeaveOneGroupOut()

# filter_size_list = [2, 4, 8, 16, 32, 64]
filter_size_list = [8]
# kernel_size_list = [4, 6, 8, 10]
kernel_size_list = [10]
filter_size_list_str = [str(element) for element in filter_size_list]
kernel_size_list_str = [str(element) for element in kernel_size_list]

train_result_df = pd.DataFrame(index=filter_size_list_str, columns=kernel_size_list_str)
test_result_df = pd.DataFrame(index=filter_size_list_str, columns=kernel_size_list_str)

Classes = ['class', 'subject_weight', 'balance_feature', 'balance']

for h in range(len(Classes)):
    if Classes[h] == 'subject_weight':
        indices = all_training_feature_df.index[(all_training_feature_df['subject_weight'] // 10) % 10 == 4].tolist()
        m_cnn_data = np.delete(m_cnn_data, indices, axis=0)
        m5_cnn_data = np.delete(m5_cnn_data, indices, axis=0)
        all_cnn_data = np.delete(all_cnn_data, indices, axis=0)
        all_training_feature_df = all_training_feature_df.drop(indices).reset_index(drop=True)


    Classlabel = Make_Class(all_training_feature_df, Classes[h])
    for i in range(len(filter_size_list)):
        for j in range(len(kernel_size_list)):
            score_train_array = []
            score_test_array = []
            for train_index, test_index in logo.split(m_cnn_data, Classlabel, groups=all_training_feature_df['subject_id']):
                train_m = m_cnn_data[train_index]
                train_label = Classlabel[train_index]
                test_m = m_cnn_data[test_index]
                test_label = Classlabel[test_index]

                learning_process, model = cnn_model(120, 3, 6, 6, 800, train_m, train_label, filter_size_list[i], kernel_size_list[j])

                score_train = model.evaluate(train_m, train_label, verbose=1, batch_size=1)
                score_test = model.evaluate(test_m, test_label, verbose=1, batch_size=1)
                
                score_train_array.append(np.round(score_train[1], 4))
                score_test_array.append(np.round(score_test[1], 4))

            train_ave_score = np.mean(score_train_array)
            test_ave_score = np.mean(score_test_array)
            
            train_result_df.at[filter_size_list_str[i], kernel_size_list_str[j]] = train_ave_score
            test_result_df.at[filter_size_list_str[i], kernel_size_list_str[j]] = test_ave_score
    
    print(Classes[h], '_', 'train_ave_score == ', train_ave_score)
    print(Classes[h], '_', 'test_ave_score == ', test_ave_score)


# train_result_csv_path = './train_result_df.csv'
# test_result_csv_path = './test_result_df.csv'
# train_result_df.to_csv(train_result_csv_path)
# test_result_df.to_csv(test_result_csv_path)
