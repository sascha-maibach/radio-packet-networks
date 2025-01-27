from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt

BARKER_CODE = np.array([1, 1, 1, 0, 0, 1, 0])

sdr = RtlSdr()
sdr.sample_rate = 1.2e6  
sdr.center_freq = 446.2e6
sdr.freq_correction = 30 
sdr.gain = 49.6

fft_size = 512
num_rows = 1
sdr.read_samples(2048)  
samples = sdr.read_samples(fft_size * num_rows)

spectrogram = np.zeros((num_rows, fft_size))
for i in range(num_rows):
    fft_result = np.fft.fft(samples[i * fft_size:(i + 1) * fft_size])
    spectrogram[i, :] = 10 * np.log10(np.abs(np.fft.fftshift(fft_result))**2)

extent = [
    (sdr.center_freq + sdr.sample_rate / -4) / 1e6,
    (sdr.center_freq + sdr.sample_rate / 4) / 1e6,
    len(samples) / sdr.sample_rate, 
    0
]

plt.imshow(spectrogram, aspect='auto', extent=extent)
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [s]")
plt.title("Spectrogram")
plt.savefig("images/spectrogram.pdf", bbox_inches='tight')
plt.close()

def find_barker(signal, barker_code):
    code_len = len(barker_code)
    correlation = np.correlate(signal > 0, barker_code, mode='valid')
    positions = np.where(correlation == code_len)[0]
    return positions

def extract_binary(signal, barker_positions, bit_length=512):
    binary_data = []
    for pos in barker_positions:
        start = pos + len(BARKER_CODE)
        binary_segment = signal[start:start + bit_length]
        binary_data.append((binary_segment > 0).astype(int))
    return binary_data

barker_positions = find_barker(samples, BARKER_CODE)
print(f"Gefundene Barker-Positionen: {barker_positions}")

binary_data = extract_binary(samples, barker_positions)
print(f"Erste Binärdaten: {binary_data[0] if binary_data else 'Keine Daten gefunden'}")
