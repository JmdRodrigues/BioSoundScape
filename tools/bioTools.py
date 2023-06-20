import neurokit2 as nk
import numpy as np
from pyo import *
from scipy.signal import resample
from scipy.io import wavfile
import matplotlib.pyplot as plt

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def generateBioSound(biosignal, name, fs):
    biosignal = resample(biosignal, int(44100 * len(biosignal) / fs)) #resample
    biosignal = (biosignal - np.min(biosignal)) / (max(biosignal) - min(biosignal)) #normalize between [0-1]
    wavfile.write("../data/bioSnds/"+name+".wav", 44100, biosignal) #save as wav file

def generateAutomaticMeanECGWave():
    # Retrieve ECG data from data folder
    ecg_signal = nk.data(dataset="ecg_1000hz")
    # Extract R-peaks locations
    _, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=1000)
    peaks_pos = rpeaks["ECG_R_Peaks"]

    mean_wave = []
    for i in range(len(peaks_pos)):
        if i == 0:
            pass
        elif (i == len(peaks_pos) - 1):
            pass
        else:
            subsegment = ecg_signal[peaks_pos[i] - 500:peaks_pos[i] + 500]
            mean_wave.append(subsegment)

    mean_wave = np.mean(mean_wave, axis=0)

    return mean_wave

def createECGMeanWaveSnd():
    ecg_mean_wave = generateAutomaticMeanECGWave()
    generateBioSound(ecg_mean_wave, "ecg_mw", 1000)

def createEMGWaveSnd():
    emg_raw = np.loadtxt("../data/biosignals/SampleEMG_converted.txt")[:, -1]
    emg_env = moving_average(np.abs(emg_raw), 1000)
    # generateBioSound(emg_raw, "emg_raw", 1000)
    # generateBioSound(emg_env, "emg_env", 1000)
    # generateBioSound(emg_raw[1000:2500], "emg_raw_key", 1000)
    generateBioSound(emg_env[1000:2500], "emg_env_key", 1000)


if __name__ == "__main__":
    createEMGWaveSnd()