from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

class Decoder:    
    
    def __init__(self):
        self.sdr = RtlSdr()
        self.sdr.sample_rate = 2e6 # Hz
        self.sdr.center_freq = 446.2e6 + 900   # Hz
        self.sdr.freq_correction = 30  # PPM
        #print(sdr.valid_gains_db)
        self.sdr.gain = 49.6
        self.average_max_signal_strength = 0
        self.signal_found = False
        self.signal_threshold = 2e9
        self.freq_threshold = 0
        
    def __str__(self):
        return f"custom object string method. sdr: {self.sdr}"

    
    def calibrate(self):
        pass


    def sample(self):
        fft_size = 512
        num_rows = 2048
        samples = self.sdr.read_samples(2048) # get rid of initial empty samples
        samples = self.sdr.read_samples(fft_size*num_rows) # get all the samples we need for the spectrogram
        return samples

    def do_fft(self, samples):
        spectrogram[i, :] = 10 * np.log10(
            np.abs(np.fft.fftshift(np.fft.fft(samples[i * fft_size:(i + 1) * fft_size]))) ** 2)









if __name__ == "__main__":
    pass