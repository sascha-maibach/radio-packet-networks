from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import warnings

class Decoder:    
    
    def __init__(self, fft_size=512, num_rows=2048):
        self.sdr = RtlSdr()
        self.sdr.sample_rate = 2e6 # Hz
        self.sdr.center_freq = 446.2e6 + 900   # Hz
        self.sdr.freq_correction = 30  # PPM
        #print(sdr.valid_gains_db)
        self.sdr.gain = 49.6
        self.average_max_signal_strength = 0
        self.signal_found = False
        self.signal_threshold = 0
        self.frequency_threshold = 0
        self.fft_size = fft_size
        self.num_rows = num_rows
        self.barker_sequence = np.array([1, 1, 1, -1, -1, 1, -1])

        warnings.filterwarnings("ignore", category=RuntimeWarning)

    def __str__(self):
        return f"custom object string method. sdr: {self.sdr}"


    def sample(self):
        samples = self.sdr.read_samples(2048) # some initial samples are usually useless
        samples = self.sdr.read_samples(self.fft_size*self.num_rows)
        return samples


    def do_fft(self, samples):
        #fft = np.zeros(shape=(self.num_rows, self.fft_size))
        fft = np.zeros((self.num_rows, self.fft_size), dtype=np.complex128)
        fft_shifted = np.zeros(shape=(self.num_rows, self.fft_size), dtype=np.complex128)
        spectro = np.zeros(shape=(self.num_rows, self.fft_size))
        for i in range(self.num_rows):
            fft[i] = np.fft.fft(samples[i*self.fft_size:(i+1)*self.fft_size])
            fft_shifted[i] = np.fft.fftshift(fft[i])
            spectro[i] = 10*np.log10(np.abs(fft_shifted[i])**2)
        return fft, fft_shifted, spectro


    def calibrate_signal_strength(self):
        print("Calibrating signal strength...\n")
        max_signal_strength = []
        repetitions = 5
        for i in range(repetitions):
            print(f"  {  ((int)(100/repetitions))*(i+1) }%")
            fft, _, _ = self.do_fft(self.sample())
            for j in range(self.num_rows):
                p = np.partition(fft[j], self.fft_size - 32)
                #print(f"fft'd {len(p)} samples, taking {len(p[self.fft_size - 32:])} largest for averaging.")
                max_signal_strength.append(p[self.fft_size - 32:])
            #print(f"Signal strength {max_signal_strength[i]} detected.\n")
        print("  100%")
        self.signal_threshold = 2*self.get_2d_array_average(max_signal_strength)
        print(f"Signal strength threshold set to {self.signal_threshold}.\n")


    def get_2d_array_average(self, array):
        total_sum = 0
        element_count = 0
        for x in array:
            total_sum += sum(x)
            element_count += len(x)
        return total_sum/element_count


    def wait_for_user_input(self):
        a = input("* ************\n* Signal strength threshold calibrated.\n* Start Sending to calibrate FSK frequencies\n* Press enter to continue\n * ************")


    def calibrate_frequencies(self):
        print("Calibrating frequencies..")
        total_sum = 0
        total_len = 0
        for i in range(10):
            fft, _, _ = self.do_fft(self.sample())  # sample data
            for j in range(self.num_rows):
                fft_row = fft[j]
                frequencies = np.fft.fftfreq(len(fft_row))
                signal_frequencies = frequencies[fft_row > self.signal_threshold]
                total_sum += sum(signal_frequencies)
                total_len += len(signal_frequencies)
        self.frequency_threshold = total_sum/total_len


    def extract_frequencies(self):
        while True:
            fft, _, _ = self.do_fft(self.sample())  # sample data
            for j in range(self.num_rows):
                fft_row = fft[j]
                frequencies = np.fft.fftfreq(len(fft_row))
                signal_frequencies = frequencies[fft_row > self.signal_threshold]
                for x in signal_frequencies:
                    if x > self.frequency_threshold:
                        print("1")
                    else:
                        print("0")


    def detect_barker(self, binary_signal):
        i = 0
        for x in binary_signal:
            if x == 0:
                binary_signal[i] = -1
            i += 1
        return max(np.correlate(binary_signal, self.barker_sequence, mode='same')) == 7


if __name__ == "__main__":
    '''
    test_array = np.random.rand(2048)
    print(f"{test_array}\n length: {len(test_array)}")
    extract = test_array[(test_array>0.5)]
    print(f"{extract}\n length: {len(extract)}")
    '''

    decoder = Decoder()
    decoder.calibrate_signal_strength()
    decoder.wait_for_user_input()
    decoder.calibrate_frequencies()
    decoder.extract_frequencies()
    print("Done.")