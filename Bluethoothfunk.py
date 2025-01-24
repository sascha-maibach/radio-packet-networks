import asyncio
from bleak import BleakClient

# UUIDs müssen mit denen in BLE.h übereinstimmen
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
DEVICE_ADDRESS = "48:CA:43:31:41:09"  # Name oder MAC-Adresse des ESP32

async def send_string_to_device():
    async with BleakClient(DEVICE_ADDRESS) as client:
        if client.is_connected:
            print(f"Verbunden mit {DEVICE_ADDRESS}")

            # Sende mehrere Strings
            strings_to_send = ["Hallo ESP32", "Das ist ein Test", "BLE funktioniert!"]
            for text in strings_to_send:
                await client.write_gatt_char(CHARACTERISTIC_UUID, text.encode())
                print(f"Gesendet: {text}")
                await asyncio.sleep(1)  # Warte kurz zwischen den Nachrichten


async def send_wav_to_device(file_path):
    """Sendet eine WAV-Datei über Bluetooth an das T-TWR-Gerät."""
    try:
        async with BleakClient(DEVICE_ADDRESS) as client:
            if client.is_connected:
                print(f"Verbunden mit {DEVICE_ADDRESS}")

                # Öffne die WAV-Datei im Binärmodus
                with open(file_path, "rb") as wav_file:
                    print(f"Sende WAV-Datei: {file_path}")
                    while chunk := wav_file.read(512):  # Lese Daten in 512-Byte-Blöcken
                        await client.write_gatt_char(CHARACTERISTIC_UUID, chunk)
                        print(f"Gesendet: {len(chunk)} Bytes")
                        await asyncio.sleep(0.1)  # Kurze Pause zwischen den Blöcken

                # Markiere das Ende der Übertragung
                await client.write_gatt_char(CHARACTERISTIC_UUID, b"END_OF_WAV")
                print("Übertragung abgeschlossen.")
    except Exception as e:
        print(f"Fehler: {e}")

# Starte den asyncio-Eventloop
#asyncio.run(send_string_to_device())
file_path = "T-TWR-master/output2.wav"  # Pfad zur WAV-Datei
asyncio.run(send_wav_to_device(file_path))

