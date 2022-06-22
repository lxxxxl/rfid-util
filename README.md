# rfid-util
Utility to read/write RFID cards based on ESP32/ESP8266 and RFID-MFRC522 board.

## Assembly
Pins:  
|ESP8266| ESP32 | MFRC522                    |
|-------|-------|----------------------------|
| 16    | 21    | SDA (SS)                   |
| 14    | 18    | SCK                        |
| 13    | 23    | MOSI                       |
| 12    | 19    | MISO                       |
| GND   | GND   | GND                        |
| 11    | 22    | RST                        |
| 3v3   | 3v3   | 3v3                        |
