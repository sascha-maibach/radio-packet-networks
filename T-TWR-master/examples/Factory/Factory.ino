#include "packet.h"
#include "LilyGo_TWR.h"


#include <BLEServer.h>
#include "BLE.h"

#include <AceButton.h>
#include <Rotary.h>

#include "Constants.h"

#include "fix_fft.h"
#include <U8g2lib.h>

#define DEBUG_PORT Serial 

#define DECLARE_DEMO(function)      void function(uint8_t menuSelect)
#define U8G2_HOR_ALIGN_CENTER(t)    ((u8g2.getDisplayWidth() - (u8g2.getUTF8Width(t))) / 2)
#define U8G2_HOR_ALIGN_RIGHT(t)     (u8g2.getDisplayWidth()  -  u8g2.getUTF8Width(t))

using namespace ace_button;

U8G2_SH1106_128X64_NONAME_F_HW_I2C  u8g2(U8G2_R0, U8X8_PIN_NONE);


int bitpack[512];
bool bitready = false;

List list;

uint8_t wavBuffer[1024 * 50];
//double fskArray[1024 * 50];  // Puffer für WAV-Datei
size_t wavIndex = 0;            // Aktueller Index im Puffer
bool wavFileReady = false;    

void setup() {

    bool rslt = false;


    #ifdef DEBUG_PORT
        DEBUG_PORT.begin(115200);
    #endif

    rslt = twr.begin();

    while (!rslt) {
        DBG("PMU communication failed..");
        delay(1000);
    }

    radio.setPins(SA868_PTT_PIN, SA868_PD_PIN);
    rslt = radio.begin(RadioSerial, twr.getBandDefinition());
    Serial.print(twr.getBandDefinition());
    uint8_t addr = twr.getOLEDAddress();
    if ((addr != 0x3C || addr != 0x3D) && !rslt) {
        // Initialize display
        u8g2.setI2CAddress(addr << 1);
        u8g2.begin();
        u8g2.clearBuffer();
        u8g2.setFont(u8g2_font_tenstamps_mu);
        u8g2.setCursor(30, 28);
        u8g2.print("SA8X8");
        u8g2.setCursor(22, 52);
        u8g2.print("FAILED");
        u8g2.sendBuffer();
    }

    while (!rslt) {
        DBG("SA8x8 communication failed, please use ATDebug to check whether the module responds normally..");
    }

    setupOLED(addr);
    delay(3000);

    BLE::enableBLE();
}

void loop() {
    if (bitready) {
            //Serial.print("bip\n");
            int array[64];

            try {
                uint8_t* cont = list.get();
                int length = sizeof(cont)/sizeof(cont[0]);
                playBarker(ESP2SA868_MIC, 0); //zur erkennung und synkronisation
                for (int i = 0; i<length; i++) {                
                    //twr.routingWav(array, 64, 44100);
                    radio.transmit();
                    playMessage(ESP2SA868_MIC, 0, cont);
                    radio.receive();
                }
            }catch (const std::exception& e) {
                Serial.print("Error in list.get() oder im senden\n");
            }
            if(list.getHead() == nullptr){
                bitready == false;
            }
        }

}

//========Helper Funktions=================

void setupOLED(uint8_t addr)
{
    u8g2.setI2CAddress(addr << 1);
    u8g2.begin();
    u8g2.clearBuffer();
    u8g2.setContrast(10);
    uint8_t b = 10;
    u8g2.firstPage();
    do {
        do {
            u8g2.setFont(u8g2_font_tenstamps_mu);
            u8g2.drawXBM(40, 0, 48, 48, xbmLOGO);
            u8g2.setCursor(22, 62);
            u8g2.print("LILYGO");
            u8g2.sendBuffer();
            u8g2.setContrast(b);
        } while (u8g2.nextPage());
        b += 10;
        delay(8);
    } while (b < twr.pdat.dispBrightness);
}


void playMessage(uint8_t pin, uint8_t channel, uint8_t message[])
{
    ledcAttachPin(pin, channel);

    int length = sizeof(message)/sizeof(message[0]);
    uint8_t bits[length*8];
    bits = IntToBinary(message, bits); // könnte bits falsch speichern... bein test darauf achten
    
    for (uint8_t i = 0; i < length; i++) {
        Serial.printf("inhalt von bits[i]: %d",bits[i]);
        if (bits[i] == 0) {
            ledcWriteTone(channel, 100);
            //delay(750);
        } else {
            ledcWriteTone(channel, 500);
            //delay(750);
        }
        //delay(250);
    }
    ledcDetachPin(pin);
}

//Sendet einen Barker code der länge 7.
void playBarker(uint8_t pin, uint8_t channel)
{
    ledcAttachPin(pin, channel);
    ledcWriteTone(channel, 500); //1
    ledcWriteTone(channel, 500); //1
    ledcWriteTone(channel, 500); //1
    ledcWriteTone(channel, 100); //0
    ledcWriteTone(channel, 100); //0
    ledcWriteTone(channel, 500); //1
    ledcWriteTone(channel, 100); //0
    ledcDetachPin(pin);
    Serial.printf("Barker code send \r\n");
}

//nimmt die message und erstellt ein weiteres array indem die einzelnen bits der integer gespeichert werden. Zur weiterversendung.
uint8_t* IntToBinary(uint8_t* messages, uint8_t* bits)
{
    int length = sizeof(messages)/sizeof(messages[0]);

    for (int i = 0; i < length*8; i = i + 8) 
    {
        // Extrahiere Bit 
        bits[i] = messages[i] & 0b00000001; 
        bits[i+1] = (messages[i]& 0b00000010) >> 1; 
        bits[i+2] = (messages[i] & 0b00000100) >> 2;
        bits[i+3] = (messages[i] & 0b00001000) >> 3;
        bits[i+4] = (messages[i] & 0b00010000) >> 4;
        bits[i+5] = (messages[i] & 0b00100000) >> 5;
        bits[i+6] = (messages[i] & 0b01000000) >> 6;
        bits[i+7] = (messages[i] & 0b10000000) >> 7;

    } 
    return bits;
}