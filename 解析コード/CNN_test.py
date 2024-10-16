from CNN import cnn_model, shuffle
import numpy as np
import pandas as pd
import matplotlib as plt

sampling_hz = 20
a_training_second = 6
train_name = ['hamstring_curl', 'press_up', "knee_extension", "pike", "skier", "abdominal_crunch"]
subject_name_list = ["tanaka","liliu","ori","a","a","a","a","a","a","a"]
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

# j = 0 # j+1.csvを表示、j=0

# fig = plt.figure(figsize=(10, 5)) # 描画領域の横、縦のサイズ
# plt.imshow(m_cnn_data[j, :, :, 0].T, cmap='gray') #.Tは転置
# plt.show()

Classlabel = np.zeros([len(all_training_feature_df), all_training_feature_df["class"].nunique()])
print(Classlabel.shape)

print(len(all_training_feature_df["class"]))
for i in range(len(all_training_feature_df["class"])):
    Classlabel[i, :] = np.zeros([1, 6])
    Classlabel[i, train_name.index(all_training_feature_df["class"][i])] = 1
    # print(Classlabel)

# print(m_cnn_data.shape)
# print(Classlabel)

print("m_cnn_data.shape:", m_cnn_data.shape)

s_m_cnn_data, s_Classlabel = shuffle(m_cnn_data, Classlabel)

print("s_m_cnn_data.shape:", m_cnn_data.shape)

train_m = s_m_cnn_data[:int(len(s_m_cnn_data) * 0.8), :, :, :]
test_m = s_m_cnn_data[int(len(s_m_cnn_data) * 0.8):, :, :, :]
train_label = s_Classlabel[:int(len(s_m_cnn_data) * 0.8), :]
test_label = s_Classlabel[int(len(s_m_cnn_data) * 0.8):, :]

print("test_m shape:", test_m.shape)
print("test_label shape:", test_label.shape)
# print("test_m:", test_m)
# print("test_label:", test_label)


filter_size_list = [1,2,4,8,16,32,64]
# filter_size_list = [1]
filter_size_list_str = [str(element) for element in filter_size_list]
kernel_size_list = [4,6,8,10,12,15,20]
# kernel_size_list = [4]
kernel_size_list_str = [str(element) for element in kernel_size_list]

train_result_df = pd.DataFrame(index = filter_size_list_str, columns=kernel_size_list_str)
test_result_df = pd.DataFrame(index = filter_size_list_str, columns=kernel_size_list_str)

for i in range(len(filter_size_list)):
  for j in range(len(kernel_size_list)):
    for k in range(1):
      score_train_array = []
      score_test_array = []
      learning_process, model = cnn_model(120, 3, 6, 6, 800, train_m, train_label, filter_size_list[i], kernel_size_list[j])

  # plt.figure()
  # plt.plot(learning_process.epoch, np.array(learning_process.history['accuracy']),label='Train acc')
  # plt.xlabel('Epoch')
  # plt.ylabel('Acc')
  # plt.grid()
  # plt.legend()
  # plt.show()

      score_train = model.evaluate(train_m, train_label, verbose=1, batch_size=1)
      score_test = model.evaluate(test_m, test_label, verbose=1, batch_size=1)
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





