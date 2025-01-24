# 1 "C:\\Users\\Alphe\\AppData\\Local\\Temp\\tmpn82ivhv4"
#include <Arduino.h>
# 1 "C:/Users/Alphe/Desktop/Uni/Radio Packet Network/radio-packet-networks/T-TWR-master/examples/Factory/Factory.ino"
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

#define DECLARE_DEMO(function) void function(uint8_t menuSelect)
#define U8G2_HOR_ALIGN_CENTER(t) ((u8g2.getDisplayWidth() - (u8g2.getUTF8Width(t))) / 2)
#define U8G2_HOR_ALIGN_RIGHT(t) (u8g2.getDisplayWidth() - u8g2.getUTF8Width(t))

using namespace ace_button;

U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);


int bitpack[512];
bool bitready = false;

List list;

uint8_t wavBuffer[1024 * 50];

size_t wavIndex = 0;
bool wavFileReady = false;
void setup();
void loop();
void setupOLED(uint8_t addr);
void playMessage(uint8_t pin, uint8_t channel, uint8_t message[]);
#line 37 "C:/Users/Alphe/Desktop/Uni/Radio Packet Network/radio-packet-networks/T-TWR-master/examples/Factory/Factory.ino"
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

            int array[64];

            try {
                uint8_t cont[5] = {0,1,0,1,0};
                for (int i = 0; i<5; i++) {

                    playMessage(ESP2SA868_MIC, 0, cont);

                }
            }catch (const std::exception& e) {
                Serial.print("Error in list.get() oder im senden\n");
            }
            if(list.getHead() == nullptr){
                bitready == false;
            }
        }

}



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
    Serial.print("In Play Message\r\n");
    ledcAttachPin(pin, channel);
    int length = sizeof(message)/sizeof(message[0]);
    Serial.printf("message length: %d", length);
    for (uint8_t i = 0; i < length; i++) {
        Serial.print("in playmessage loop: \r\n");
        Serial.printf("message[i]: %d",message[i]);
        if (message[i] == 0) {
            Serial.print("play 0");
            ledcWriteTone(channel, 100);
            delay(1000);
        } else {
            Serial.print("play else");
            ledcWriteTone(channel, 200);
            delay(1000);
        }
        delay(250);
    }
    ledcDetachPin(pin);
}