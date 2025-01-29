from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt

sdr = RtlSdr()
sdr.sample_rate = 9e6 # Hz
sdr.center_freq = 446.2e6   # Hz
sdr.freq_correction = 30  # PPM
#print(sdr.valid_gains_db)
sdr.gain = 49.6

def sample_from_sdr():
    
    
    fft_size = 512
    num_rows = 256
    #x = sdr.read_samples(2048) # get rid of initial empty samples
    samples = sdr.read_samples(fft_size*num_rows) # get all the samples we need for the spectrogram
    spectrogram = np.zeros((num_rows, fft_size))
    #print(x)
    for i in range(num_rows):
        #print(f"fft: {np.fft.fft(samples[i*fft_size:(i+1)*fft_size])}\n\n")
        #print(f"fft + fftshift:  {np.fft.fftshift(np.fft.fft(samples[i*fft_size:(i+1)*fft_size]))}\n\n")
        #print(f"fft + fftshift + abs + ^2:  {np.abs(np.fft.fftshift(np.fft.fft(samples[i*fft_size:(i+1)*fft_size])))**2}\n\n")
        #print(f"full: {10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(samples[i*fft_size:(i+1)*fft_size])))**2)}\n\n")
        spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(samples[i*fft_size:(i+1)*fft_size])))**2)

        #print(f"spectogram: {spectrogram[0]}")
    return spectrogram, samples


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
    spectrogram, samples = sample_from_sdr()
    samples_length = 0
    i = 0
    #while True:
    for x in range(3):
        print(f"iteration {i}")
        spectrogram_tmp, samples_tmp = sample_from_sdr()
        spectrogram = np.concatenate((spectrogram, spectrogram_tmp), axis=0)
        samples = np.concatenate((samples, samples_tmp), axis=0)
        min_val = 1e9
        max_val = 0
        print(len(spectrogram))
        for row in spectrogram:
            for elem in row:
                min_val = elem if elem < min_val else min_val
                max_val = elem if elem > max_val else max_val
        print(f"max: {max_val}   min: {min_val}")
        
        samples_length += len(samples)
        i += 1
    plot_spectrogram(spectrogram, get_extent(samples_length))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        