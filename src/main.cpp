#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 22 // Configurable, see typical pin layout above
#define SS_PIN 21  // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance.

byte buffer[18];
byte block;
MFRC522::StatusCode status;

MFRC522::MIFARE_Key key;

byte uid[10];
byte uid_size;

// Number of known default keys (hard-coded)
// NOTE: Synchronize the NR_KNOWN_KEYS define with the defaultKeys[] array
#define NR_KNOWN_KEYS 1
// Known keys, see: https://code.google.com/p/mfcuk/wiki/MifareClassicDefaultKeys
byte knownKeys[NR_KNOWN_KEYS][MFRC522::MF_KEY_SIZE] = {
    {0xff, 0xff, 0xff, 0xff, 0xff, 0xff}, // FF FF FF FF FF FF = factory default
};

char cmd;      // incoming command code
//char buf[128]; // incoming command args

/*
 * Initialize.
 */
void setup()
{
  Serial.begin(9600); // Initialize serial communications with the PC
  SPI.begin();        // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522 card


  Serial.println("1. Read UID");
  Serial.println("2. Write UID");
  Serial.println("3. Dump data");
}

void dump_byte_array(byte *buffer, byte bufferSize)
{
  for (byte i = 0; i < bufferSize; i++)
  {
    Serial.printf(" %02X", buffer[i]);
  }
}

/*
 * Try using the PICC (the tag/card) with the given key to access block 0 to 63.
 * On success, it will show the key details, and dump the block data on Serial.
 *
 * @return true when the given key worked, false otherwise.
 */

bool try_key(MFRC522::MIFARE_Key *key)
{
  bool result = false;

  for (byte block = 0; block < 64; block++)
  {

    // Serial.println(F("Authenticating using key A..."));
    status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, key, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK)
    {
      Serial.print("PCD_Authenticate() failed: ");
      Serial.println(mfrc522.GetStatusCodeName(status));
      return false;
    }

    // Read block
    byte byteCount = sizeof(buffer);
    status = mfrc522.MIFARE_Read(block, buffer, &byteCount);
    if (status != MFRC522::STATUS_OK)
    {
      Serial.print("MIFARE_Read() failed: ");
      Serial.println(mfrc522.GetStatusCodeName(status));
    }
    else
    {
      // Successful read
      // result = true;
      // Serial.print(F("Success with key:"));
      // dump_byte_array((*key).keyByte, MFRC522::MF_KEY_SIZE);
      // Serial.println();

      // Dump block data
      Serial.printf("Block %02d:", block);
      dump_byte_array(buffer, 16);
      Serial.println();
    }
  }
  Serial.println();
  mfrc522.PICC_HaltA();      // Halt PICC
  mfrc522.PCD_StopCrypto1(); // Stop encryption on PCD
  return result;
}

void uid_read()
{
  Serial.println("Insert card...");
  // Wait for new cards
  while (!mfrc522.PICC_IsNewCardPresent())
    delay(50);

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial())
    return;

  // Show some details of the PICC (that is: the tag/card)
  Serial.print("Card UID:");
  dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.println();
  Serial.print("PICC type: ");
  MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  Serial.println(mfrc522.PICC_GetTypeName(piccType));
  uid_size = mfrc522.uid.size;
  memcpy(uid, mfrc522.uid.uidByte, uid_size);
}

void uid_write()
{
  Serial.println("Insert card...");
  // Wait for new cards
  while (!mfrc522.PICC_IsNewCardPresent())
    delay(50);

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial())
    return;

  // TODO
  // https://github.com/miguelbalboa/rfid/blob/master/examples/ChangeUID/ChangeUID.ino
}

void card_dump()
{
  Serial.println("Insert card...");
  // Wait for new cards
  while (!mfrc522.PICC_IsNewCardPresent())
    delay(50);

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial())
    return;

  // Show some details of the PICC (that is: the tag/card)
  Serial.print("Card UID:");
  dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.println();
  Serial.print("PICC type: ");
  MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  Serial.println(mfrc522.PICC_GetTypeName(piccType));

  // Try the known default keys
  MFRC522::MIFARE_Key key;
  for (byte k = 0; k < NR_KNOWN_KEYS; k++)
  {
    // Copy the known key into the MIFARE_Key structure
    for (byte i = 0; i < MFRC522::MF_KEY_SIZE; i++)
    {
      key.keyByte[i] = knownKeys[k][i];
    }
    // Try the key
    if (try_key(&key))
    {
      // Found and reported on the key and block,
      // no need to try other keys for this PICC
      break;
    }
  }
}

void version_check(){
  Serial.println("rfid-util-1");
}

/*
 * Main loop.
 */
void loop()
{
  cmd = Serial.read();

  if (cmd == '1')
  {
    Serial.println("Read card UID");
    uid_read();
  }

  else if (cmd == '2')
  {
    Serial.println("Write card UID");
    uid_write();
  }

  else if (cmd == '3')
  {
    Serial.println("Dump card data");
    card_dump();
  }

  else if (cmd == '9')
  {
    version_check();
  }

  delay(50);
}