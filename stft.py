import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import resample
import random
from scipy.signal import stft
import matplotlib.pyplot as plt

def myspectrogram(F0=150, Fm=50, lambda_=0, snrin=10):
    # 参数
    f0 = F0  # 海洋色背景噪声频谱峰值频率
    fm = Fm  # 海洋色背景噪声尖锐度因子
    lam = lambda_  # 海洋色背景噪声幅度比因子
    snr = snrin  # 含噪水下脉冲信号的信噪比
    
    fs = 4000  # 采样频率
    A = 1  # 信号幅度
    T = 5  # 脉冲信号单周期长度
    NP = 1  # 脉冲信号周期数
    T_total = T * NP  # 含噪信号总时长
    NT = round(T * fs)  # 单周期点数
    NL = round(T * NP * fs)  # 总点数
    
    # 生成干净的水下脉冲信号（CW, LFM, HFM）
    f0_CW = random.uniform(100, 1500)  # CW脉冲信号中心频率 (100-1500Hz)
    tau_CW = random.uniform(0.5, 1)  # CW脉冲信号宽度 (0.5-1s)
    t_CW = np.arange(0, tau_CW, 1/fs)  # CW脉冲信号时间
    s_CW = A * np.cos(2 * np.pi * f0_CW * t_CW)  # CW脉冲信号
    
    f1_LFM = random.uniform(100, 400)  # LFM脉冲信号起始频率 (100-400Hz)
    f2_LFM = f1_LFM + random.uniform(50, 100)  # LFM脉冲信号终止频率 (50-100Hz更高)
    tau_LFM = random.uniform(0.5, 1)  # LFM脉冲信号宽度 (0.5-1s)
    k = (f2_LFM - f1_LFM) / tau_LFM  # LFM脉冲信号频率调制率
    t_LFM = np.arange(0, tau_LFM, 1/fs)  # LFM脉冲信号时间
    s_LFM = A * np.cos(2 * np.pi * (f1_LFM * t_LFM + 0.5 * k * t_LFM**2))  # LFM脉冲信号
    
    f1_HFM = random.uniform(100, 300)  # HFM脉冲信号起始频率 (100-300Hz)
    f2_HFM = f1_HFM + random.uniform(400, 500)  # HFM脉冲信号终止频率 (400-500Hz更高)
    tau_HFM = random.uniform(1, 1.5)  # HFM脉冲信号宽度
    mu = (f2_HFM - f1_HFM) / (tau_HFM * f1_HFM * f2_HFM)  # HFM脉冲信号变化率
    t_HFM = np.arange(0, tau_HFM, 1/fs)  # HFM脉冲信号时间
    s_HFM = A * np.cos(2 * np.pi / mu * np.log(-mu * t_HFM + 1 / f1_HFM))  # HFM脉冲信号
    
    tau_interval = random.random()
    t_interval = np.arange(0, tau_interval, 1/fs)  # 间隔信号时间
    s_interval = np.zeros_like(t_interval)  # 间隔信号（无脉冲）
    
    sig = np.concatenate([s_CW,s_interval,s_LFM])  # 清净信号（仅包含CW信号，简化处理）
    NS = len(sig)  # 组合脉冲信号长度
    
    # 读取实际海洋数据（背景噪声）
    filename_wav = rf"D:\AAAprogramfile\matlab\shuju\shipsear\Shipsear1\6__10_07_13_marDeCangas_Entra.wav"
    fs_wav, y_wav = wav.read(filename_wav)
    
    # 在5秒范围内随机选择起点
    total_duration_wav = len(y_wav) / fs_wav  # 总持续时间（秒）
    start_time_wav = random.randint(0, int((total_duration_wav - T_total) * fs_wav))  # 随机起始时间
    
    # 提取选定的5秒音频
    y_selected_wav = y_wav[start_time_wav:start_time_wav + int(T_total * fs_wav)]
    
    # 将信号重采样到所需的采样率
    y_wav_downsampled = resample(y_selected_wav, int(len(y_selected_wav) * fs / fs_wav))
    
    # 根据SNR计算噪声幅度
    sigma = A * np.sqrt(1 / (10 ** (snr / 10)))  # 噪声幅度
    noise = sigma * y_wav_downsampled
    
    # 生成含噪脉冲信号
    noisy_sig = noise.copy()
    for k in range(NP):
        noisy_sig[(k * NT):((k * NT) + NS)] += sig  # 将脉冲信号加到含噪信号上
    
    sig = noisy_sig - noise  # 清净脉冲信号
    
    return noisy_sig, noise, sig, fs

if __name__ == '__main__':
    snrin = 100
    noisy_sig, noise, sig, fs = myspectrogram(snrin=snrin)
    print(noisy_sig, noise, sig, fs)

    #对noisy_sig进行STFT，窗长为256，步长为64
    f, t, Zxx = stft(noisy_sig, fs, nperseg=256, noverlap=192)
    plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')

    plt.show()






