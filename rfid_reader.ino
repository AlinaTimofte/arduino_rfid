#include <MFRC522.h>
#include <SPI.h>

//definesc led-urile rosu si verde pentru estetica codului
#define LED_RED_PIN 7
#define LED_GREEN_PIN 6

//definesc pini pentru sda si reset
//..
#define SDA_RFID_PIN 10
#define RST_RFID_PIN 9
//vreau sa-mi creez un obiect pe baza librariei MFRC522
MFRC522 RFID(SDA_RFID_PIN, RST_RFID_PIN); //..

struct USER
{
    unsigned long ID;
}   Users[] =
{
    {0xA119F0E3},  //pun UL la final de la usigned long
    {0x315AF7E3},
    {0xD1CA08E4},
    {0xA1E6F5E3}
};

const byte UserCount = sizeof Users / sizeof Users[0];

void setup() {
    Serial.begin(9600); //parte de comunicare intre placuta si calculator
    //9600-este standard, care semnifica cati biti sunt trimisi pe secunda
    //cu cat numarul e mai mare cu atat datele sunt trimise mai repede
    while(!Serial); //vrem ca dupa executarea while-ului Serial sa fie complet executat
    
    pinMode(LED_RED_PIN, OUTPUT); 
    pinMode(LED_GREEN_PIN, OUTPUT);
    
    SPI.begin(); //permite sa comunic prin intermediul arduino cu senzorul RFID
    RFID.PCD_Init(); //initializam pentru senzor pini (conexiunea dintre arduino si senzor (ca la define))
    //"citeste conexiunea cablurilor"
}

void loop() {
    if (!RFID.PICC_IsNewCardPresent()) //PICC- Proximity integrsated circuit card
        return; 
    //daca nu am nici un card apropiat atunci ies din loop

    readRFID();
}

void readRFID()
{
    if (!RFID.PICC_ReadCardSerial()) //verific daca s-a citit ID-ul
        return;

    unsigned long UIDVal = RFID.uid.uidByte[0]; //UIDVal- valoarea UID(user ID)
    UIDVal = (UIDVal << 8) | RFID.uid.uidByte[1];
    UIDVal = (UIDVal << 8) | RFID.uid.uidByte[2];
    UIDVal = (UIDVal << 8) | RFID.uid.uidByte[3];
    //citesc id-ul cardului punandu-l pe 32 de biti
    //Serial.println(UIDVal, HEX); //afisarea in hexazecimal

    boolean authorized = false;
    for( int i = 0; i < UserCount; i++)
    {
        if(UIDVal == Users[i].ID)
        {
            authorized = true;
            break; // nu are rost sa mai parcurg for-ul daca l-am gasit
        }
    }

    if (authorized)
    {
        Serial.println(UIDVal, HEX);
        digitalWrite(LED_GREEN_PIN, HIGH);
        delay(3000);
        digitalWrite(LED_GREEN_PIN, LOW);
        delay(500);
    }
    else
    {
        digitalWrite(LED_RED_PIN, HIGH);
        delay(3000);
        digitalWrite(LED_RED_PIN, LOW);
        delay(500);
    }
}