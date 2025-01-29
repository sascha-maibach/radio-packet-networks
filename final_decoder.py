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









if __name__ == "__main__":
    pass