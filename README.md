# Hauptveränderungen:
    \T-TWR-master\lib\LilyGo_TWR_Library\src :
    
    - TWRClass.cpp 
    --TWRClass::routingWav
    
    \T-TWR-master\examples\Factory:

    - Factory.ino
    --loop()
    ---if (bitready) 

    - BLE.h
    --class BLECallback
    --- onWrite()

    - packed.h
    --Alles