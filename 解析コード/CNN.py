import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
print("TensorFlowのバージョン:", tf.__version__)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# GPU情報を表示
tf.config.experimental.list_physical_devices('GPU')

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print("使用可能なGPUデバイスがあります:")
    for gpu in gpus:
        print(gpu)
else:
    print("使用可能なGPUデバイスはありません。")

from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

def cnn_model(InputSize1, InputSize2, NumClass, batch_size, epochs, sig_cnn_train, ClassLabel_train, filters, kernel_size):
    model = Sequential()
    model.add(Conv2D(filters=filters, kernel_size=(kernel_size, 1), activation='relu', input_shape=(InputSize1, InputSize2, 1)))
    model.add(Conv2D(filters=filters, kernel_size=(kernel_size, 1), activation='relu'))
    model.add(Conv2D(filters=filters, kernel_size=(kernel_size, 1), activation='relu'))
    # model.add(Conv2D(filters=filters, kernel_size=(kernel_size, 1), activation='relu'))
    # model.add(Conv2D(filters=filters, kernel_size=(kernel_size, 1), activation='relu'))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(30, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(NumClass, activation='softmax'))

    # コンパイル（学習方法の定義）
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
    model.summary() # 構造出力


    ### 学習！ ###
    # batch_size = 30 # うまくいかない場合は、2^n+1にする
    # epochs = 200 # 学習回数
    learning_process = model.fit(sig_cnn_train, ClassLabel_train,  # 信号とラベルデータ
                                    batch_size=batch_size, # バッチサイズ
                                    epochs=epochs,     # エポック数
                                    verbose=0) # 学習過程を可視化させたい場合は1

    print("finish!")
    return learning_process, model

def shuffle(cnn_data, classlabel):
    original_indices = np.arange(len(cnn_data))
    # インデックスをシャッフル
    np.random.shuffle(original_indices)
    # データをシャッフルしたインデックスに基づいて並べ替え
    cnn_data = cnn_data[original_indices, :, :, :]
    classlabel = classlabel[original_indices, :]
    return cnn_data, classlabel