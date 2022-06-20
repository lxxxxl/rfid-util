#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN D0 // Configurable, see typical pin layout above
#define SS_PIN D8  // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance.


// buffer for outgoing data
byte g_buffer_tx[20];

// buffer for incomming command
byte g_buffer_rx[20];
// count of bytes already received
byte g_buffer_rx_count = 0;
// if cmd fully received?
bool g_buffer_rx_cmd_received = false;

MFRC522::StatusCode status;

// default (hardcoded) key
MFRC522::MIFARE_Key key = {0xff, 0xff, 0xff, 0xff, 0xff, 0xff};

enum Command
{
  IDLE            = 0x00,
  READ_UID        = 0x31,   // '1'
  WRITE_UID       = 0x32,   // '2'
  READ_DATA       = 0x33,   // '3'
  WRITE_DATA      = 0x34,   // '4'
  VERSION_CHECK   = 0x39    // '?'
};

Command g_cmd;      // incoming command code
//char buf[128]; // incoming command args

/*
 * Initialize.
 */
void setup()
{
  Serial.begin(9600); // Initialize serial communications with the PC
  SPI.begin();        // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522 card

}

void dump_byte_array(byte *buffer, byte bufferSize)
{
  for (byte i = 0; i < bufferSize; i++)
  {
    Serial.printf(" %02X", buffer[i]);
  }
  Serial.println();
}

/*
 * Try using the PICC (the tag/card) with the given key to access block 0 to 63.
 * On success, it will show the key details, and dump the block data on Serial.
 *
 * @return true when the given key worked, false otherwise.
 */

bool try_dump_with_key(MFRC522::MIFARE_Key *key)
{
  bool result = false;

  for (byte block = 0; block < 64; block++)
  {

    // Serial.println(F("Authenticating using key A..."));
    status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, key, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK)
    {
      return false;
    }

    // Read block
    byte byteCount = sizeof(g_buffer_tx);
    status = mfrc522.MIFARE_Read(block, g_buffer_tx, &byteCount);
    if (status != MFRC522::STATUS_OK)
    {
      return false;
    }
    else
    {
      // Successful read
      result = true;
      // Dump block data
      Serial.printf("3 B%02d:", block);
      dump_byte_array(g_buffer_tx, 16);
      Serial.println();
    }
  }
  mfrc522.PICC_HaltA();      // Halt PICC
  mfrc522.PCD_StopCrypto1(); // Stop encryption on PCD
  return result;
}

void uid_read()
{
//  Serial.println("Insert card...");
  // Wait for new cards
  if (!mfrc522.PICC_IsNewCardPresent())
    return;

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial())
    return;

  // Show some details of the PICC (that is: the tag/card)
  Serial.print("1 UID:");
  dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.print("1 Type: ");
  //MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  Serial.println(mfrc522.PICC_GetTypeName(mfrc522.PICC_GetType(mfrc522.uid.sak)));
  //uid_size = mfrc522.uid.size;
  //memcpy(uid, mfrc522.uid.uidByte, uid_size);
  g_cmd = Command::IDLE;
}

void uid_write()
{
  // Wait for new cards
  while (!mfrc522.PICC_IsNewCardPresent())
    return;

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial())
    return;

  // set new UID
  // https://github.com/miguelbalboa/rfid/blob/master/examples/ChangeUID/ChangeUID.ino


  mfrc522.PICC_HaltA();
  g_cmd = Command::IDLE;

}

void card_dump()
{
  // Wait for new cards
  if (!mfrc522.PICC_IsNewCardPresent())
    return;

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial())
    return;

  // Show some details of the PICC (that is: the tag/card)
  Serial.print("1 UID:");
  dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.print("1 Type: ");
  Serial.println(mfrc522.PICC_GetTypeName(mfrc522.PICC_GetType(mfrc522.uid.sak)));

  // Try dump with known default key
  if (try_dump_with_key(&key))
  {
    Serial.println("3 Done");
  }
  else
  {
    Serial.println("3 Fail");
  }

  g_cmd = Command::IDLE;
}

void card_write()
{
  // Wait for new cards
  if (!mfrc522.PICC_IsNewCardPresent())
    return;

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial())
    return;

  MFRC522::StatusCode status;

  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, g_buffer_rx[1], &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK)
  {
    // Serial.print(F("PCD_Authenticate() failed: "));
    // Serial.println(mfrc522.GetStatusCodeName(status));
    Serial.println("4 Fail");
    return;
  }

  // Write data to the block
  // Serial.print(F("Writing data into block ")); Serial.print(g_buffer_rx[1]);
  // Serial.println(F(" ..."));
  // dump_byte_array(&g_buffer_rx[2], 16); Serial.println();
  status = mfrc522.MIFARE_Write(g_buffer_rx[1], &g_buffer_rx[2], 16);
  if (status != MFRC522::STATUS_OK)
  {
    // Serial.print(F("MIFARE_Write() failed: "));
    // Serial.println(mfrc522.GetStatusCodeName(status));
    Serial.println("4 Fail");
  }
  Serial.println("4 Done");

  // Halt PICC
  mfrc522.PICC_HaltA();
  // Stop encryption on PCD
  mfrc522.PCD_StopCrypto1();
  
  g_cmd = Command::IDLE;
}

void version_check(){
  Serial.println("rfid-util-1");
  g_cmd = Command::IDLE;
}

void send_command_ack()
{
  Serial.print(char(g_cmd));
  Serial.println(" OK");
}

/*
 * Main loop.
 */
void loop()
{

  byte len = Serial.available();
  if (len > 0 && (g_buffer_rx_count + len) <= 20)
  {
    Serial.readBytes(&g_buffer_rx[g_buffer_rx_count], len);
    g_buffer_rx_count += len;
    // check if we received full command
    if (g_buffer_rx[g_buffer_rx_count-1] == 0x0A && g_buffer_rx[g_buffer_rx_count-2] == 0x0D)
    {
      g_buffer_rx_cmd_received = true;
      g_cmd = (Command)g_buffer_rx[0];
      send_command_ack();
      g_buffer_rx_count = 0;
    }
    else
    {
      g_buffer_rx_cmd_received = false;
    }
  }

  // return if command received patrially
  if (!g_buffer_rx_cmd_received)
  {
    return;
  }

  

  if (g_cmd == Command::READ_UID)
  {
    uid_read();
  }

  else if (g_cmd == Command::WRITE_UID)
  {
    uid_write();
  }

  else if (g_cmd == Command::READ_DATA)
  {
    card_dump();
  }

  else if (g_cmd == Command::WRITE_DATA)
  {
    card_write();
  }

  else if (g_cmd == Command::VERSION_CHECK)
  {
    version_check();
  }

  delay(50);
}