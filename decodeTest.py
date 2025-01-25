import numpy as np

def wavToArray(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    array = np.frombuffer(raw_data, dtype=np.uint8)

    return array

#Pe Test Prep:

file_path = "T-TWR-master/output2.wav" 

data = wavToArray(file_path)
print("Erster Teil des Arrays:", data[:20])
print("Länge des Arrays:", len(data))