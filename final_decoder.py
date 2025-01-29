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

        warnings.filterwarnings("ignore", category=RuntimeWarning)

    def __str__(self):
        return f"custom object string method. sdr: {self.sdr}"

    
    def calibrate(self):
        pass


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
        total_sum = 0
        total_len = 0
        for i in range(10):
            fft, fft_shifted, spectro = self.do_fft(self.sample()) # sample data
            for j in range(self.num_rows):
                x = fft[j]
                y = []
                for value in x:
                    if value > self.signal_threshold:
                        y.append(float(value))
                #print(y)

                fft_shifted = np.fft.fftshift(y)
                spectro = 10 * np.log10((fft_shifted))
                total_sum += sum(spectro)
                total_len += len(spectro)
                print(spectro)
        self.frequency_threshold = total_sum/total_len
        print(f"Frequency threshold set to {self.frequency_threshold}.\n")


    def print_binary_signal(self):
        fft_tmp, fft_shifted_tmp, spectro_tmp = self.do_fft(self.sample()) # sample data
        for i in range(10):
            fft = fft_tmp
            fft_tmp, fft_shifted_tmp, spectro_tmp = self.do_fft(self.sample()) # sample data
            for j in range(self.num_rows):
                x = fft[j] # row in fft
                freqs = np.fft.fftfreq(len(x))
                y = []
                for value in x:
                    if value > self.signal_threshold:
                        y.append(float(value))
                #print(y)

                fft_shifted = np.fft.fftshift(y)
                spectro = 10 * np.log10((fft_shifted))
                for x in spectro:
                    if x > self.frequency_threshold:
                        print("1")
                    else:
                        print("0")


    def extract_frequencies_stolen_code(self):

        fft, fft_shifted, spectro = self.do_fft(self.sample())  # sample data

        fs = int(2e6)  # Abtastrate (Hz)
        t = np.linspace(0, 1, fs, endpoint=False)  # Zeitachse

        fft_values = fft[1]
        freqs = np.fft.fftfreq(len(fft_values), 1 / fs)  # Frequenzachse
        magnitude = np.abs(fft_values)  # Betrag der FFT

        # Frequenzen extrahieren, die signifikante Werte haben
        threshold = np.max(magnitude) * 0.1  # Dynamische Schwelle (10% vom Maximum)
        detected_frequencies = freqs[magnitude > threshold]  # Nur relevante Frequenzen

        # Nur positive Frequenzen (da FFT symmetrisch ist)
        detected_frequencies = detected_frequencies[detected_frequencies > 0]

        # Ergebnis ausgeben
        print("Erkannte Frequenzen (Hz):", np.round(detected_frequencies, 2))

        # Frequenzspektrum visualisieren
        plt.figure(figsize=(10, 5))
        plt.plot(freqs[:len(freqs) // 2], magnitude[:len(magnitude) // 2])  # Nur positive Frequenzen plotten
        plt.xlabel("Frequenz (Hz)")
        plt.ylabel("Magnitude")
        plt.title("FFT-Spektrum")
        plt.grid()
        plt.savefig("test_spectrum.pdf", bbox_inches='tight')

'''
                #print(f"x array: {x}\n\n")
                print(y)
                idx = np.argmax(np.abs(y)) if len(y) > 0 else None
                freqs = np.fft.fftfreq(len(y))
                #print(freqs)
                '''

'''
    def calibrate_frequencies(self):
        print("Calibrating frequencies...\n")
        received_frequencies = []
        for i in range(5): # do 10 calibration steps
            fft, fft_shifted, spectro = self.do_fft(self.sample()) # sample data
            for j in range(self.num_rows): # loop over rows in fft
                idx = np.argmax(fft[j*self.num_rows])
                freqs = np.fft.fftfreq(len(fft_shifted))
                freq = freqs[idx]
            received_frequencies.append(freq)
            print(f"Frequency {freq} received.\n")
        self.frequency_threshold = sum(received_frequencies)/len(received_frequencies)
        print(f"Frequency threshold set to {self.frequency_threshold}.\n")
'''




if __name__ == "__main__":
    '''
    test_array = np.random.rand(2048)
    print(f"{test_array}\n length: {len(test_array)}")
    extract = test_array[(test_array>0.5)]
    print(f"{extract}\n length: {len(extract)}")
    '''

    decoder = Decoder()
    decoder.calibrate_signal_strength()
    #decoder.wait_for_user_input()
    decoder.calibrate_frequencies()
    decoder.print_binary_signal()
    print("Done.")