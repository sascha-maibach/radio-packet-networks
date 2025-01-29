from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

sdr = RtlSdr()
sdr.sample_rate = 2e6 # Hz
sdr.center_freq = 446.2e6 + 900   # Hz
sdr.freq_correction = 30  # PPM
#print(sdr.valid_gains_db)
sdr.gain = 49.6
average_max_signal_strength = 20
signal_found = False
signal_threshold = 2e9
freq_threshold = 0

def sample_from_sdr(calib):    
    fft_size = 512
    num_rows = 256
    samples = sdr.read_samples(2048) # get rid of initial empty samples
    samples = sdr.read_samples(fft_size*num_rows) # get all the samples we need for the spectrogram
    spectrogram = np.zeros((num_rows, fft_size))
    for i in range(num_rows):
        #check_signal(samples, i, fft_size)
        #print(f"fft: {np.fft.fft(samples[i*fft_size:(i+1)*fft_size])}\n\n")
        #print(f"fft + fftshift:  {np.fft.fftshift(np.fft.fft(samples[i*fft_size:(i+1)*fft_size]))}\n\n")
        #print(f"fft + fftshift + abs + ^2:  {np.abs(np.fft.fftshift(np.fft.fft(samples[i*fft_size:(i+1)*fft_size])))**2}\n\n")
        #print(f"full: {10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(samples[i*fft_size:(i+1)*fft_size])))**2)}\n\n")
        spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(samples[i*fft_size:(i+1)*fft_size])))**2)
        if calib:
            calibrate(spectrogram, i, fft_size)
        else:
            check_signal_with_spectrogram(samples, i, fft_size)

        #print(f"spectogram: {spectrogram[0]}")
    return spectrogram, samples

def check_signal_with_spectrogram(samples, i, fft_size):
    
    fft = np.fft.fft(samples[i*fft_size:(i+1)*fft_size])
    fft_shift = np.fft.fftshift(fft)
    if max(fft) > signal_threshold: 
        idx = np.argmax(np.abs(fft))        
        freqs = np.fft.fftfreq(len(fft_shift))
        freq = freqs[idx]
        
        if freq > freq_threshold:
            print("1")
        else:
            print("0")

def calibrate(samples, i, fft_size):
    print("calibrating..")
    global freq_list
    global freq_threshold
    global signal_threshold
    fft = np.fft.fft(samples[i*fft_size:(i+1)*fft_size])
    fft_shift = np.fft.fftshift(fft)
    detect_signal_threshold(fft)
    
    if max(fft) > signal_threshold: 
        idx = np.argmax(np.abs(fft))        
        freqs = np.fft.fftfreq(len(fft_shift))
        freq = freqs[idx]
        freq_list.append(freq)
        if freq_list.size() == 9:
            freq_threshold = sum(freq_list) / freq_list.size()
            print(freq_threshold)
    
def detect_signal_threshold(fft):
    global average_max_signal_strength
    global signal_threshold
    global signal_found
    
    old_average = average_max_signal_strength
    average_max_signal_strength = 0.8*average_max_signal_strength + 0.2*max(fft)
    if (average_max_signal_strength - old_average > 0.5*old_average and not signal_found):
        signal_threshold = 2*old_average

def check_signal(samples, i, fft_size):
    global signal_threshold
    global average_max_signal_strength
    global signal_found
    global average_zero_freq
    global average_one_freq
    
    
    fft = np.fft.fft(samples[i*fft_size:(i+1)*fft_size])
    fft_shift = np.fft.fftshift(fft)
    
    
    
    old_average = average_max_signal_strength
    average_max_signal_strength = 0.8*average_max_signal_strength + 0.2*max(fft)
    if max(fft) > signal_threshold: 
        idx = np.argmax(np.abs(fft))        
        freqs = np.fft.fftfreq(len(fft_shift))
        freq = freqs[idx]
        print(freq)
        
        if freq > 0:
            # likely frequency of 1, e.g. > 456,200,900
            print("1")
        else:
            # frequency of 0
            print("0")
            
        '''
        if abs(freq - average_zero_freq) < average_zero_freq * 0.1:  # Wenn neue stärkste frequenz maximal 10% von 0 frequenz abweicht            
            average_zero_freq = 0.8*average_zero_freq + 0.2*((freq + 1) * 448.2e6)/1e6
            print(f"average 0 freq: {average_zero_freq} Hz")
        else:
            average_one_freq = 0.8*average_one_freq + 0.2*((freq + 1)* 448.2e6 )/1e6
            print(f"average 1 freq: {average_one_freq} Hz")
            '''
        

        
        print(f"old average: {average_max_signal_strength}\n")
        print(f"new average: {average_max_signal_strength}\n")
        print("SIGNAL DETECTED!\n\n")
        
        
        
        samples = sdr.read_samples(512*1024)
        fft_1kk = np.abs(np.fft.fftshift(np.fft.fft(samples[:512])))
        plt.plot(fft_1kk)
        
        plt.savefig("double_signal_found.pdf", bbox_inches='tight')
        plt.close()
                
        S_mag = np.abs(fft)
        plt.plot(S_mag,'.-')
        plt.savefig("test_fft.pdf", bbox_inches='tight')
        plt.close()
        plt.plot(np.abs(abs(np.fft.fftshift(fft))))
        plt.savefig("test_fft_shift.pdf", bbox_inches='tight')
        plt.close()
        signal_found = True 
        
        
    elif(average_max_signal_strength - old_average < -0.5*old_average):        
        print(f"old average: {average_max_signal_strength}\n")
        print(f"new average: {average_max_signal_strength}\n")
        print("SIGNAL LOST\n\n")
        signal_found = False
        

    
def get_extent(samples_length):
       return [(sdr.center_freq + sdr.sample_rate/-16)/1e6,
            (sdr.center_freq + sdr.sample_rate/16)/1e6,
            samples_length/sdr.sample_rate, 0]
    



def plot_spectrogram(spectrogram, extent):
    plt.plot(spectrogram[0])
    plt.savefig("images/spectro_graph.pdf", bbox_inches='tight')
    plt.close()
    plt.imshow(spectrogram, aspect='auto', extent=extent)
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("Time [s]")
    plt.savefig("images/spectogram.pdf", bbox_inches='tight')
    plt.close()
    

def sync_found(spectrogram):
    pass
    

    
if __name__ == "__main__":
    print("receiver starting")
    max_signal_strength = 0
    for i in range(100):
        
        spectrogram, samples_tmp = sample_from_sdr(1)
        
    while True:
    #for x in range(3):
        spectrogram, samples_tmp = sample_from_sdr(0)
        # print(spectrogram)
            
            
        #sleep(0.5)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        