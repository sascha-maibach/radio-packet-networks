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

