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