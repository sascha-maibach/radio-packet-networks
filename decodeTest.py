import numpy as np

def wavToArray(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    array = np.frombuffer(raw_data, dtype=np.uint8)

    return array

def intToBinary(messages):
    length = len(messages)
    bits = [0] * (length * 8)
    for i in range(length):
        bits[i * 8] = messages[i] & 0b00000001
        bits[i * 8 + 1] = (messages[i] & 0b00000010) >> 1
        bits[i * 8 + 2] = (messages[i] & 0b00000100) >> 2
        bits[i * 8 + 3] = (messages[i] & 0b00001000) >> 3
        bits[i * 8 + 4] = (messages[i] & 0b00010000) >> 4
        bits[i * 8 + 5] = (messages[i] & 0b00100000) >> 5
        bits[i * 8 + 6] = (messages[i] & 0b01000000) >> 6
        bits[i * 8 + 7] = (messages[i] & 0b10000000) >> 7
    
    return bits
        
def barker(message):
    barker = np.array([1,1,1,0,0,1,0])
    message = np.insert(message, 0, barker, axis=0)
    return message

def packet(data):
    packetList = []
    j = 0
    for i in range(0,len(data),512):
        if i > len(data):
            packetList.append(data[i:])
        elif i == 0:
            packetList.append(data[:512])
        else:
            packetList.append(data[i:i+512])
        j =+ 1 
    return packetList

def toSendPaked(list):
    for i in range(len(list)):
        list[i] = barker(list[i])
    return list

#Pe Test Prep:

file_path = "T-TWR-master/output2.wav" 

data = wavToArray(file_path)
print("Erster Teil des Arrays:", data[:20])
print("Länge des Arrays:", len(data))

print("packet test:")
test = packet(data)
#print(test[:10])

print("to binary test:") 
btest = intToBinary(test)
print(btest[:10])

print("add barker test")
bbtest = toSendPaked(btest)
print(bbtest[:10])

print("Packeges ready for decoding")

#===================================================================

from scipy.io.wavfile import write

import numpy as np
from scipy.io.wavfile import write


amplitude = 32767  
audio_signal = np.array([amplitude if bit == 1 else amplitude/2 for bit in bbtest[0]], dtype=np.int16)


samples_per_bit = 4410
audio_signal = np.repeat(audio_signal, samples_per_bit)


sample_rate = 44100  
write("binary_audio.wav", sample_rate, audio_signal)

print("The test audio was created!")

#==================================================================
import wave

BARKER_CODE = np.array([1, 1, 1, 0, 0, 1, 0])

def wav_to_array(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        raw_data = wav_file.readframes(wav_file.getnframes())
        return np.frombuffer(raw_data, dtype=np.int16)  

def find_barker(signal, barker_code, threshold=0.9):
  
    code_len = len(barker_code)
    positions = []

    for i in range(len(signal) - code_len + 1):
        window = signal[i:i + code_len] > 0 
        similarity = np.mean(window == barker_code)
        if similarity >= threshold:
            positions.append(i)

    return positions

def extract_packets(signal, barker_positions, packet_size=512):
    packets = []
    for pos in barker_positions:
        start = pos + len(BARKER_CODE)
        end = start + packet_size
        packets.append(signal[start:end])
    return packets

def decode_binary(packet):
    byte_array = np.packbits(packet.astype(np.uint8))
    return byte_array.tobytes()


file_path = "binary_audio.wav"

signal = wav_to_array(file_path)
print("Signalgröße:", len(signal))

barker_positions = find_barker(signal, BARKER_CODE)
print("Gefundene Barker-Positionen:", barker_positions)

packets = extract_packets(signal, barker_positions)
print(f"Anzahl der Pakete: {len(packets)}")

decoded_data = [decode_binary(packet) for packet in packets]

print("Erstes dekodiertes Paket (als Bytes):", decoded_data[0])
