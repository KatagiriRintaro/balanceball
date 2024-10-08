<<<<<<< HEAD
import numpy as np
from scipy.stats import skew, kurtosis

def extract_features(data, hz):
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
=======
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import skew, kurtosis

def apply_time(time):
    digit_count = len(str(time))
    if digit_count == 13:
        dt = datetime(1970, 1, 1) + timedelta(seconds=time / 1000) + timedelta(hours=9)
    else:
        dt = datetime(1970, 1, 1) + timedelta(seconds=time / 1e9) + timedelta(hours=9)

    # フォーマットして表示
    formatted_time = dt.strftime('%Y/%m/%d %H:%M:%S')
    return formatted_time


def extract_features(data, hz):
    N=len(data) #データ数
    freq = np.fft.fftfreq(N, d = 1/hz) #fftの横軸(分解能はデータ数で決まる)
    data_fft = np.fft.fft(data)
    power_spectrum = np.abs(data_fft)**2/N #データ数で割ることでパワースペクトルに変換
    freq = freq[1:N//2]
    power_spectrum = power_spectrum[1:N//2]
    # amplitude = nk.rsp_amplitude(cleaned, peak_signals)
    # rate = nk.rsp_rate(cleaned, sampling_rate=hz)
    # symmetry = nk.rsp_symmetry(cleaned, peak_signals)

    features = []

    features.append(round(np.mean(data),3))
    features.append(round(np.mean(power_spectrum),3))
    features.append(round(np.std(data),3))
    features.append(round(np.std(power_spectrum),3))
    features.append(round(np.max(data),3))
    features.append(round(np.max(power_spectrum),3))
    features.append(round(np.min(data),3))
    features.append(round(np.min(power_spectrum),3))
    features.append(round(skew(data),3))
    features.append(round(skew(power_spectrum),3))
    features.append(round(kurtosis(data),3))
    features.append(round(kurtosis(power_spectrum),3))

    peak_sorted_indices = np.argsort(power_spectrum)[::-1]
    peak_sorted_power_spectrum = power_spectrum[peak_sorted_indices]
    peak_sorted_freq = freq[peak_sorted_indices]
    # print(peak_sorted_power_spectrum)
    # print(peak_sorted_freq)

    peak_freq = peak_sorted_freq[0]
    features.append(round(peak_freq,3))

    second_peak_freq = peak_sorted_freq[1]
    features.append(round(second_peak_freq,3))
    second_peak_freq_ratio = peak_sorted_power_spectrum[1]/peak_sorted_power_spectrum[0]
    features.append(round(second_peak_freq_ratio,3))

    third_peak_freq = peak_sorted_freq[2]
    features.append(round(third_peak_freq,3))
    third_peak_freq_ratio = peak_sorted_power_spectrum[2]/peak_sorted_power_spectrum[0]
    features.append(round(third_peak_freq_ratio,3))

    weighted_frequencies = []
    for i in range(len(power_spectrum)):
        weighted_frequencies.append(power_spectrum[i] * freq[i])
    total_sum = np.sum(power_spectrum)
    weighted_sum = np.sum(weighted_frequencies)
    mean_frequency = round(weighted_sum / total_sum, 3)
    features.append(mean_frequency)

>>>>>>> c77b0830baa7108ec8cbb14edce9792e4a122857
    features = np.nan_to_num(features)

    return features