/**
 * @file      ble.cpp
 * @author    Lewis He (lewishe@outlook.com)
 * @license   MIT
 * @copyright Copyright (c) 2023  Shenzhen Xinyuan Electronic Technology Co., Ltd
 * @date      2023-12-05
 * @note      Bluetooth has no function, just broadcasting
 */
#pragma once

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Arduino.h>
#include <math.h>

extern uint8_t wavBuffer[];
extern size_t wavIndex;
extern bool wavFileReady;
extern double fskArray[];


#define MAX_WAV_SIZE 1024 * 50
#define BLE_SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define BLE_CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define BLE_DEVICE_NAME         "T-TWR"



class BLECallback : public BLECharacteristicCallbacks {

public:
    void onWrite(BLECharacteristic *pCharacteristic) override {
        // Empfangene Daten auslesen
        std::string value = pCharacteristic->getValue();

        if (value.length() > 0) {
            // Daten in den Puffer schreiben
            size_t length = value.length();
            if (wavIndex + length < MAX_WAV_SIZE) {
                memcpy(&wavBuffer[wavIndex], value.c_str(), length);
                wavIndex += length;

                Serial.print("Empfangene Daten: ");
                Serial.print(length);
                Serial.println(" Bytes");
            } else {
                Serial.println("Pufferüberlauf! WAV-Datei zu groß.");
            }
        }

        // Wenn WAV-Daten vollständig, starte Funkübertragung
        if (isEndOfWav(value)) {
            Serial.println("WAV-Datei vollständig empfangen. Bearbeite...");
            //fsk_modulation(wavBuffer, fskArray);
            wavFileReady = true;
            wavIndex = 0; // Puffer zurücksetzen
        }
    }

    // Überprüft, ob die empfangenen Daten das Ende der WAV-Datei markieren
    bool isEndOfWav(const std::string &data) {
        return data.find("END_OF_WAV") != std::string::npos; // Beispiel-Ende-Markierung
    }

    // Funkübertragung der WAV-Daten
    void sendWavOverRadio(const uint8_t *data, size_t length) {
        // Beispiel: Funkübertragung implementieren (z. B. LoRa, WiFi)
        Serial.print("Übertrage ");
        Serial.print(length);
        Serial.println(" Bytes über Funk.");
        // Hier Funk-API einfügen (z. B. LoRa-Sendung)
    }

    void fsk_modulation(uint8_t binary_array[], double* fskArray) {
        int Fs = 1000; // Samples per second
        int fc = 30; // carrier freq 30 Hz
        int T = 1; // simulation time in seconds

        Serial.print("vor devide");
        Serial.print(T);
        Serial.print(Fs);
        int size = T/(1/Fs);
        int array[size];
        int index = 0;
        Serial.print("Erster loop:");
        for (int i = 0; i < T; i + 1/Fs) {
            array[index] = i;
            Serial.printf("round: %i",i);
        }
        Serial.print("End of loop");
        double Td = 0.1; // bit duration
        int Nsamples = int(Td*Fs);

        int Nsym = int(floor(size/Nsamples));

        int n = sizeof(binary_array) / sizeof(binary_array[0]);
        double f[n];
        Serial.print("Zweiter loop:");
        for (int i = 0; i<n; i++) {
            f[i] = fc + fc*binary_array[i]/2;
            Serial.printf("round: %i",i);
        }
        Serial.print("End of loop");

        Serial.print("Dritter loop:");
        for (int i = 0; i<size; i++) {
            fskArray[i] = sin(2*M_PI*f[i]*array[i]);
            Serial.printf("round: %i",i);
        }
        Serial.print("End of loop");

    }
};

class BLE
{
public:
    static bool isRunning()
    {
        return _started;
    }

    static const char *getDevName()
    {
        return BLE_DEVICE_NAME;
    }

    static void enableBLE()
    {
        if (_started) {
            return;
        }
        _started = true;

        BLEDevice::init(BLE_DEVICE_NAME);
        BLEDevice::setMTU(512);
        BLEServer *pServer = BLEDevice::createServer();

        pServer->setCallbacks(new BLEServerCallbacks());

        BLEService *pService = pServer->createService(BLE_SERVICE_UUID);
        /*BLECharacteristic *pCharacteristic = */
        BLECharacteristic *pCharacteristic = pService->createCharacteristic(
            BLE_CHARACTERISTIC_UUID,
            BLECharacteristic::PROPERTY_READ |
            BLECharacteristic::PROPERTY_WRITE |
            BLECharacteristic::PROPERTY_WRITE_NR
        );

        pCharacteristic->setCallbacks(new BLECallback());

        pService->start();


        BLEAdvertising *pAdvertising = pServer->getAdvertising();  // this still is working for backward compatibility
        //BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
        pAdvertising->addServiceUUID(BLE_SERVICE_UUID);
        pAdvertising->setScanResponse(true);
        pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
        pAdvertising->setMinPreferred(0x12);
        pServer->setCallbacks(new BLEServerCallbacks());
        BLEDevice::startAdvertising();

        Serial.println(F("BLE-Werbung gestartet"));
        Serial.print(F("BLE-Gerätename: "));
        Serial.println(BLE_DEVICE_NAME);
        Serial.print(F("BLE-Adresse: "));
        Serial.println(BLEDevice::getAddress().toString().c_str());
    }

    static void disableBLE()
    {
        if (_started) {
            BLEDevice::deinit(false);
        }
        _started = false;
    }


private:
    static  bool _started ;
};
bool BLE::_started = false;